#Todo lo referente a fechas y horas de Alicia
from datetime import datetime

rightNow = datetime.now()

def fechaActual(): #Retorna la fecha en formato YYYY-mm-dd
    return rightNow.strftime("%Y-%m-%d")

def fechaHoraActual(): #Retorna la fecha en formato YYYY-mm-dd
    return rightNow.strftime("%Y-%m-%d (%H:%M:%S)")

def horaActualInt(): #Retorna un entero de la hora actual (0-23)
    return int(dateTimeObj.strftime("%H"))
