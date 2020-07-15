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
        if pregunta == "porque_sintomas_yosolo_familia":
            dispatcher.utter_message(template='utter_porque_sintomas_yosolo_familia')
            return [UserUtteranceReverted()]
        elif pregunta == "porque_variosdias_sintomas_nocurar":
            dispatcher.utter_message(template='utter_porque_variosdias_sintomas_nocurar')
            return [UserUtteranceReverted()]
        elif pregunta == "dioxidocloro_ayuda":
            dispatcher.utter_message(template='utter_dioxidocloro_ayuda')
            return [UserUtteranceReverted()]
        elif pregunta == "nosaber_covid":
            dispatcher.utter_message(template='utter_nosaber_covid')
            return [UserUtteranceReverted()]
        elif pregunta == "nomejora_hospital":
            dispatcher.utter_message(template='nomejora_hospital')
            return [UserUtteranceReverted()]
        elif pregunta == "medico_atendio_seguimiento":
            dispatcher.utter_message(template='utter_medico_atendio_seguimiento')
            return [UserUtteranceReverted()]
        elif pregunta == "sintomas_covid":
            dispatcher.utter_message(template='utter_sintomas_covid')
            return [UserUtteranceReverted()]
        elif pregunta == "numero_ambulancia":
            dispatcher.utter_message(template='utter_numero_ambulancia')
            return [UserUtteranceReverted()]
        elif pregunta == "prueba_covid":
            dispatcher.utter_message(template='utter_prueba_covid')
            return [UserUtteranceReverted()]
        elif pregunta == "cuanto_tipo_prueba":
            dispatcher.utter_message(template='utter_cuanto_tipo_prueba')
            return [UserUtteranceReverted()]
        elif pregunta == "ivermectina_sirve":
            dispatcher.utter_message(template='utter_ivermectina_sirve')
            return [UserUtteranceReverted()]
        elif pregunta == "calor_mata_virus":
            dispatcher.utter_message(template='utter_calor_mata_virus')
            return [UserUtteranceReverted()]
        elif pregunta == "contraerdenuevo_despues_de_enfermarse":
            dispatcher.utter_message(template='utter_contraerdenuevo_despues_de_enfermarse')
            return [UserUtteranceReverted()]
        elif pregunta == "mosquitos_infectar":
            dispatcher.utter_message(template='utter_mosquitos_infectar')
            return [UserUtteranceReverted()]
        elif pregunta == "cuanto_falta_para_vacuna_medicamento":
            dispatcher.utter_message(template='utter_cuanto_falta_para_vacuna_medicamento')
            return [UserUtteranceReverted()]
        elif pregunta == "cuanto_falta_para_vacuna_medicamento":
            dispatcher.utter_message(template='utter_cuanto_falta_para_vacuna_medicamento')
            return [UserUtteranceReverted()]
        elif pregunta == "tomar_medicinas":
            dispatcher.utter_message(template='utter_tomar_medicinas')
            return [UserUtteranceReverted()]
        elif pregunta == "tiempo_sobrevive_virus":
            dispatcher.utter_message(template='utter_tiempo_sobrevive_virus')
            return [UserUtteranceReverted()]
        elif pregunta == "algunos_sintomas":
            dispatcher.utter_message(template='utter_algunos_sintomas')
            return [UserUtteranceReverted()]
        elif pregunta == "periodo_incubacion_virus":
            dispatcher.utter_message(template='utter_periodo_incubacion_virus')
            return [UserUtteranceReverted()]
        elif pregunta == "dias_para_presentar_sintomas":
            dispatcher.utter_message(template='utter_dias_para_presentar_sintomas')
            return [UserUtteranceReverted()]
        elif pregunta == "duracion_enfermedad":
            dispatcher.utter_message(template='utter_duracion_enfermedad')
            return [UserUtteranceReverted()]
        elif pregunta == "como_saber_si_tengo_covid":
            dispatcher.utter_message(template='utter_como_saber_si_tengo_covid')
            return [UserUtteranceReverted()]
        elif pregunta == "asintomatico":
            dispatcher.utter_message(template='utter_asintomatico')
            return [UserUtteranceReverted()]
        elif pregunta == "post_tratamiento":
            dispatcher.utter_message(template='utter_post_tratamiento')
            return [UserUtteranceReverted()]
        elif pregunta == "primeros_sintomas":
            dispatcher.utter_message(template='utter_primeros_sintomas')
            return [UserUtteranceReverted()]
        elif pregunta == "tiempo_prueba_negativo":
            dispatcher.utter_message(template='utter_tiempo_prueba_negativo')
            return [UserUtteranceReverted()]
        elif pregunta == "lactancia":
            dispatcher.utter_message(template='utter_lactancia')
            return [UserUtteranceReverted()]
        elif pregunta == "prevencion":
            dispatcher.utter_message(template='utter_prevencion')
            return [UserUtteranceReverted()]
        elif pregunta == "como_se_transmite_covid":
            dispatcher.utter_message(template='utter_como_se_transmite_covid')
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
        dispatcher.utter_message(template='utter_default')
        return [UserUtteranceReverted()]
