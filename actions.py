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
from funciones_strings import *
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
        'nosaber_covid' , 'sintomas_covid', 'numero_ambulancia',
        'prueba_covid', 'cuanto_tipo_prueba', 'ivermectina_sirve', 'calor_mata_virus', 'contraerdenuevo_despues_de_enfermarse',
        'mosquitos_infectar', 'cuanto_falta_para_vacuna_medicamento', 'cuanto_falta_para_vacuna_medicamento', 'tomar_medicinas',
        'tiempo_sobrevive_virus', 'algunos_sintomas', 'periodo_incubacion_virus', 'dias_para_presentar_sintomas', 'duracion_enfermedad',
        'como_saber_si_tengo_covid', 'asintomatico', 'post_tratamiento', 'primeros_sintomas', 'tiempo_prueba_negativo', 'lactancia',
        'prevencion', 'como_se_transmite_covid', 'virus_en_el_aire', 'alimentos_contagio', 'que_es_el_covid' , 'consultas_menores_de_edad',
        'consultas_costo', 'vulnerables','info_plasma','centros_de_salud', 'menores_enfermedad', 'cuanto_tiempo_aislado', 'que_alimentos_consumir',
        'ir_al_consultorio', 'diferenciar_resfriado', 'embarazo_covid' , 'aislamiento' , 'secuelas', 'temperatura', 'animales', 'usuario_curioso'
        ]

        if pregunta in lista_preguntas:
            dispatcher.utter_message(template=f'utter_{pregunta}')
            return [UserUtteranceReverted()]

        return []

class responderCHITCHAT(Action):

    def name(self) -> Text:
        return "actions_chitchat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función para responder preguntas frecuentes
        chitchat = tracker.latest_message['intent'].get('name')
        lista_chitchats = ['chitchat_quien_tecreo', 'chitchat_eres_ia'
        ]

        if chitchat in lista_chitchats:
            dispatcher.utter_message(template=f'utter_{chitchat}')
            return [UserUtteranceReverted()]

        return []

