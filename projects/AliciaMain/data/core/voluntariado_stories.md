## Quiero ayudar, soy doctor, afirmar
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyDoctor OR afirmar
  - utter_quieroAyudar_soyDoctor
  - actions_verificarCanal
* afirmar
  - utter_desplegarMenu

## Quiero ayudar, soy doctor, negar
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyDoctor OR afirmar
  - utter_quieroAyudar_soyDoctor
  - actions_verificarCanal
* negar
  - utter_negarPregunta

## Quiero ayudar, soy ninguno
* quieroAyudar
  - utter_quieroAyudar
* quieroAyudar_soyNinguno OR negar
- utter_quieroAyudar_soyNinguno
- utter_desplegarMenu
