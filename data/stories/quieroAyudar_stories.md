## Quiero ayudar, soy doctor, afirmar pregunta final CAMINO
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyDoctor OR afirmar
  - utter_quieroAyudar_soyDoctor
  - actions_verificarCanal
* afirmar
  - utter_desplegarMenu

## Quiero ayudar, soy doctor, afirmar pregunta final CAMINO, FALLO
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyDoctor OR afirmar
  - utter_quieroAyudar_soyDoctor
  - actions_verificarCanal
* afirmar
  - utter_desplegarMenu
* out_of_scope
  - utter_default

## Quiero ayudar, soy doctor, negar pregunta final CAMINO
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyDoctor OR afirmar
  - utter_quieroAyudar_soyDoctor
  - actions_verificarCanal
* negar
  - utter_negarPregunta

## Quiero ayudar, soy doctor, negar pregunta final CAMINO, FALLO
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyDoctor OR afirmar
  - utter_quieroAyudar_soyDoctor
  - actions_verificarCanal
* negar
  - utter_negarPregunta
* out_of_scope
  - utter_default

## Quiero ayudar, soy ninguno, negar pregunta final CAMINO
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyNinguno
- utter_quieroAyudar_soyNinguno
- utter_desplegarMenu
