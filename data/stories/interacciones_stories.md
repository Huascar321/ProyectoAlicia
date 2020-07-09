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

## faq, afirmar pregunta, FALLO
* faq
  - respond_faq
* afirmar
  - utter_tengoPreguntas
* out_of_scope
  - utter_default

## faq, negar pregunta
* faq
  - respond_faq
* negar
  - utter_negarPregunta

## faq, negar pregunta, FALLO
* faq
  - respond_faq
* negar
  - utter_negarPregunta
* out_of_scope
  - utter_default

## faq, pregunta equivocada
* faq
  - respond_faq
* out_of_scope
  - utter_default

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

## Fuera de lugar
* out_of_scope
  - utter_default
