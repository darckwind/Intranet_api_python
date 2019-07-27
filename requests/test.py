import requests
from bs4 import BeautifulSoup
import json

login = "https://intranet.ufro.cl/autentifica.php"

notas ="https://intranet.ufro.cl/alumno/notas/ver_notas_sem.php"

deudas = "https://intranet.ufro.cl/alumno/ver_deudas.php"

horario ="https://intranet.ufro.cl/alumno/ver_horario.php"

rut ="***********"
password="***********"


session =requests.Session()

payload_login = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; " \
                "name=\"Formulario[POPUSERNAME]\"\r\n\r\n"+rut+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
                "form-data; name=\"Formulario[XYZ]\"\r\n\r\n"+password+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

headers = {'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"}

# this art is for login on intranet

response_lo = session.request("POST", login, data=payload_login, headers=headers)

# this is for recover asignatures

#print(response_lo.status_code)

responce_notas = session.request('GET', notas)

parce_asignaturas = BeautifulSoup(responce_notas.content,'html.parser')
tablas = parce_asignaturas.findAll("table", {"class": "TablaEstandar"})

td =  tablas[0].findAll("td")

general = {}
codigo =""
ramo =""
asignaturas = {}

for tds in td:
    if not tds.get_text().startswith(('1', '\t')):
        if not tds.findAll("a",{"class": "link_normal"}):
            ramo =tds.get_text()
        if tds.findAll("a",{"class": "link_normal"}):
            a = tds.findAll("a",{"class": "link_normal"})
            if a[0].get_text() !="":
                codigo= a[0].get_text()

    asignaturas[codigo] = ramo

general['asignaturas']=asignaturas

#print(json.dumps(general))

#this is for recover financial data

responce_deudas = session.request('GET', deudas)
parce_deudas = BeautifulSoup(responce_deudas.content,'html.parser')
table_deudas = parce_deudas.findAll("table", {"class": "TablaEstandar"})
td_deudas = table_deudas[1].findAll("td")

deudas = {}
c_data = ""
c_monto = ""

for td_deudas in td_deudas:
    if td_deudas.get_text() != "2019":
        if td_deudas.get_text().startswith(('C')):
            c_data= td_deudas.get_text()
        else:
            c_monto= td_deudas.get_text()
    deudas[c_data] = c_monto

general['deudas']=deudas

#this is for recover horirio data

response__horario = session.request('GET', horario)
table_hor = BeautifulSoup(response__horario.content,'html.parser')
table_hor = table_hor.findAll("table", {"class": "Normal"})

data_horario = {}
data = {}
periodo = ""
count=0

#print(table_hor[1].find_all('td'))
for hor in table_hor[1].find_all('td'):
    if hor.get_text().startswith('Alm') or hor.get_text().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        periodo = hor.get_text()
    else:
        data[count] = hor.get_text()
        count +=1
        if count > 6:
            count = 0
    data_horario[periodo] = data


general['horario']=data_horario

print(json.dumps(general,indent=4))