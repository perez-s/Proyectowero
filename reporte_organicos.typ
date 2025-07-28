// Some definitions presupposed by pandoc's typst output.
#let blockquote(body) = [
  #set text( size: 0.92em )
  #block(inset: (left: 1.5em, top: 0.2em, bottom: 0.2em))[#body]
]

#let horizontalrule = line(start: (25%,0%), end: (75%,0%))

#let endnote(num, contents) = [
  #stack(dir: ltr, spacing: 3pt, super[#num], contents)
]

#show terms: it => {
  it.children
    .map(child => [
      #strong[#child.term]
      #block(inset: (left: 1.5em, top: -0.4em))[#child.description]
      ])
    .join()
}

// Some quarto-specific definitions.

#show raw.where(block: true): set block(
    fill: luma(230),
    width: 100%,
    inset: 8pt,
    radius: 2pt
  )

#let block_with_new_content(old_block, new_content) = {
  let d = (:)
  let fields = old_block.fields()
  fields.remove("body")
  if fields.at("below", default: none) != none {
    // TODO: this is a hack because below is a "synthesized element"
    // according to the experts in the typst discord...
    fields.below = fields.below.abs
  }
  return block.with(..fields)(new_content)
}

#let empty(v) = {
  if type(v) == str {
    // two dollar signs here because we're technically inside
    // a Pandoc template :grimace:
    v.matches(regex("^\\s*$")).at(0, default: none) != none
  } else if type(v) == content {
    if v.at("text", default: none) != none {
      return empty(v.text)
    }
    for child in v.at("children", default: ()) {
      if not empty(child) {
        return false
      }
    }
    return true
  }

}

// Subfloats
// This is a technique that we adapted from https://github.com/tingerrr/subpar/
#let quartosubfloatcounter = counter("quartosubfloatcounter")

#let quarto_super(
  kind: str,
  caption: none,
  label: none,
  supplement: str,
  position: none,
  subrefnumbering: "1a",
  subcapnumbering: "(a)",
  body,
) = {
  context {
    let figcounter = counter(figure.where(kind: kind))
    let n-super = figcounter.get().first() + 1
    set figure.caption(position: position)
    [#figure(
      kind: kind,
      supplement: supplement,
      caption: caption,
      {
        show figure.where(kind: kind): set figure(numbering: _ => numbering(subrefnumbering, n-super, quartosubfloatcounter.get().first() + 1))
        show figure.where(kind: kind): set figure.caption(position: position)

        show figure: it => {
          let num = numbering(subcapnumbering, n-super, quartosubfloatcounter.get().first() + 1)
          show figure.caption: it => {
            num.slice(2) // I don't understand why the numbering contains output that it really shouldn't, but this fixes it shrug?
            [ ]
            it.body
          }

          quartosubfloatcounter.step()
          it
          counter(figure.where(kind: it.kind)).update(n => n - 1)
        }

        quartosubfloatcounter.update(0)
        body
      }
    )#label]
  }
}

