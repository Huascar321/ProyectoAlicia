#from-import por defecto de rasa
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#Nuevos
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

        if(hora >= 5) and (hora <= 11):
            dispatcher.utter_message(template='utter_saludos_dias')
        elif (hora >= 12) and (hora <= 17):
            dispatcher.utter_message(template='utter_saludos_tardes')
        elif ((hora >= 18) and (hora <= 23)) or ((hora >= 0) and (hora <= 4)):
            dispatcher.utter_message(template='utter_saludos_noches')
        else:
            dispatcher.utter_message(template='utter_saludos_normal')

        return []

class menu_1(Action):

    def name(self) -> Text:
        return "actions_menu_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Función del menu
        message = tracker.latest_message.get('text')
        if(message == "4"):
            return [UserUttered("/" + quieroAyudar, {
                "intent": {"name": quieroAyudar, "confidence": 1.0},
                "entities": {}
            })]

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
            nombreDepartamento = ""

            if (v_dp == "la paz"):
                nombreDepartamento = "La Paz"
            elif (v_dp == "santa cruz"):
                nombreDepartamento = "Santa Cruz"
            elif (v_dp == "cochabamba"):
                nombreDepartamento = "Cochabamba"
            elif (v_dp == "oruro"):
                nombreDepartamento = "Oruro"
            elif (v_dp == "potosi"):
                nombreDepartamento = "Potosi"
            elif (v_dp == "tarija"):
                nombreDepartamento = "Tarija"
            elif (v_dp == "chuquisaca"):
                nombreDepartamento = "Chuquisaca"
            elif (v_dp == "beni"):
                nombreDepartamento = "Beni"
            elif (v_dp == "pando"):
                nombreDepartamento = "Pando"
            else:
                dispatcher.utter_message(text="Lo siento no entendí el departamento, intenta escribirlo bien 🙌")
                return[SlotSet("departamento", None)]


            casosConfirmados = ddf[ddf['Province/State']==nombreDepartamento]['Confirmed'].item()
            cantFallecidos = ddf[ddf['Province/State']==nombreDepartamento]['Deaths'].item()
            cantRecuperados = ddf[ddf['Province/State']==nombreDepartamento]['Recovered'].item()

            dispatcher.utter_message(text="En "+nombreDepartamento+" hay: \n*"+ str(casosConfirmados) +"* confirmados* ☑️ \n*"+ str(cantFallecidos)+"* decesos 📉 \n*"+str(cantRecuperados)+"* recuperados 💊")

        return[SlotSet("departamento", None)]
