#from-import por defecto de rasa
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUttered
from rasa_sdk.events import FollowupAction, UserUtteranceReverted, AllSlotsReset
from rasa_sdk.events import ActionExecuted
#Nuevos
from fechaHora import *
#Librerias para usar csv
from urllib.request import urlopen
import json
import csv
import pandas as pd
from rasa_sdk.events import SlotSet

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
            dispatcher.utter_message(template='utter_saludos_dias')
        elif (hora >= 12) and (hora <= 17):
            dispatcher.utter_message(template='utter_saludos_tardes')
        elif ((hora >= 18) and (hora <= 23)) or ((hora >= 0) and (hora <= 4)):
            dispatcher.utter_message(template='utter_saludos_noches')
        else:
            dispatcher.utter_message(template='utter_saludos_normal')

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
                    dispatcher.utter_message(text="En Bolivia hay: *"+ str(nroConfirmados) +"* confirmados* 🧪, *"+ str(nroFallecidos)+"* decesos 📉 y *"+str(nroRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento o tienes otra *pregunta*?")

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