// callout rendering
// this is a figure show rule because callouts are crossreferenceable
#show figure: it => {
  if type(it.kind) != str {
    return it
  }
  let kind_match = it.kind.matches(regex("^quarto-callout-(.*)")).at(0, default: none)
  if kind_match == none {
    return it
  }
  let kind = kind_match.captures.at(0, default: "other")
  kind = upper(kind.first()) + kind.slice(1)
  // now we pull apart the callout and reassemble it with the crossref name and counter

  // when we cleanup pandoc's emitted code to avoid spaces this will have to change
  let old_callout = it.body.children.at(1).body.children.at(1)
  let old_title_block = old_callout.body.children.at(0)
  let old_title = old_title_block.body.body.children.at(2)

  // TODO use custom separator if available
  let new_title = if empty(old_title) {
    [#kind #it.counter.display()]
  } else {
    [#kind #it.counter.display(): #old_title]
  }

  let new_title_block = block_with_new_content(
    old_title_block, 
    block_with_new_content(
      old_title_block.body, 
      old_title_block.body.body.children.at(0) +
      old_title_block.body.body.children.at(1) +
      new_title))

  block_with_new_content(old_callout,
    block(below: 0pt, new_title_block) +
    old_callout.body.children.at(1))
}

// 2023-10-09: #fa-icon("fa-info") is not working, so we'll eval "#fa-info()" instead
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: false, 
    fill: background_color, 
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"), 
    width: 100%, 
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%, 
      below: 0pt, 
      block(
        fill: background_color, 
        width: 100%, 
        inset: 8pt)[#text(icon_color, weight: 900)[#icon] #title]) +
      if(body != []){
        block(
          inset: 1pt, 
          width: 100%, 
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    )
}


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



#show: PrettyTypst.with(
  title: "Reporte Wero",
  typst-logo: (
    path: "logo.png",
    caption: []
  ), 
)




#set align(center)
#table(
  columns: 4,
  align: (right + horizon, center + horizon, right + horizon, center + horizon),
  fill: (rgb("#d9d9d9"), none, rgb("#d9d9d9"), none),
[
 *Fecha presentación:*
 ],
table.cell(
    colspan: 3,
    align: center,
)[28 de julio de 2025],
[
 *Nombre del documento:*
 ],
table.cell(
    colspan: 3,
    align: center,
)[Proyecto Piloto Circularidad de
 Residuos (Coca Cola – Qbano)],
[
 *Fecha inicio de
 proyecto:*
 ],
table.cell(
    colspan: 3,
    align: center,
)[13 de diciembre de 2023],
[
 *No. del documento:*
 ],
[1],
[
 *Periodo del informe:*
 ],
[Del 2024-07-09 al 2025-07-14],
)
#set align(left)
= Información General
<información-general>
A continuación, en las siguientes tablas se presentan los datos registrados con corte al 14 de julio de 2025 del proyecto de circularidad de residuos en los 27 puntos de venta de Qbano seleccionados para el piloto, 15 en la ciudad de Cali, 1 en la ciudad de Bucaramanga, 1 en la ciudad de Barranquilla, 9 en la ciudad de Bogotá y 1 en la ciudad de Medellín. Estos resultados son gracias al esfuerzo conjunto entre Coca Cola y Qbano para promover acciones encaminadas a la circularidad, la sostenibilidad y lograr Un Mundo Sin Residuos.

#set table(stroke: (x, y) => (
  left: if x == 0 or y > 0 { 0pt } else { 0pt },
  right: 0pt,
  top: if y == 1 { 0.5pt } else if y == 0 { 0.5pt } else { 0pt },
  bottom: 0.5pt,
))


