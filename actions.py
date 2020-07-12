
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
import json
import logging
#from datetime import datetime
#import datetime
import requests
import csv
import pandas as pd
from rasa_sdk.events import SlotSet
from urllib.request import urlopen
from fechaHora import *
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    ActionExecuted,
    FollowupAction,
    UserUttered,
    ActionReverted,
    datetime,
    ReminderScheduled
)
global fallback_variable
fallback_variable = False
global fallback_contador
fallback_contador = 0

class saludar(Action):

    def name(self) -> Text:
        return "actions_saludar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día

        hora = horaActualInt()
        texto = ""

        print(fallback_variable)
        print(fallback_contador)
        if(hora >= 5) and (hora <= 11):
            if (tracker.get_slot("nombre_alicia") == "Alicia") or (tracker.get_slot("nombre_alicia") == "alicia"):
                dispatcher.utter_message(template='utter_saludos_dias_conocer_nombre')
            else:
                dispatcher.utter_message(template='utter_saludos_dias')
        elif (hora >= 12) and (hora <= 17):
            if (tracker.get_slot("nombre_alicia") == "Alicia") or (tracker.get_slot("nombre_alicia") == "alicia"):
                dispatcher.utter_message(template='utter_saludos_tardes_conocer_nombre')
            else:
                dispatcher.utter_message(template='utter_saludos_tardes')
        elif ((hora >= 18) and (hora <= 23)) or ((hora >= 0) and (hora <= 4)):
            if (tracker.get_slot("nombre_alicia") == "Alicia") or (tracker.get_slot("nombre_alicia") == "alicia"):
                dispatcher.utter_message(template='utter_saludos_noches_conocer_nombre')
            else:
                dispatcher.utter_message(template='utter_saludos_noches')
        else:
            dispatcher.utter_message(template='utter_saludos_normal')

        return[SlotSet("nombre_alicia", None)]

