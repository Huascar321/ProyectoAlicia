from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from urllib.request import urlopen
from rasa_sdk.events import (
    #datetime,
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    ActionExecuted,
    FollowupAction,
    UserUttered,
    ActionReverted,
    ReminderScheduled
)
from fechaHora import *
from mongodb import *
import csv
import pandas as pd

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
       if tracker.get_latest_input_channel() == 'facebook':
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
       else:
           if tracker.get_slot("fallback_slot2") == True:
               feedback = tracker.latest_message['text']
               new_feedback = {
                   'fecha' : fechaActual(),
                   'mensaje' : feedback
               }

               collection_feedback.insert_one(new_feedback)
               message = "Lo siento, tu pregunta no se encuentra en nuestra base de datos. \nSera enviada a revision y agregada en el futuro, mientras tanto. \nDime tu siguiente pregunta!"
               dispatcher.utter_message(text=message)
               return [FollowupAction('actions_slot_fallback')]
           last_intent_name = tracker.latest_message['intent']['name']

           intent_prompt = self.intent_mappings[last_intent_name]

           message = "Lo siento, intentaste decir '{}'? \n \n• *Si* \n• *No*".format(intent_prompt)

           global intent_fallback
           intent_fallback = last_intent_name

           dispatcher.utter_message(text=message)
           return [FollowupAction('actions_slot_fallback')]
       return []

class slotFallback(Action):

    def name(self) -> Text:
        return "actions_slot_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        if tracker.get_slot("fallback_slot2") == True:
            return [SlotSet("fallback_slot2", None)]
        if tracker.get_slot("fallback_slot") == None:
            return [SlotSet("fallback_slot", True)]

        return []

class afirmarFallback(Action):

    def name(self) -> Text:
        return "actions_afirmar_Fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        from rasa_sdk.events import datetime
        if tracker.get_slot("fallback_slot") == True:

            #date = datetime.datetime.now()
            date = datetime.datetime.now()
            entities = tracker.latest_message.get("entities")

            reminder = ReminderScheduled(
                intent_fallback,
                trigger_date_time=date,
                entities=entities,
                name="my_reminder",
                kill_on_user_message=False,
            )
            print("afirmar correcto")
            return [reminder] + [SlotSet("fallback_slot", None)] + [FollowupAction('action_listen')]
        return []

class negarFallback(Action):

    def name(self) -> Text:
        return "actions_negar_Fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        if tracker.get_slot("fallback_slot") == True:

            dispatcher.utter_message(template='utter_reformular')
            return [FollowupAction('action_listen')] + [SlotSet("fallback_slot", None), SlotSet("fallback_slot2", True)]
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
                    dispatcher.utter_message(text="En Bolivia hay: \n \n*"+ str(nroConfirmados) +"* confirmados* 🧪 \n*"+ str(nroFallecidos)+"* decesos 📉 \n*"+str(nroRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento o tienes otra *pregunta*?")

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
                dispatcher.utter_message(text="En "+listaDepartamento[nombreDepartamento]+" hay: \n*"+ str(casosConfirmados) +"* confirmados* 🧪 \n*"+ str(cantFallecidos)+"* decesos 📉 \n*"+str(cantRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento o tienes otra *pregunta*?")

        return[SlotSet("departamento", None)]

class fallback(Action):

    def name(self) -> Text:
        return "custom_action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        if tracker.get_slot("fallback_slot") == True:
            return []
        if tracker.get_slot("fallback_slot2") == True:
            feedback = tracker.latest_message['text']
            new_feedback = {
                'fecha' : fechaActual(),
                'mensaje' : feedback
            }

            collection_feedback.insert_one(new_feedback)
            message = "Lo siento, tu pregunta no se encuentra en nuestra base de datos \nSera enviada a revision y agregada en el futuro, mientras tanto. Dime tu siguiente pregunta!"
            dispatcher.utter_message(text=message)
            return [UserUtteranceReverted()] + [FollowupAction('actions_slot_fallback')]
        dispatcher.utter_message(template='utter_default')
        return [UserUtteranceReverted()]