#set text(8pt)
#show table.cell.where(y: 0): set text(weight: "bold")
#figure([
#table(
  columns: 4,
  align: (center,center,center,center,),
  table.header(table.cell(align: center)[Ciudad], table.cell(align: center)[Cantidad RS (kg)], table.cell(align: center)[Recolecciones], table.cell(align: center)[Kg/recolección],),
  table.hline(),
  table.cell(align: center)[Barranquilla], table.cell(align: center)[250,6], table.cell(align: center)[3,0], table.cell(align: center)[83,5],
  table.cell(align: center)[Bogotá], table.cell(align: center)[2\'579,9], table.cell(align: center)[1\'067,0], table.cell(align: center)[2,4],
  table.cell(align: center)[Bucaramanga], table.cell(align: center)[51,0], table.cell(align: center)[3,0], table.cell(align: center)[17,0],
  table.cell(align: center)[Cali], table.cell(align: center)[14\'162,9], table.cell(align: center)[1\'733,0], table.cell(align: center)[8,2],
  table.cell(align: center)[Medellín], table.cell(align: center)[77,0], table.cell(align: center)[10,0], table.cell(align: center)[7,7],
)
], caption: figure.caption(
position: top, 
[
Resumen general resultados operativos.
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-1>



#show figure: set block(breakable: true)
#figure([
#table(
  columns: (15%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 10%),
  align: (right,center,center,center,center,center,center,center,center,center,center,center,center,center,center,),
  table.header(table.cell(align: center, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Ciudad], table.cell(align: center)[jul. 24], table.cell(align: center)[ago. 24], table.cell(align: center)[sep. 24], table.cell(align: center)[oct. 24], table.cell(align: center)[nov. 24], table.cell(align: center)[dic. 24], table.cell(align: center)[ene. 25], table.cell(align: center)[feb. 25], table.cell(align: center)[mar. 25], table.cell(align: center)[abr. 25], table.cell(align: center)[may. 25], table.cell(align: center)[jun. 25], table.cell(align: center)[jul. 25], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[Total],),
  table.hline(),
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Bogotá], table.cell(align: center)[193,5], table.cell(align: center)[285,0], table.cell(align: center)[281,5], table.cell(align: center)[234,5], table.cell(align: center)[208,5], table.cell(align: center)[177,5], table.cell(align: center)[187,2], table.cell(align: center)[230,0], table.cell(align: center)[259,5], table.cell(align: center)[154,0], table.cell(align: center)[11,3], table.cell(align: center)[348,9], table.cell(align: center)[8,5], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[2\'579,9],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Cali], table.cell(align: center)[513,1], table.cell(align: center)[432,7], table.cell(align: center)[684,0], table.cell(align: center)[949,6], table.cell(align: center)[910,5], table.cell(align: center)[1\'091,7], table.cell(align: center)[1\'075,2], table.cell(align: center)[1\'153,5], table.cell(align: center)[1\'976,8], table.cell(align: center)[1\'747,1], table.cell(align: center)[137,4], table.cell(align: center)[3\'392,3], table.cell(align: center)[98,9], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[14\'162,9],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Barranquilla], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[41,7], table.cell(align: center)[106,0], table.cell(align: center)[102,9], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[250,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Bucaramanga], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[17,0], table.cell(align: center)[17,0], table.cell(align: center)[17,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[51,0],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Medellín], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[57,7], table.cell(align: center)[19,2], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[77,0],
  table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), right: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Total], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[706,6], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[717,7], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'007,2], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'307,1], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'296,6], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'305,4], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'262,4], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'383,5], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[2\'236,3], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'901,1], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[148,8], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[3\'741,2], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[107,4], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), left: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[17\'121,3],
)
], caption: figure.caption(
position: top, 
[
Número de recolecciones realizadas por mes de operación
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-2>



#show figure: set block(breakable: true)
#figure([
#table(
  columns: (15%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 10%),
  align: (center,center,center,center,center,center,center,center,center,center,center,center,center,center,center,),
  table.header(table.cell(align: center, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Sucursal], table.cell(align: center)[jul. 24], table.cell(align: center)[ago. 24], table.cell(align: center)[sep. 24], table.cell(align: center)[oct. 24], table.cell(align: center)[nov. 24], table.cell(align: center)[dic. 24], table.cell(align: center)[ene. 25], table.cell(align: center)[feb. 25], table.cell(align: center)[mar. 25], table.cell(align: center)[abr. 25], table.cell(align: center)[may. 25], table.cell(align: center)[jun. 25], table.cell(align: center)[jul. 25], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[Total],),
  table.hline(),
  table.cell(align: center, colspan: 15, stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Bogotá],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Connecta], table.cell(align: center)[29,5], table.cell(align: center)[34,5], table.cell(align: center)[31,0], table.cell(align: center)[33,0], table.cell(align: center)[30,0], table.cell(align: center)[15,5], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[173,5],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Galan], table.cell(align: center)[27,0], table.cell(align: center)[46,0], table.cell(align: center)[51,0], table.cell(align: center)[46,0], table.cell(align: center)[30,0], table.cell(align: center)[37,0], table.cell(align: center)[41,0], table.cell(align: center)[57,0], table.cell(align: center)[45,5], table.cell(align: center)[38,0], table.cell(align: center)[3,0], table.cell(align: center)[66,0], table.cell(align: center)[1,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[488,5],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Kennedy], table.cell(align: center)[17,0], table.cell(align: center)[29,0], table.cell(align: center)[37,5], table.cell(align: center)[32,0], table.cell(align: center)[33,0], table.cell(align: center)[29,0], table.cell(align: center)[33,5], table.cell(align: center)[33,0], table.cell(align: center)[45,5], table.cell(align: center)[28,0], table.cell(align: center)[2,5], table.cell(align: center)[59,8], table.cell(align: center)[1,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[380,8],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Lourdes], table.cell(align: center)[16,5], table.cell(align: center)[26,0], table.cell(align: center)[29,5], table.cell(align: center)[16,5], table.cell(align: center)[21,0], table.cell(align: center)[14,0], table.cell(align: center)[20,5], table.cell(align: center)[22,5], table.cell(align: center)[27,0], table.cell(align: center)[14,0], table.cell(align: center)[0,5], table.cell(align: center)[36,6], table.cell(align: center)[1,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[245,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Mundo Aventura], table.cell(align: center)[11,5], table.cell(align: center)[20,5], table.cell(align: center)[16,0], table.cell(align: center)[17,0], table.cell(align: center)[11,0], table.cell(align: center)[22,0], table.cell(align: center)[20,5], table.cell(align: center)[23,0], table.cell(align: center)[13,5], table.cell(align: center)[7,5], table.cell(align: center)[2,0], table.cell(align: center)[23,5], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[188,0],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Pepe Sierra], table.cell(align: center)[48,0], table.cell(align: center)[25,0], table.cell(align: center)[34,0], table.cell(align: center)[27,0], table.cell(align: center)[31,0], table.cell(align: center)[23,0], table.cell(align: center)[20,0], table.cell(align: center)[32,0], table.cell(align: center)[50,0], table.cell(align: center)[20,5], table.cell(align: center)[1,3], table.cell(align: center)[60,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[371,8],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Quinta Paredes], table.cell(align: center)[12,0], table.cell(align: center)[22,0], table.cell(align: center)[20,0], table.cell(align: center)[18,0], table.cell(align: center)[11,0], table.cell(align: center)[6,0], table.cell(align: center)[14,0], table.cell(align: center)[18,0], table.cell(align: center)[22,0], table.cell(align: center)[12,0], table.cell(align: center)[0,0], table.cell(align: center)[19,0], table.cell(align: center)[2,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[176,0],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Santa Isabel], table.cell(align: center)[10,5], table.cell(align: center)[29,0], table.cell(align: center)[25,5], table.cell(align: center)[24,0], table.cell(align: center)[23,5], table.cell(align: center)[16,0], table.cell(align: center)[18,2], table.cell(align: center)[31,5], table.cell(align: center)[36,0], table.cell(align: center)[18,0], table.cell(align: center)[1,0], table.cell(align: center)[36,0], table.cell(align: center)[2,5], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[271,7],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Villa del Prado], table.cell(align: center)[21,5], table.cell(align: center)[53,0], table.cell(align: center)[37,0], table.cell(align: center)[21,0], table.cell(align: center)[18,0], table.cell(align: center)[15,0], table.cell(align: center)[19,5], table.cell(align: center)[13,0], table.cell(align: center)[20,0], table.cell(align: center)[16,0], table.cell(align: center)[1,0], table.cell(align: center)[48,0], table.cell(align: center)[1,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[284,0],
  table.cell(align: center, colspan: 15, stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Cali],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Av. Roosevelt], table.cell(align: center)[25,4], table.cell(align: center)[28,8], table.cell(align: center)[34,8], table.cell(align: center)[25,4], table.cell(align: center)[30,1], table.cell(align: center)[15,1], table.cell(align: center)[9,2], table.cell(align: center)[21,1], table.cell(align: center)[34,3], table.cell(align: center)[18,4], table.cell(align: center)[0,0], table.cell(align: center)[31,2], table.cell(align: center)[3,1], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[277,0],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Calima], table.cell(align: center)[51,4], table.cell(align: center)[42,9], table.cell(align: center)[44,5], table.cell(align: center)[48,9], table.cell(align: center)[46,1], table.cell(align: center)[67,8], table.cell(align: center)[78,8], table.cell(align: center)[43,2], table.cell(align: center)[52,1], table.cell(align: center)[43,9], table.cell(align: center)[0,0], table.cell(align: center)[66,2], table.cell(align: center)[1,7], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[587,5],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Ciudad Jardín], table.cell(align: center)[15,7], table.cell(align: center)[28,6], table.cell(align: center)[21,9], table.cell(align: center)[29,6], table.cell(align: center)[38,3], table.cell(align: center)[31,4], table.cell(align: center)[66,7], table.cell(align: center)[102,7], table.cell(align: center)[331,5], table.cell(align: center)[369,4], table.cell(align: center)[31,1], table.cell(align: center)[563,1], table.cell(align: center)[33,9], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'663,8],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Cámbulos], table.cell(align: center)[15,9], table.cell(align: center)[14,7], table.cell(align: center)[24,5], table.cell(align: center)[16,7], table.cell(align: center)[25,3], table.cell(align: center)[28,1], table.cell(align: center)[36,5], table.cell(align: center)[28,6], table.cell(align: center)[45,5], table.cell(align: center)[34,4], table.cell(align: center)[1,0], table.cell(align: center)[59,3], table.cell(align: center)[4,8], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[335,4],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Guayacanes], table.cell(align: center)[23,0], table.cell(align: center)[17,7], table.cell(align: center)[37,5], table.cell(align: center)[56,3], table.cell(align: center)[46,0], table.cell(align: center)[40,5], table.cell(align: center)[51,6], table.cell(align: center)[47,7], table.cell(align: center)[38,1], table.cell(align: center)[47,2], table.cell(align: center)[2,4], table.cell(align: center)[63,6], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[471,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[La Merced], table.cell(align: center)[196,4], table.cell(align: center)[97,7], table.cell(align: center)[271,1], table.cell(align: center)[275,9], table.cell(align: center)[295,4], table.cell(align: center)[335,4], table.cell(align: center)[320,8], table.cell(align: center)[306,1], table.cell(align: center)[405,7], table.cell(align: center)[351,4], table.cell(align: center)[53,6], table.cell(align: center)[584,6], table.cell(align: center)[19,8], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[3\'514,1],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Norte 1], table.cell(align: center)[24,9], table.cell(align: center)[28,1], table.cell(align: center)[42,9], table.cell(align: center)[73,8], table.cell(align: center)[58,8], table.cell(align: center)[76,0], table.cell(align: center)[63,4], table.cell(align: center)[95,8], table.cell(align: center)[381,8], table.cell(align: center)[276,8], table.cell(align: center)[12,6], table.cell(align: center)[534,7], table.cell(align: center)[17,5], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'687,0],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Norte 2], table.cell(align: center)[31,6], table.cell(align: center)[38,2], table.cell(align: center)[41,5], table.cell(align: center)[44,4], table.cell(align: center)[78,8], table.cell(align: center)[74,1], table.cell(align: center)[44,4], table.cell(align: center)[55,8], table.cell(align: center)[62,6], table.cell(align: center)[69,2], table.cell(align: center)[5,2], table.cell(align: center)[100,6], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[646,4],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Panamericano], table.cell(align: center)[9,1], table.cell(align: center)[18,9], table.cell(align: center)[26,9], table.cell(align: center)[25,8], table.cell(align: center)[33,4], table.cell(align: center)[60,1], table.cell(align: center)[43,3], table.cell(align: center)[38,4], table.cell(align: center)[56,2], table.cell(align: center)[28,2], table.cell(align: center)[0,0], table.cell(align: center)[68,9], table.cell(align: center)[2,2], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[411,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Republica de Israel], table.cell(align: center)[12,9], table.cell(align: center)[18,0], table.cell(align: center)[28,2], table.cell(align: center)[22,8], table.cell(align: center)[32,4], table.cell(align: center)[30,6], table.cell(align: center)[25,4], table.cell(align: center)[31,8], table.cell(align: center)[17,4], table.cell(align: center)[19,9], table.cell(align: center)[2,4], table.cell(align: center)[29,3], table.cell(align: center)[0,9], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[272,1],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[San Fernando], table.cell(align: center)[75,6], table.cell(align: center)[71,1], table.cell(align: center)[81,6], table.cell(align: center)[99,8], table.cell(align: center)[97,7], table.cell(align: center)[114,2], table.cell(align: center)[99,2], table.cell(align: center)[115,5], table.cell(align: center)[158,2], table.cell(align: center)[117,5], table.cell(align: center)[10,2], table.cell(align: center)[186,9], table.cell(align: center)[7,5], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'235,1],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Valle Grande], table.cell(align: center)[31,2], table.cell(align: center)[28,0], table.cell(align: center)[28,6], table.cell(align: center)[23,5], table.cell(align: center)[20,8], table.cell(align: center)[32,5], table.cell(align: center)[34,3], table.cell(align: center)[37,1], table.cell(align: center)[34,4], table.cell(align: center)[31,0], table.cell(align: center)[12,8], table.cell(align: center)[34,6], table.cell(align: center)[7,3], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[356,1],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Normandia], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[206,7], table.cell(align: center)[107,6], table.cell(align: center)[185,8], table.cell(align: center)[201,7], table.cell(align: center)[160,5], table.cell(align: center)[259,1], table.cell(align: center)[231,9], table.cell(align: center)[6,2], table.cell(align: center)[558,9], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'918,2],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Cañaveralejo], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[15,3], table.cell(align: center)[89,3], table.cell(align: center)[81,7], table.cell(align: center)[0,0], table.cell(align: center)[132,5], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[318,9],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Chapinero], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[53,7], table.cell(align: center)[10,5], table.cell(align: center)[26,1], table.cell(align: center)[0,0], table.cell(align: center)[378,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[468,3],
  table.cell(align: center, colspan: 15, stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Barranquilla],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Calle 74], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[41,7], table.cell(align: center)[106,0], table.cell(align: center)[102,9], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[250,6],
  table.cell(align: center, colspan: 15, stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Bucaramanga],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Cabecera], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[17,0], table.cell(align: center)[17,0], table.cell(align: center)[17,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[51,0],
  table.cell(align: center, colspan: 15, stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Medellín],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[La 70], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[57,7], table.cell(align: center)[19,2], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[77,0],
  table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), right: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Total], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[707], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[718], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'007], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'307], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'297], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'305], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'262], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'383], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[2\'236], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'901], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[149], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[3\'741], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[107], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), left: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[17\'121],
)
], caption: figure.caption(
position: top, 
[
Cantidad de residuos recogidos (kg) por punto de venta
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-3>



#set text(10pt)
De acuerdo con la #ref(<tbl-1>, supplement: [Tabla]), #ref(<tbl-2>, supplement: [Tabla]) y #ref(<tbl-3>, supplement: [Tabla]), se puede concluir que en cada servicio se está haciendo una recolección promedio de 8.17 kg de residuos en la ciudad de Cali, 17.00 kg de residuos en la ciudad de Bucaramanga, 83.53 kg de residuos en la ciudad de Barranquilla, 2.42 kg de residuos en la ciudad de Bogotá y 7.70 kg de residuos en la ciudad de Medellín. En la #ref(<fig-1>, supplement: [Figura]), se presenta gráficamente la composición general de los residuos sólidos aprovechables que se han entregado a la fecha de corte de este informe en las sucursales participantes del piloto; mientras tanto, en la #ref(<tbl-4>, supplement: [Tabla]), se presenta la cantidad de residuos por material en kilogramos.

#set text(8pt)
#figure([
#box(image("reporte_organicos_files/figure-typst/unnamed-chunk-13-1.svg"))

], caption: figure.caption(
position: bottom, 
[
Composición de los residuos aprovechables por tipo de material (total: 16982 kg)
]), 
kind: "quarto-float-fig", 
supplement: "Figura", 
)
<fig-1>