class ActionDefaultAskAffirmation(Action):
   """Asks for an affirmation of the intent if NLU threshold is not met."""

   def name(self):
       return "action_default_ask_affirmation"

   def __init__(self):
       self.intent_mappings = {}
       self.intent_mappings_whatsapp = {}
       # read the mapping from a csv and store it in a dictionary
       with open('intent_mapping.csv', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.intent_mappings[row[0]] = row[1]
       with open('intent_mapping_whatsapp.csv', newline='', encoding='utf-8') as file:
            csv_reader_2 = csv.reader(file)
            for row in csv_reader_2:
                self.intent_mappings_whatsapp[row[0]] = row[1]

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
           last_intent_name = tracker.latest_message['intent']['name']

           # get the prompt for the intent
           intent_prompt = self.intent_mappings[last_intent_name]
           intent_prompt_whatsapp = self.intent_mappings_whatsapp[last_intent_name]

           # Create the affirmation message and add two buttons to it.
           # Use '/<intent_name>' as payload to directly trigger '<intent_name>'
           # when the button is clicked.
           message = "Si tu pregunta fue '{}' escribe {}\nSi esa no era tu duda, por favor reformula tu pregunta con mas claridad 🙌🏻".format(intent_prompt, intent_prompt_whatsapp)
           dispatcher.utter_message(text=message)
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
                if len(tracker.get_slot("sintomas")) == 1:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    message = "Efectivamente, "+ sintoma_1 +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 1")
                    return[SlotSet("sintomas", None)]
                elif len(tracker.get_slot("sintomas")) == 2:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    message = "Si, "+ sintoma_1 +" y "+ sintoma_2 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 2")
                    return[SlotSet("sintomas", None)]
                elif len(tracker.get_slot("sintomas")) == 3:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    message = "Para aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +" y "+ sintoma_3 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 3")
                    return[SlotSet("sintomas", None)]
                elif len(tracker.get_slot("sintomas")) > 3:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    message = "Para aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +", "+ sintoma_3 +" y otros que nombraste, son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 4")
                    return[SlotSet("sintomas", None)]

            elif (tracker.get_slot("sintomas") != None) and (tracker.get_slot("familiares") != None):
                len_sintomas = len(tracker.get_slot("sintomas"))
                len_familiares = len(tracker.get_slot("familiares"))
                if (len_sintomas == 1) and (len_familiares == 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    familiar_1 = tracker.get_slot("familiares")[0]
                    message = "Lo siento mucho por tu "+ familiar_1 +" 😕 \nEfectivamente, "+ sintoma_1 +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 5")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 2) and (len(tracker.get_slot("familiares")) == 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    familiar_1 = tracker.get_slot("familiares")[0]
                    message = "Lo siento mucho por tu "+ familiar_1 +" 😕 \nSi, "+ sintoma_1 +" y "+ sintoma_2 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 6")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 3) and (len(tracker.get_slot("familiares")) == 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    familiar_1 = tracker.get_slot("familiares")[0]
                    message = "Lo siento mucho por tu "+ familiar_1 +" 😕 \nPara aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +" y "+ sintoma_3 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 7")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 2) and (len(tracker.get_slot("familiares")) > 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    message = "Lo siento mucho por tus familiares 😕 \nSi, "+ sintoma_1 +" y "+ sintoma_2 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 8")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 3) and (len(tracker.get_slot("familiares")) > 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    message = "Lo lamento mucho por tus familiares 😕 \nPara aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +" y "+ sintoma_3 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 9")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) > 3) and (len(tracker.get_slot("familiares")) > 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    message = "Lo lamento mucho por tus familiares 😕 \nPara aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +", "+ sintoma_3 +" y otros que nombraste, son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 10")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
            elif (tracker.get_slot("sintomas") == None) and (tracker.get_slot("familiares") == None) and (tracker.get_slot("no_sintomas") != None):
                if len(tracker.get_slot("no_sintomas")) == 1:
                    sintoma_aparte = tracker.get_slot("no_sintomas")[0]
                    message = "Heem, "+ sintoma_aparte+" no esta directamente relacionada con el COVID-19, pero si tienes sospechas de que podrias estar enfermo te puedo comunicar con un medico para que revise tu caso 👩🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 11")
                    if tracker.get_slot("familiares") != None:
                        return [SlotSet("no_sintomas", None)] + [SlotSet("familiares", None)]
                    else:
                        return [SlotSet("no_sintomas", None)]
                elif len(tracker.get_slot("no_sintomas")) > 1:
                    sintoma_aparte = tracker.get_slot("no_sintomas")[0]
                    message = "Heem, "+ sintoma_aparte+" y otros que nombraste no estan directamente relacionados con el COVID-19, pero si tienes sospechas de que podrias estar enfermo te puedo comunicar con un medico para que revise tu caso 👩🏽‍⚕️ \n¿Deseas agendar una consulta?"
                    buttons = [{'title': 'Si',
                                'payload': '/afirmar'},
                               {'title': 'No',
                                'payload': '/negar'}]
                    dispatcher.utter_message(text=message, buttons=buttons)
                    #print ("PRUEBA 12")
                    if tracker.get_slot("familiares") != None:
                        return [SlotSet("no_sintomas", None)] + [SlotSet("familiares", None)]
                    else:
                        return [SlotSet("no_sintomas", None)]
            else:
                message = "Que mal oir eso 😕 \nSi crees que podrias estar enfermo, puedo facilitarte una consulta gratuita con un medico en linea para que revise tu caso \n¿Deseas agendar una consulta?"
                buttons = [{'title': 'Si',
                            'payload': '/afirmar'},
                            {'title': 'No',
                            'payload': '/negar'}]
                dispatcher.utter_message(text=message, buttons=buttons)
                return[SlotSet("familiares", None)]
        else:

            if (tracker.get_slot("sintomas") != None) and (tracker.get_slot("familiares") == None):
                if len(tracker.get_slot("sintomas")) == 1:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    dispatcher.utter_message(text="Efectivamente, "+ sintoma_1 +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 1")
                    return[SlotSet("sintomas", None)]
                elif len(tracker.get_slot("sintomas")) == 2:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    dispatcher.utter_message(text="Si, "+ sintoma_1 +" y "+ sintoma_2 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 2")
                    return[SlotSet("sintomas", None)]
                elif len(tracker.get_slot("sintomas")) == 3:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    dispatcher.utter_message(text="Para aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +" y "+ sintoma_3 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 3")
                    return[SlotSet("sintomas", None)]
                elif len(tracker.get_slot("sintomas")) > 3:
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    dispatcher.utter_message(text="Para aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +", "+ sintoma_3 +" y otros que nombraste, son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 4")
                    return[SlotSet("sintomas", None)]

            elif (tracker.get_slot("sintomas") != None) and (tracker.get_slot("familiares") != None):
                len_sintomas = len(tracker.get_slot("sintomas"))
                len_familiares = len(tracker.get_slot("familiares"))
                if (len_sintomas == 1) and (len_familiares == 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    familiar_1 = tracker.get_slot("familiares")[0]
                    dispatcher.utter_message(text="Lo siento mucho por tu "+ familiar_1 +" 😕 \nEfectivamente, "+ sintoma_1 +" es un posible sintoma del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 5")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 2) and (len(tracker.get_slot("familiares")) == 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    familiar_1 = tracker.get_slot("familiares")[0]
                    dispatcher.utter_message(text="Lo siento mucho por tu "+ familiar_1 +" 😕 \nSi, "+ sintoma_1 +" y "+ sintoma_2 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 6")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 3) and (len(tracker.get_slot("familiares")) == 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    familiar_1 = tracker.get_slot("familiares")[0]
                    dispatcher.utter_message(text="Lo siento mucho por tu "+ familiar_1 +" 😕 \nPara aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +" y "+ sintoma_3 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 7")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 2) and (len(tracker.get_slot("familiares")) > 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    dispatcher.utter_message(text="Lo siento mucho por tus familiares 😕 \nSi, "+ sintoma_1 +" y "+ sintoma_2 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 8")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) == 3) and (len(tracker.get_slot("familiares")) > 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    dispatcher.utter_message(text="Lo lamento mucho por tus familiares 😕 \nPara aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +" y "+ sintoma_3 +" son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 9")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
                elif (len(tracker.get_slot("sintomas")) > 3) and (len(tracker.get_slot("familiares")) > 1):
                    sintoma_1 = tracker.get_slot("sintomas")[0]
                    sintoma_2 = tracker.get_slot("sintomas")[1]
                    sintoma_3 = tracker.get_slot("sintomas")[2]
                    dispatcher.utter_message(text="Lo lamento mucho por tus familiares 😕 \nPara aclararte la duda, "+ sintoma_1 +", "+ sintoma_2 +", "+ sintoma_3 +" y otros que nombraste, son posibles sintomas del COVID-19 \nPerdon pero no estoy autorizada para otorgarte un tratamiento o recomendarte medicamentos, sin embargo, te puedo facilitar una consulta gratuita con un medico en linea para que revise tu caso 👨🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 10")
                    return [SlotSet("sintomas", None)] + [SlotSet("familiares", None)]
            elif (tracker.get_slot("sintomas") == None) and (tracker.get_slot("familiares") == None) and (tracker.get_slot("no_sintomas") != None):
                if len(tracker.get_slot("no_sintomas")) == 1:
                    sintoma_aparte = tracker.get_slot("no_sintomas")[0]
                    dispatcher.utter_message(text="Heem, "+ sintoma_aparte+" no esta directamente relacionada con el COVID-19, pero si tienes sospechas de que podrias estar enfermo te puedo comunicar con un medico para que revise tu caso 👩🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 11")
                    if tracker.get_slot("familiares") != None:
                        return [SlotSet("no_sintomas", None)] + [SlotSet("familiares", None)]
                    else:
                        return [SlotSet("no_sintomas", None)]
                elif len(tracker.get_slot("no_sintomas")) > 1:
                    sintoma_aparte = tracker.get_slot("no_sintomas")[0]
                    dispatcher.utter_message(text="Heem, "+ sintoma_aparte+" y otros que nombraste no estan directamente relacionados con el COVID-19, pero si tienes sospechas de que podrias estar enfermo te puedo comunicar con un medico para que revise tu caso 👩🏽‍⚕️ \n¿Deseas agendar una consulta?")
                    #print ("PRUEBA 12")
                    if tracker.get_slot("familiares") != None:
                        return [SlotSet("no_sintomas", None)] + [SlotSet("familiares", None)]
                    else:
                        return [SlotSet("no_sintomas", None)]
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
            dispatcher.utter_message(text="Lo siento, solo puedo mostrar casos a nivel nacional 😕")
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
                    dispatcher.utter_message(text="En "+dict_departamento[v_dp]+" hay: \n*"+ str(casosConfirmados) +"* confirmados 🧪 \n*"+ str(cantFallecidos)+"* decesos 📉 \n*"+str(cantRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento/municipio o quieres volver al *menu*?")

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
                    dispatcher.utter_message(text="En Bolivia hay: \n \n*"+ str(nroConfirmados) +"* confirmados* 🧪 \n*"+ str(nroFallecidos)+"* decesos 📉 \n*"+str(nroRecuperados)+"* recuperados 💊" + "\n¿Quieres saber los *casos* de otro departamento/municipio o quieres volver al *menu*?")

            else:
                dispatcher.utter_message(template='utter_departamento_incorrecto')
            return[SlotSet("departamento", None)]

        elif tracker.get_slot("municipios") != None:
            url = 'https://raw.githubusercontent.com/mauforonda/casos-municipios/master/clean_data/2020-07-18.csv'
            webpage = urlopen(url)
            slot_municipios = tracker.get_slot("municipios").lower()
            df = pd.read_csv(webpage)
            ddf = pd.DataFrame(df)

            tabla_val = None

            for municipio in ddf['municipio']:
                if quitar_acentos(slot_municipios)==quitar_acentos(municipio.lower()):
                    tabla_val = municipio
                    casos_confirmados = ddf[ddf['municipio']==tabla_val]['confirmados'].item()
                    casos_recuperados = ddf[ddf['municipio']==tabla_val]['recuperados'].item()
                    cant_fallecidos = ddf[ddf['municipio']==tabla_val]['decesos'].item()

                    if tracker.get_latest_input_channel() == 'facebook':
                        dispatcher.utter_message(text=f'En {tabla_val} hay: \n{casos_confirmados} confirmados 🧪 \n{cant_fallecidos} decesos 📉 \n{casos_recuperados} recuperados 💊')
                        dispatcher.utter_message(template='utter_preguntarOtrosCasos')
                    else:
                        dispatcher.utter_message(text=f'En {tabla_val} hay: \n*{casos_confirmados}* confirmados 🧪 \n*{cant_fallecidos}* decesos 📉 \n*{casos_recuperados}* recuperados 💊\n¿Quieres saber los *casos* de otro departamento/municipio o quieres volver al *menu*?')

            if tabla_val == None:
                dispatcher.utter_message(template='utter_municipio_incorrecto')

            return[SlotSet("municipios", None)]

class fallback(Action):

    def name(self) -> Text:
        return "custom_action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función que retorna un saludo diferente según la hora del día
        dispatcher.utter_message(template='utter_default')
        return [UserUtteranceReverted()]
