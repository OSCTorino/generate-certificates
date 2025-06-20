#import "@preview/suiji:0.4.0": *
#import "@preview/cades:0.3.0": qr-code

#set page(paper: "a4")

// This controls the data in the certificate
#let certificate(
  issued_to: [],
  issuer: [],
  issuer_orcid: [],
  event: [],
  event_extra: [],
  unique_id: "",
  id_link: "",
  event_date: "",
  issued_on: "",
  issued_at: ""
) = [
  #set text(font: "Atkinson Hyperlegible", size: 20pt)
  #place(
  center,
  dx: 0cm, dy: 4.8cm,
  [
    #text(size:30pt, weight: "bold")[Certificate of Attendance]
    
    The Open Science Community Torino certifies that
    
    *#issued_to*
  
    has attended the event
  
    "#text(style: "italic", event)"
  
    held on #event_date#event_extra.
  ]
  )

  #place(
    bottom+left,
    dx: 0cm, dy: -0cm,
    [
      #set text(size: 13pt)
      This certification has been issued by #issuer (#issuer_orcid) on behalf of the Open Science Community Torino.
      
      #if (unique_id.len() > 0) [
        This certificate has an associated unique ID: #unique_id
      ]

      #v(0.6cm)
      #issued_at, \
      #issued_on

      #if (id_link.len() > 0) [
        #move(
          dx: -1.5cm, dy: 1.5cm,
          qr-code(unique_id, width: 5cm)
        )
      ] else [
        #v(3cm)
      ]
    ]
  )
]

#let circle_at(
  x, y,
  radius: 1cm,
  opacity: 0%,
  color: ""
) = {
  
  place(
    top+left,
    dx: x, dy: y,
    {
      circle(
        radius: radius,
        fill: rgb(color).transparentize(opacity)
      )
    }
  )
}

// Show the decorative coloured circles
// Top-left
#circle_at(-5cm, -8cm, radius: 5cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(-6cm, -3cm, radius: 3cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(-2cm, -0.5cm, radius: 2cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(2cm, -5cm, radius: 3cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(6cm, 0cm, radius: 1cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(6cm, -3cm, radius: 1.5cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")

// Bottom-right
#circle_at(12cm, 23cm, radius: 5cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(9cm, 26cm, radius: 3cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(15cm, 22cm, radius: 1cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(8cm, 24cm, radius: 2cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(16cm, 20cm, radius: 2cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")
#circle_at(6cm, 26cm, radius: 1.5cm {{rand.jiggle}}, opacity: {{rand.opacity}}, color: "{{rand.color}}")

// Top-right logo
#place(
  top+right,
  dx: 2cm, dy: -2cm,
  image("resources/Logo_OSC_Torino.png", width: 50%)
)

#certificate(
  issued_to: [{{issued_to}}],
  issuer: [{{issuer}}],
  issuer_orcid: [{{issuer_orcid}}],
  event: [{{event}}],
  event_extra: [{{event_description}}],
  unique_id: "{{unique_id}}",
  id_link: "{{id_link}}",
  event_date: "{{event_date}}",
  issued_on: "{{issued_on}}",
  issued_at: "{{issued_at}}"
)

