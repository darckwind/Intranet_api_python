import requests
from bs4 import BeautifulSoup
import pandas as pd



class Requesteo():
    rut =""
    password =""

    def contructor(self, run, passwo):
        global rut,password
        rut = run
        password = passwo

        print(rut,password)

    @staticmethod
    def recover():


        login = "https://intranet.ufro.cl/autentifica.php"

        notas ="https://intranet.ufro.cl/alumno/notas/ver_notas_sem.php"

        deudas = "https://intranet.ufro.cl/alumno/ver_deudas.php"

        horario ="https://intranet.ufro.cl/alumno/ver_horario.php"




        session =requests.Session()

        payload_login = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; " \
                        "name=\"Formulario[POPUSERNAME]\"\r\n\r\n"+rut+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
                        "form-data; name=\"Formulario[XYZ]\"\r\n\r\n"+password+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

        headers = {'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"}

        # this art is for login on intranet

        session.request("POST", login, data=payload_login, headers=headers)

        # this is for recover asignatures

        responce_notas = session.request('GET', notas)

        parce_asignaturas = BeautifulSoup(responce_notas.content,'html.parser')
        tablas = parce_asignaturas.findAll("table", {"class": "TablaEstandar"})

        td = tablas[0].findAll("td")

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
        table = table_hor[1]

        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
        #print(df.to_dict())

        general['horario']=df.to_dict()

        return general