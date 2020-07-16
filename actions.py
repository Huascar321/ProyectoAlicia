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

class responderFAQ(Action):

    def name(self) -> Text:
        return "actions_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función para responder preguntas frecuentes
        pregunta = tracker.latest_message['intent'].get('name')
        lista_preguntas = ['porque_sintomas_yosolo_familia', 'porque_variosdias_sintomas_nocurar', 'dioxidocloro_ayuda',
        'nosaber_covid', 'nomejora_hospital', 'medico_atendio_seguimiento', 'sintomas_covid', 'numero_ambulancia',
        'prueba_covid', 'cuanto_tipo_prueba', 'ivermectina_sirve', 'calor_mata_virus', 'contraerdenuevo_despues_de_enfermarse',
        'mosquitos_infectar', 'cuanto_falta_para_vacuna_medicamento', 'cuanto_falta_para_vacuna_medicamento', 'tomar_medicinas',
        'tiempo_sobrevive_virus', 'algunos_sintomas', 'periodo_incubacion_virus', 'dias_para_presentar_sintomas', 'duracion_enfermedad',
        'como_saber_si_tengo_covid', 'asintomatico', 'post_tratamiento', 'primeros_sintomas', 'tiempo_prueba_negativo', 'lactancia',
        'prevencion', 'como_se_transmite_covid', 'virus_en_el_aire', 'alimentos_contagio', 'que_es_el_covid'
        ]

        if pregunta in lista_preguntas:
            dispatcher.utter_message(template=f'utter_{pregunta}')
            return [UserUtteranceReverted()]

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
                       'payload': '/reformular'}]
           dispatcher.utter_message(text=message, buttons=buttons)
       else:
           dispatcher.utter_message(template='utter_reformular')
       return []

class estoyEnfermo(Action):

    def name(self) -> Text:
        return "actions_enfermedad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        if tracker.get_latest_input_channel() == 'facebook':
            if (tracker.get_slot("sintomas") != None) and (tracker.get_slot("familiares") == None):
                sintoma = tracker.get_slot("sintomas")
                dispatcher.utter_message(text="Efectivamente, "+ sintoma +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                return[SlotSet("sintomas", None)]
            elif (tracker.get_slot("no_sintomas") != None):
                sintoma_aparte = tracker.get_slot("no_sintomas")
                dispatcher.utter_message(Text=sintoma_aparte+" no esta directamente relacionada con el COVID-19, pero si tienes sospechas de que podrias estar enfermo te puedo comunicar con un medico para que revise tu caso \n¿Deseas agendar una consulta?")
                return[SlotSet("no_sintomas", None)]
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
        else:
            if (tracker.get_slot("sintomas") != None) and (tracker.get_slot("familiares") == None):
                sintoma = tracker.get_slot("sintomas")
                dispatcher.utter_message(text="Efectivamente, "+ sintoma +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                return[SlotSet("sintomas", None)]
            elif (tracker.get_slot("no_sintomas") != None):
                sintoma_aparte = tracker.get_slot("no_sintomas")
                dispatcher.utter_message(text="Heem, "+ sintoma_aparte+" no esta directamente relacionada con el COVID-19, pero si tienes sospechas de que podrias estar enfermo te puedo comunicar con un medico para que revise tu caso 👩🏽‍⚕️ \n¿Deseas agendar una consulta?")
                return[SlotSet("no_sintomas", None)]
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

        if tracker.get_slot("paises") != None:
            dispatcher.utter_message(text="Lo siento, solo puedo mostrar casos en departamentos 😕")
            return [UserUtteranceReverted()] + [SlotSet("paises", None)]

        elif tracker.get_slot("departamento") != None:
            url = 'https://raw.githubusercontent.com/mauforonda/covid19-bolivia/master/total.csv'
            webpage = urlopen(url)
            v_dp = tracker.get_slot("departamento").lower()
            df = pd.read_csv(webpage)
            ddf = pd.DataFrame(df)
            dict_departamento = {
                'la paz': 'La Paz',
                'santa cruz': 'Santa Cruz',
                'cochabamba': 'Cochabamba',
                'oruro': 'Oruro',
                'potosi': 'Potosí',
                'tarija': 'Tarija',
                'chuquisaca': 'Chuquisaca',
                'beni': 'Beni',
                'pando': 'Pando'
            }

            if v_dp in dict_departamento:
                casosConfirmados = ddf[ddf['Province/State']==dict_departamento[v_dp]]['Confirmed'].item()
                cantFallecidos = ddf[ddf['Province/State']==dict_departamento[v_dp]]['Deaths'].item()
                cantRecuperados = ddf[ddf['Province/State']==dict_departamento[v_dp]]['Recovered'].item()

                if tracker.get_latest_input_channel() == 'facebook':
                    dispatcher.utter_message(text="En "+dict_departamento[v_dp]+" hay: \n"+ str(casosConfirmados) +" confirmados 🧪 \n"+ str(cantFallecidos)+" decesos 📉 \n"+str(cantRecuperados)+" recuperados 💊")
                    dispatcher.utter_message(template='utter_preguntarOtrosCasos')

                else:
                    dispatcher.utter_message(text="En "+dict_departamento[v_dp]+" hay: \n*"+ str(casosConfirmados) +"* confirmados* 🧪 \n*"+ str(cantFallecidos)+"* decesos 📉 \n*"+str(cantRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento o tienes otra *pregunta*?")

            elif v_dp == 'bolivia':
                nroConfirmados = 0
                nroFallecidos = 0
                nroRecuperados = 0
                for dpto in dict_departamento.values():
                    nroConfirmados += ddf[ddf['Province/State']==dpto]['Confirmed'].item()
                    nroFallecidos += ddf[ddf['Province/State']==dpto]['Deaths'].item()
                    nroRecuperados += ddf[ddf['Province/State']==dpto]['Recovered'].item()
                if tracker.get_latest_input_channel() == 'facebook':
                    dispatcher.utter_message(text="En Bolivia hay: \n"+ str(nroConfirmados) +" confirmados 🧪 \n"+ str(nroFallecidos)+" decesos 📉 \n"+str(nroRecuperados)+" recuperados 💊")
                    dispatcher.utter_message(template='utter_preguntarOtrosCasos')

                else:
                    dispatcher.utter_message(text="En Bolivia hay: \n \n*"+ str(nroConfirmados) +"* confirmados* 🧪 \n*"+ str(nroFallecidos)+"* decesos 📉 \n*"+str(nroRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento o tienes otra *pregunta*?")

            else:
                dispatcher.utter_message(template='utter_departamento_incorrecto')

        return[SlotSet("departamento", None)]

class fallback(Action):

    def name(self) -> Text:
        return "custom_action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        dispatcher.utter_message(template='utter_default')
        return [UserUtteranceReverted()]