#figure([
#table(
  columns: (15%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 5%, 10%),
  align: (right,center,center,center,center,center,center,center,center,center,center,center,center,center,),
  table.header(table.cell(align: center, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Material], table.cell(align: center)[jul. 24], table.cell(align: center)[ago. 24], table.cell(align: center)[sep. 24], table.cell(align: center)[oct. 24], table.cell(align: center)[nov. 24], table.cell(align: center)[dic. 24], table.cell(align: center)[ene. 25], table.cell(align: center)[feb. 25], table.cell(align: center)[mar. 25], table.cell(align: center)[abr. 25], table.cell(align: center)[jun. 25], table.cell(align: center)[jul. 25], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[Total],),
  table.hline(),
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Archivo], table.cell(align: center)[101,0], table.cell(align: center)[116,0], table.cell(align: center)[130,4], table.cell(align: center)[49,4], table.cell(align: center)[96,1], table.cell(align: center)[106,0], table.cell(align: center)[65,7], table.cell(align: center)[94,9], table.cell(align: center)[67,4], table.cell(align: center)[22,0], table.cell(align: center)[99,4], table.cell(align: center)[2,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[950,2],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Cartón], table.cell(align: center)[178,9], table.cell(align: center)[230,4], table.cell(align: center)[219,9], table.cell(align: center)[284,9], table.cell(align: center)[469,7], table.cell(align: center)[428,4], table.cell(align: center)[419,7], table.cell(align: center)[378,4], table.cell(align: center)[586,8], table.cell(align: center)[373,3], table.cell(align: center)[691,6], table.cell(align: center)[39,6], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[4\'301,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[PEAD], table.cell(align: center)[16,4], table.cell(align: center)[0,0], table.cell(align: center)[2,1], table.cell(align: center)[3,5], table.cell(align: center)[21,7], table.cell(align: center)[54,9], table.cell(align: center)[45,0], table.cell(align: center)[41,0], table.cell(align: center)[42,2], table.cell(align: center)[61,7], table.cell(align: center)[54,8], table.cell(align: center)[1,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[344,4],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[PEBD], table.cell(align: center)[40,7], table.cell(align: center)[58,0], table.cell(align: center)[56,1], table.cell(align: center)[63,4], table.cell(align: center)[40,9], table.cell(align: center)[34,8], table.cell(align: center)[70,0], table.cell(align: center)[110,5], table.cell(align: center)[109,5], table.cell(align: center)[88,2], table.cell(align: center)[85,4], table.cell(align: center)[23,7], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[781,3],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[PET], table.cell(align: center)[8,8], table.cell(align: center)[73,7], table.cell(align: center)[46,0], table.cell(align: center)[156,4], table.cell(align: center)[85,3], table.cell(align: center)[73,8], table.cell(align: center)[69,8], table.cell(align: center)[111,0], table.cell(align: center)[95,0], table.cell(align: center)[86,0], table.cell(align: center)[83,6], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[889,4],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Plegadiza], table.cell(align: center)[56,4], table.cell(align: center)[74,4], table.cell(align: center)[62,5], table.cell(align: center)[72,4], table.cell(align: center)[72,4], table.cell(align: center)[54,2], table.cell(align: center)[18,3], table.cell(align: center)[37,0], table.cell(align: center)[43,7], table.cell(align: center)[58,3], table.cell(align: center)[96,2], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[645,8],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Rechazo], table.cell(align: center)[172,8], table.cell(align: center)[150,4], table.cell(align: center)[306,1], table.cell(align: center)[213,4], table.cell(align: center)[238,1], table.cell(align: center)[157,8], table.cell(align: center)[164,6], table.cell(align: center)[168,8], table.cell(align: center)[177,2], table.cell(align: center)[94,0], table.cell(align: center)[240,0], table.cell(align: center)[19,4], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[2\'102,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Vidrio], table.cell(align: center)[26,1], table.cell(align: center)[10,0], table.cell(align: center)[4,0], table.cell(align: center)[16,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[2,0], table.cell(align: center)[2,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[60,0],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Orgánicos], table.cell(align: center)[0,0], table.cell(align: center)[58,9], table.cell(align: center)[211,3], table.cell(align: center)[333,2], table.cell(align: center)[222,4], table.cell(align: center)[345,1], table.cell(align: center)[373,7], table.cell(align: center)[618,0], table.cell(align: center)[1\'104,5], table.cell(align: center)[1\'112,7], table.cell(align: center)[2\'165,2], table.cell(align: center)[137,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[6\'682,1],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Aluminio], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[1,5], table.cell(align: center)[6,0], table.cell(align: center)[5,9], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[6,0], table.cell(align: center)[23,0], table.cell(align: center)[0,0], table.cell(align: center)[11,8], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[54,2],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Polyboard], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[4,0], table.cell(align: center)[4,0], table.cell(align: center)[4,0], table.cell(align: center)[30,0], table.cell(align: center)[0,0], table.cell(align: center)[6,5], table.cell(align: center)[0,0], table.cell(align: center)[42,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[90,5],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Chatarra], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[25,0], table.cell(align: center)[43,0], table.cell(align: center)[9,0], table.cell(align: center)[3,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[80,0],
  table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), right: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Total], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[601,1], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[771,8], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'039,9], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'202,6], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'281,5], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'302,0], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'265,8], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'570,5], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[2\'257,8], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'896,2], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[3\'570,0], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[222,7], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), left: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[16\'982,1],
)
], caption: figure.caption(
position: top, 
[
Listado de materiales recibidos como materiales aprovechables
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-4>



#set text(10pt)
= Residuos Orgánicos
<residuos-orgánicos>
Por último, en la #ref(<tbl-5>, supplement: [Tabla]), se presenta la cantidad de residuos orgánicos en kilogramos, recolectados en La Merced, Cañaveralejo, Ciudad Jardín, Normandia, Norte 1 y Chapinero.

#set text(8pt)
#figure([
#table(
  columns: (15%, auto, auto, auto, 10%),
  align: (right,center,center,center,center,),
  table.header(table.cell(align: center, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Sucursal], table.cell(align: center)[sep. 24], table.cell(align: center)[mar. 25], table.cell(align: center)[abr. 25], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[Total],),
  table.hline(),
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[La Merced], table.cell(align: center)[211,3], table.cell(align: center)[181,7], table.cell(align: center)[265,9], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[658,9],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Cañaveralejo], table.cell(align: center)[0,0], table.cell(align: center)[53,1], table.cell(align: center)[79,8], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[132,9],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Ciudad Jardín], table.cell(align: center)[0,0], table.cell(align: center)[184,2], table.cell(align: center)[309,4], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[493,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Normandia], table.cell(align: center)[0,0], table.cell(align: center)[119,7], table.cell(align: center)[193,9], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[313,6],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Norte 1], table.cell(align: center)[0,0], table.cell(align: center)[170,3], table.cell(align: center)[230,5], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[400,9],
  table.cell(align: right, stroke: (right: (paint: rgb("#000000"), thickness: 0.49pt)))[Chapinero], table.cell(align: center)[0,0], table.cell(align: center)[0,0], table.cell(align: center)[26,1], table.cell(align: center, stroke: (left: (paint: rgb("#000000"), thickness: 0.49pt)))[26,1],
  table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), right: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[Total], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[211,3], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[709,0], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[1\'105,7], table.cell(align: center, fill: rgb("#ebebeb"), stroke: (bottom: (paint: rgb("#000000"), thickness: 0.49pt), left: (paint: rgb("#000000"), thickness: 0.49pt), top: (paint: rgb("#000000"), thickness: 0.49pt)))[2\'025,9],
)
], caption: figure.caption(
position: top, 
[
Listado de materiales recibidos como residuos sólidos Orgánicos (RSO)
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-5>



#set text(10pt, font: "Montserrat")
= Recomendaciones y oportunidades de mejora
<recomendaciones-y-oportunidades-de-mejora>
#block[
]




