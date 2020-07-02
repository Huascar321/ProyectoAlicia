#from-import por defecto de rasa
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#Nuevos
from fechaHora import *

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class saludar(Action):

    def name(self) -> Text:
        return "actions_saludar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día

        hora = horaActualInt()
        texto = ""

        if(hora >= 5) and (hora <= 11):
            texto = "Buen día 🌤 \nEstaba tomando un café ☕ \nMi nombre es ALICIA 🙋🏽 y resolveré tus dudas sobre el COVID-19! \n¿Cual es tu duda? 🤔"
        elif (hora >= 12) and (hora <= 15):
            texto = "Buenas tardes 🌇 \nEstaba leyendo 📖 \nMi nombre es ALICIA 🙋🏽 y resolveré tus dudas sobre el COVID-19! \n¿Cual es tu duda? 🤔"
        elif ((hora >= 16) and (hora <= 23)) or ((hora >= 0) and (hora <= 4)):
            texto = "Buenas noches 🌙 \nEstoy despierta 🦉 \nMi nombre es ALICIA 🙋🏽 y resolveré tus dudas sobre el COVID-19! \n¿Cual es tu duda? 🤔"
        else:
            texto = "Hola! Un gusto conocerte 👋🏽 \nMi nombre es ALICIA 🙋🏽 y resolveré tus dudas sobre el COVID-19! \n¿Cual es tu duda? 🤔"

        dispatcher.utter_message(text=texto)

        return []