class mostrarCasos(Action):

    def name(self) -> Text:
        return "actions_mostrar_casos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna los casos de COVID-19 según el departamento

        if tracker.get_slot("departamento") != None:
            url = 'https://raw.githubusercontent.com/mauforonda/covid19-bolivia/master/total.csv'
            webpage = urlopen(url)
            v_dp = tracker.get_slot("departamento").lower()
            df = pd.read_csv(webpage)
            ddf = pd.DataFrame(df)
            listaDepartamento = ['La Paz', 'Santa Cruz', 'Cochabamba', 'Oruro', 'Potosí', 'Tarija', 'Chuquisaca', 'Beni', 'Pando']
            nombreDepartamento = -1

            if (v_dp == "la paz"):
                nombreDepartamento = 0
            elif (v_dp == "santa cruz"):
                nombreDepartamento = 1
            elif (v_dp == "cochabamba"):
                nombreDepartamento = 2
            elif (v_dp == "oruro"):
                nombreDepartamento = 3
            elif (v_dp == "potosi"):
                nombreDepartamento = 4
            elif (v_dp == "tarija"):
                nombreDepartamento = 5
            elif (v_dp == "chuquisaca"):
                nombreDepartamento = 6
            elif (v_dp == "beni"):
                nombreDepartamento = 7
            elif (v_dp == "pando"):
                nombreDepartamento = 8
            elif (v_dp == "bolivia"):
                nroConfirmados = 0
                nroFallecidos = 0
                nroRecuperados = 0
                for dpto in listaDepartamento:
                    nroConfirmados += ddf[ddf['Province/State']==dpto]['Confirmed'].item()
                    nroFallecidos += ddf[ddf['Province/State']==dpto]['Deaths'].item()
                    nroRecuperados += ddf[ddf['Province/State']==dpto]['Recovered'].item()
                if tracker.get_latest_input_channel() == 'facebook':
                    dispatcher.utter_message(text="En Bolivia hay: \n"+ str(nroConfirmados) +" confirmados 🧪 \n"+ str(nroFallecidos)+" decesos 📉 \n"+str(nroRecuperados)+" recuperados 💊")
                    dispatcher.utter_message(template='utter_preguntarOtrosCasos')

                else:
                    dispatcher.utter_message(text="En Bolivia hay: *"+ str(nroConfirmados) +"* confirmados* 🧪 \n*"+ str(nroFallecidos)+"* decesos 📉 \n*"+str(nroRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento o tienes otra *pregunta*?")

                return[SlotSet("departamento", None)]

            else:
                dispatcher.utter_message(template='utter_departamento_incorrecto')
                return[SlotSet("departamento", None)]


            casosConfirmados = ddf[ddf['Province/State']==listaDepartamento[nombreDepartamento]]['Confirmed'].item()
            cantFallecidos = ddf[ddf['Province/State']==listaDepartamento[nombreDepartamento]]['Deaths'].item()
            cantRecuperados = ddf[ddf['Province/State']==listaDepartamento[nombreDepartamento]]['Recovered'].item()

            if tracker.get_latest_input_channel() == 'facebook':
                dispatcher.utter_message(text="En "+listaDepartamento[nombreDepartamento]+" hay: \n"+ str(casosConfirmados) +" confirmados 🧪 \n"+ str(cantFallecidos)+" decesos 📉 \n"+str(cantRecuperados)+" recuperados 💊")
                dispatcher.utter_message(template='utter_preguntarOtrosCasos')

            else:
                dispatcher.utter_message(text="En "+listaDepartamento[nombreDepartamento]+" hay: *"+ str(casosConfirmados) +"* confirmados* 🧪, *"+ str(cantFallecidos)+"* decesos 📉 y *"+str(cantRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento o tienes otra *pregunta*?")

        return[SlotSet("departamento", None)]

class verificarCanal(Action):

    def name(self) -> Text:
        return "actions_verificarCanal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        if tracker.get_latest_input_channel() == 'facebook':
            dispatcher.utter_message(template='utter_desplegarMenu')
        return []

class activadorIntent(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_activador_intent"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        global fallback_variable
        global fallback_contador
        if tracker.get_latest_input_channel() == 'facebook':
            return []
        else:
            #if tracker.get_slot("fallback_slot") == True:
            if fallback_variable == True:

                date = datetime.datetime.now()
                entities = tracker.latest_message.get("entities")

                reminder = ReminderScheduled(
                    intent_fallback,
                    trigger_date_time=date,
                    entities=entities,
                    name="my_reminder",
                    kill_on_user_message=False,
                )
                fallback_variable = False
                fallback_contador -=1

                return [reminder]
        return []

class activadorRefrasear(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_activador_frasear"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        global fallback_variable
        global fallback_contador
        if tracker.get_latest_input_channel() == 'facebook':
            return []
        else:
            #if tracker.get_slot("fallback_slot") == True:
            if fallback_variable == True:

                date = datetime.datetime.now()
                entities = tracker.latest_message.get("entities")

                reminder = ReminderScheduled(
                    "trigger_rephrase",
                    trigger_date_time=date,
                    entities=entities,
                    name="my_reminder",
                    kill_on_user_message=False,
                )
                fallback_variable = False
                fallback_contador +=1

                return [reminder]
        return []

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

   def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       if tracker.get_latest_input_channel() == 'facebook':
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
           dispatcher.utter_button_message(message, buttons=buttons)
       else:
           global fallback_contador
           if fallback_contador ==2:
               # enviar la variable
               feedback = tracker.latest_message['text']
               print(feedback)

               dispatcher.utter_message(template='utter_disculpas')
               fallback_contador=0
               return []
           else:
               last_intent_name = tracker.latest_message['intent']['name']

               intent_prompt = self.intent_mappings[last_intent_name]

               message = "Lo siento, intentaste decir '{}'? \n \n• *Si* \n• *No*".format(intent_prompt)

               global intent_fallback
               intent_fallback = last_intent_name

               global fallback_variable

               fallback_variable = True
               fallback_contador += 1

               dispatcher.utter_message(text=message)

               return []

       return []
