#Todo lo referente a fechas y horas
from datetime import datetime

def fechaActual(): #Retorna la fecha en formato YYYY-mm-dd
    rightNow = datetime.now()
    return rightNow.strftime("%Y-%m-%d")

def fechaHoraActual(): #Retorna la fecha en formato YYYY-mm-dd
    rightNow = datetime.now()
    return rightNow.strftime("%Y-%m-%d (%H:%M:%S)")

def horaActualInt(): #Retorna un entero de la hora actual (0-23)
    rightNow = datetime.now()
    return int(rightNow.strftime("%H"))
