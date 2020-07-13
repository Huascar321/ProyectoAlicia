from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from fechaHora import *


class saludar(Action):

    def name(self) -> Text:
        return "actions_saludar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día

        hora = horaActualInt()
        texto = ""
        #En caso de que el slot exista, lo convertira en miniscula
        if tracker.get_slot("nombre_alicia") != None:
            slot_alicia = tracker.get_slot("nombre_alicia").lower()
        else:
            slot_alicia = "Invalido"

        #En caso de que el slot nombre_alicia exista, la saludara con un diferente template
        if(hora >= 5) and (hora <= 11):
            if (slot_alicia == "alicia"):
                dispatcher.utter_message(template='utter_saludos_dias_conocer_nombre')
                print("saludos")
            else:
                dispatcher.utter_message(template='utter_saludos_dias')
        elif (hora >= 12) and (hora <= 17):
            if (slot_alicia == "alicia"):
                dispatcher.utter_message(template='utter_saludos_tardes_conocer_nombre')
                print("saludos")
            else:
                dispatcher.utter_message(template='utter_saludos_tardes')
        elif ((hora >= 18) and (hora <= 23)) or ((hora >= 0) and (hora <= 4)):
            if (slot_alicia == "alicia"):
                dispatcher.utter_message(template='utter_saludos_noches_conocer_nombre')
                print("saludos")
            else:
                dispatcher.utter_message(template='utter_saludos_noches')
        else:
            dispatcher.utter_message(template='utter_saludos_normal')

        return[SlotSet("nombre_alicia", None)]
