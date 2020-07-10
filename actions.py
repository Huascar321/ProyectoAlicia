
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
import json
from rasa_sdk.events import SlotSet
from urllib.request import urlopen
from fechaHora import *
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)

INTENT_DESCRIPTION_MAPPING_PATH = "intent_description_mapping.csv"

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

class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv(INTENT_DESCRIPTION_MAPPING_PATH)
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if len(intent_ranking) > 1:
            diff_intent_confidence = intent_ranking[0].get(
                "confidence"
            ) - intent_ranking[1].get("confidence")
            if diff_intent_confidence < 0.2:
                intent_ranking = intent_ranking[:2]
            else:
                intent_ranking = intent_ranking[:1]

        # for the intent name used to retrieve the button title, we either use
        # the name of the name of the "main" intent, or if it's an intent that triggers
        # the response selector, we use the full retrieval intent name so that we
        # can distinguish between the different sub intents
        first_intent_names = [
            intent.get("name", "")
            if intent.get("name", "") not in ["out_of_scope", "faq", "chitchat"]
            else tracker.latest_message.get("response_selector")
            .get(intent.get("name", ""))
            .get("full_retrieval_intent")
            for intent in intent_ranking
        ]

        message_title = (
            "Lo siento, no te entendí muy bien, intentaste decir...?"
        )

        entities = tracker.latest_message.get("entities", [])
        entities = {e["entity"]: e["value"] for e in entities}

        entities_json = json.dumps(entities)

        buttons = []
        for intent in first_intent_names:
            button_title = self.get_button_title(intent, entities)
            if "/" in intent:
                # here we use the button title as the payload as well, because you
                # can't force a response selector sub intent, so we need NLU to parse
                # that correctly
                buttons.append({"title": button_title, "payload": button_title})
            else:
                buttons.append(
                    {"title": button_title, "payload": f"/{intent}{entities_json}"}
                )

        buttons.append({"title": "Otra cosa", "payload": "/trigger_rephrase"})

        dispatcher.utter_message(text=message_title, buttons=buttons)

        return []

    def get_button_title(self, intent: Text, entities: Dict[Text, Text]) -> Text:
        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (self.intent_mappings.entities == entities.keys()) & (
            default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent

        return button_title.format(**entities)

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # Fallback caused by TwoStageFallbackPolicy
        if (
            len(tracker.events) >= 4
            and tracker.events[-4].get("name") == "action_default_ask_affirmation"
        ):

            dispatcher.utter_message(template="utter_restart_with_button")

            return [SlotSet("feedback_value", "negative"), ConversationPaused()]

        # Fallback caused by Core
        else:
            dispatcher.utter_message(template="utter_default")
            return [UserUtteranceReverted()]
