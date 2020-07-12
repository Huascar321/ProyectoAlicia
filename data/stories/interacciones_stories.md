## Tengo preguntas CAMINO
* tengoPreguntas
  - utter_tengoPreguntas

## Activar menu CAMINO
* activarMenu
  - utter_desplegarMenu

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

## fallback whatsapp, afirmar
* afirmar
  - slot{"fallback_slot" : "True"}
  - action_activador_intent

## fallback whatsapp, negar
* negar
  - slot{"fallback_slot" : "True"}
  - action_activador_frasear

## refrasear
* reformular
  - utter_ask_rephrase
  - actions_contadorMessenger
