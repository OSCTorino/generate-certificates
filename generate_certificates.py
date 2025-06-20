#!/usr/bin/env python

import csv
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from random import choice, randint, seed

COLORS = ["#b30033", "#007a7d", "#002060"]


def get_random_color():
    return choice(COLORS)


def get_random_opacity_str():
    op = randint(10, 80)
    return f"{op}%"


def get_random_radius_mod():
    op = randint(0, 50) / 100
    sign = choice(["+", "-"])
    return f"{sign} {op}cm"


HELP_MSG = """Utility to generate OSCT certificates.

This takes a template Typst source file and fills in some meta-information,
finally calling the Typst compiler to create the output PDF.
It makes creating many certificates a breeze, if given a correct template
file and participant table.

The input attendees file should be a CSV file with the following columns, which
will be used to replace the text in the template file:
- 'name' -> '{{issued_to}}'
- 'issuer' -> '{{issuer}}'
- 'issuer_orcid' -> '{{issuer_orcid}}'
- 'event_name' -> '{{event}}'
- 'event_description' -> '{{event_description}}'
- 'certificate_id' -> '{{unique_id}}'
- 'certificate_link' -> '{{id_link}}'
- 'date' -> '{{event_date}}'
- 'certificate_date' -> '{{issued_on}}'
- 'certificate_location' -> '{{issued_at}}'

Additionally, the following special characters will be replaced:
- '{{rand.color}}' -> Replaced with a random RGB Hex color from the OSCT palette.
- '{{rand.opacity}}' -> Replaced with a random percentage opacity, from 10% to 80%.
- '{{rand.jiggle}}' -> Replaced with a random jiggle of +- 0.90 cm

All generated files will be saved in the specified "output_dir".

This script requires a typst compiler that can be invoked with the command
'typst' present in $PATH.
"""

REPLACEMENTS = {
    "{{issued_to}}": "name",
    "{{issuer}}": "issuer",
    "{{issuer_orcid}}": "issuer_orcid",
    "{{event}}": "event_name",
    "{{event_description}}": "event_description",
    "{{unique_id}}": "certificate_id",
    "{{id_link}}": "certificate_link",
    "{{event_date}}": "date",
    "{{issued_on}}": "certificate_date",
    "{{issued_at}}": "certificate_location",
    "{{rand.color}}": get_random_color,
    "{{rand.opacity}}": get_random_opacity_str,
    "{{rand.jiggle}}": get_random_radius_mod,
}


def compile(context: Path, target: str, output: Path) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy in the context
        shutil.copytree(context, tmpdir, dirs_exist_ok=True)

        # Write the target file
        target_path = (
            Path(tmpdir)
            / "this_is_the_compiler_target_hopefully_not_in_the_context.typ"
        )
        with (target_path).open("w+") as handle:
            handle.write(target)

        os.makedirs(output.parent, exist_ok=True)

        # Launch the compiler
        return subprocess.run(
            ["typst", "compile", target_path, output], check=True, capture_output=True
        )


def replace_template(content: str, values: dict) -> str:
    for target, replacement in REPLACEMENTS.items():
        if not callable(replacement):
            replacement = values[replacement]
            content = content.replace(target, replacement)
            continue
        # We need to replace multiple times here, each with a new call
        # this is to generate the appropriate number of random colors/opacities

        keep_replacing = True
        while keep_replacing:
            new_rep = replacement()
            new_con = content.replace(target, new_rep, count=1)
            if content == new_con:
                keep_replacing = False
            content = new_con

    return content


def main(args):
    with args.template.open("r+") as handle:
        content = handle.read()

    with args.input_file.open("r+") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            print(f"Generating certificate for {row['name']}...")
            new_content = replace_template(content, row)

            sanitized_name = f"{row['name']}_cert.pdf".replace(" ", "_")
            output = args.output_dir / sanitized_name
            compile(args.context, new_content, output)

    print("All done!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=HELP_MSG
    )

    parser.add_argument(
        "input_file",
        type=Path,
        help="CSV file with the information of the attendees to generate certificates to",
    )
    parser.add_argument(
        "output_dir", type=Path, help="Directory to generate certificates to"
    )
    parser.add_argument(
        "--template",
        type=Path,
        help="Path to the Typst template to use in the context directory",
        default=Path("./main.typ"),
    )
    parser.add_argument(
        "--context",
        type=Path,
        help="Folder the context to use during compilation",
        default=Path("./context"),
    )
    parser.add_argument(
        "--static-colors",
        action="store_true",
        help="Generate the same color/bubble size combo given the same CSV file",
    )

    args = parser.parse_args()

    if args.static_colors:
        seed(1)

    main(args)
