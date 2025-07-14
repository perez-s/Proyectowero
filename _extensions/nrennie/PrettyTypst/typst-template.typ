
#let PrettyTypst(
  // The document title.
  title: "PrettyTypst",

  // Logo in top right corner.
  typst-logo: none,

  // The document content.
  body
) = {

  // Set document metadata.
  set document(title: title)
  
  // Configure pages.
  set page(
    header: [
            #set align(center)
            #show table.cell.where(y: 0): set text(weight: "regular")
            #show table.cell.where(y: 1): set text(weight: "regular")
            #table(
              columns: (1fr, 1fr, 1fr),
              align: (center + horizon, center + horizon, left),
              stroke: 1pt,
              // fill: (none, none, rgb("#6777216n")),
            [*Código:* WCEC],
            table.cell(
                rowspan: 2,
            )[*Operativo* ],
            table.cell(
                rowspan: 4,
                align: center + horizon,
                fill: none,
            )[#image("logo.png", width: 50%)],
            [
            *Versión:* 02
            ],
            [
            *Consecutivo:
            *20210323
            ],
            table.cell(
                rowspan: 2,
            )[
            *Informe de Actividades*
            ],
            [
            *Fecha
            formato:* 18/08/2021
            ],
            )],
    margin: (left: 2cm, right: 1.5cm, top: 4cm, bottom: 2cm),
    numbering: "1",
    number-align: right,
    // background: place(right + top, rect(
    //   fill: rgb("#E6E6FA"),
    //   height: 100%,
    //   width: 3cm,
    // ))
  )
  
  // Set the body font.
  set table(
    text(8pt, font: "Montserrat")
  )
  set text(10pt, font: "Montserrat")
  set figure.caption(
    separator: [.]   
    )
  show figure.caption: it => context [
    *#it.supplement~#it.counter.display()#it.separator*#it.body
  ]

  
  set heading(numbering: "1.1.1.")
  // Configure headings.
  show heading.where(level: 1): set block(below: 0.8em)
  // show heading.where(level: 1): underline
  show heading.where(level: 2): set block(above: 0.5cm, below: 0.5cm)

  // Links should be purple.
  show link: set text(rgb("#800080"))

  // show figure: set block(breakable: true)

  // Configure light purple border.
  // show figure: it => block({
  //   move(dx: -3%, dy: 1.5%, rect(
  //     fill: rgb("FF7D79"),
  //     inset: 0pt,
  //     move(dx: 3%, dy: -1.5%, it.body)
  //   ))
  // })

  set par(
    justify: true,
    spacing: 12pt,
  )
  body
  // v(1fr)
  // Purple border column
  // grid(
  //   columns: (1fr),
  //   column-gutter: 2.5cm,

  //   // Title.
  //   // pad(bottom: 1cm, text(font: "Montserrat", 20pt, weight: 800, upper(title))),
    
  //   // The main body text.
  //   {
  //     set par(justify: true)
  //     body
  //     v(1fr)
  //   },
  

  // )
}


