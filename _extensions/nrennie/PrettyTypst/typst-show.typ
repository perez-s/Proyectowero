#show: PrettyTypst.with(
$if(title)$
  title: "$title$",
$endif$
$if(typst-logo)$
  typst-logo: (
    path: "$typst-logo.path$",
    caption: [$typst-logo.caption$]
  ), 
$endif$
$if(params.cliente)$
  cliente: "$params.cliente$",
$endif$
)

