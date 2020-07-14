from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from fechaHora import *
import csv
import pandas as pd


class saludar(Action):

    def name(self) -> Text:
        return "actions_saludar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        print("saludos")
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
            else:
                dispatcher.utter_message(template='utter_saludos_dias')
        elif (hora >= 12) and (hora <= 17):
            if (slot_alicia == "alicia"):
                dispatcher.utter_message(template='utter_saludos_tardes_conocer_nombre')
            else:
                dispatcher.utter_message(template='utter_saludos_tardes')
        elif ((hora >= 18) and (hora <= 23)) or ((hora >= 0) and (hora <= 4)):
            if (slot_alicia == "alicia"):
                dispatcher.utter_message(template='utter_saludos_noches_conocer_nombre')
            else:
                dispatcher.utter_message(template='utter_saludos_noches')
        else:
            dispatcher.utter_message(template='utter_saludos_normal')

        return[SlotSet("nombre_alicia", None)]

class ActionDefaultAskAffirmation(Action):
   """Asks for an affirmation of the intent if NLU threshold is not met."""

   def name(self):
       return "action_default_ask_affirmation"

   def __init__(self):
       self.intent_mappings = {}
       # read the mapping from a csv and store it in a dictionary
       with open('intent_mapping.csv', newline='', encoding='utf-8') as file:
           csv_reader = csv.reader(file)
           for row in csv_reader:
               self.intent_mappings[row[0]] = row[1]

   def run(self, dispatcher, tracker, domain):
       # get the most likely intent
       last_intent_name = tracker.latest_message['intent']['name']

       # get the prompt for the intent
       intent_prompt = self.intent_mappings[last_intent_name]

       # Create the affirmation message and add two buttons to it.
       # Use '/<intent_name>' as payload to directly trigger '<intent_name>'
       # when the button is clicked.
       message = "Lo siento, intentaste decir '{}'?".format(intent_prompt)
       buttons = [{'title': 'Si',
                   'payload': '/{}'.format(last_intent_name)},
                  {'title': 'No',
                   'payload': '/out_of_scope'}]
       dispatcher.utter_message(text=message, buttons=buttons)

       return []

class estoyEnfermo(Action):

    def name(self) -> Text:
        return "actions_enfermedad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        if tracker.get_latest_input_channel() == 'facebook':
            return []
        else:
            if (tracker.get_slot("sintomas") != None) and (tracker.get_slot("familiares") == None):
                sintoma = tracker.get_slot("sintomas")
                dispatcher.utter_message(text="Efectivamente, "+ sintoma +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                return[SlotSet("sintomas", None)]
            elif (tracker.get_slot("sintomas") == None) and (tracker.get_slot("familiares") != None):
                familiar = tracker.get_slot("familiares")
                dispatcher.utter_message(text="Lo siento mucho por tu "+ familiar +" 😕 \nLastimosamente, no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                return[SlotSet("familiares", None)]
            elif (tracker.get_slot("sintomas") != None) and (tracker.get_slot("familiares") != None):
                sintoma = tracker.get_slot("sintomas")
                familiar = tracker.get_slot("familiares")
                dispatcher.utter_message(text="Lo siento mucho por tu "+ familiar +" 😕 \nEfectivamente, "+ sintoma +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                return[SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
            else:
                dispatcher.utter_message(text="Que mal oir eso 😕 \nSi crees que podrias estar enfermo, puedo facilitarte una consulta gratuita con un medico en linea para que revise tu caso \n¿Deseas agendar una consulta?")
                return[SlotSet("familiares", None)]
        return []
