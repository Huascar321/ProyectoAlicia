## Tengo preguntas CAMINO
* tengoPreguntas
  - utter_tengoPreguntas

## Activar menu CAMINO
* activarMenu
  - utter_desplegarMenu

## chitchat
* chitchat
  - respond_chitchat

## faq, afirmar pregunta
* faq
  - respond_faq
* afirmar
  - utter_tengoPreguntas

## faq, negar pregunta
* faq
  - respond_faq
* negar
  - utter_negarPregunta

## Compartir Contacto, negar pregunta final
* QuieroCompartir
  - utter_QuieroCompartir
  - actions_verificarCanal
* afirmar
  - utter_desplegarMenu

## Compartir Contacto, negar pregunta final
* QuieroCompartir
  - utter_QuieroCompartir
  - actions_verificarCanal
* negar
  - utter_negarPregunta
