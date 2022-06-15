
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import xlwt
import tkinter as tk
from tkinter import messagebox
import statistics

# Tkinter GUI, just for task checking purposes

window = tk.Tk()
window.title("Viviendas de Cerdanyola")
window.pack_propagate(False)
window.geometry("450x253")
bg=tk.PhotoImage(file="fraskitowers.png")
label1 = tk.Label(window, image = bg)
label1.place(x = 0,y = 0)

# One function for each city

def Cerdanyola():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.idealista.com',
        'Sec-Fetch-Dest': 'document',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

    headers = {k: str(v).encode("utf-8") for k, v in headers.items()}  # Encode en UTF-8

    # Data that will be on the output dataframe

    precios = []
    calles = []
    enlaces = []
    descripciones = []
    media = []
    moda = []
    metros_finales = []
    # media_m2 = [] De momento descartada
    siguiente = True
    pagina = 1

    while siguiente:
        time.sleep(1)
        base_url = f"https://www.idealista.com/venta-viviendas/cerdanyola-del-valles-barcelona/pagina-{pagina}.htm?ordenado-por=precios-asc"
        web = requests.get(base_url, headers=headers)
        soup = bs(web.content, 'html.parser')

        precio = soup.findAll("span", attrs={"class", "item-price h2-simulated"})
        calle = soup.findAll("a", attrs={"class", "item-link"})
        enlace = soup.findAll("a", attrs={"class", "item-link", "href", "/inmueble*"})  # Enlace del inmueble
        descrip = soup.findAll("div", attrs={"class", "item-description description"})
        metros = soup.findAll("span", attrs={"class", "item-detail"})
        seguir = soup.findAll("a", attrs={"class", "icon-arrow-right-after"})


        if len(seguir) == 0:  # If there's no next page, it stops the loop.

            siguiente=False

        print(f"Vuelta {pagina}") # Page check

        for i in precio:  # First converts the price into string, removes dots, then it converts it into a float.
            new_precio = str(i.contents[0])
            new_precio2 = new_precio.replace(".", "")
            new_precio2 = float(new_precio2)
            precios.append(new_precio2)

        for j in calle:
            new_calle = str(j.contents)
            calles.append(new_calle)

        for p in enlace:
            new_enlace = "www.idealista.com"
            new_enlace += str(p['href'])
            enlaces.append(new_enlace)

        for result in descrip:  # If it does not find any description, adds a default row to make the data rows match.

            try:
                meaning = result.find(class_="ellipsis")
                descripciones.append(meaning.text)

            except:
                descripciones.append("Sin descripción")

        # Cleans useless symbols from descriptions.

        signo1 = "["
        signo2 = "]"
        calles = [s.replace(signo1, "") for s in calles]
        calles = [s.replace(signo2, "") for s in calles]

        try:   #Makes corrections on description content, if there's no description, it just pass.

            for i in descripciones:
                descripciones = [s.replace(signo1, "") for s in descripciones]
                descripciones = [s.replace(signo2, "") for s in descripciones]
                descripciones = [s.replace('\\n', "") for s in descripciones]

        except:
            pass

        # Loop to get m2 tag. Double loop since it needs to be separated from useless data inside "metros".
        for item in metros:

            for i in item:
                item2 = str(i).strip(' ') #Strip spaces from each "item-detail"
                if len(item2) ==3: # If it has 3 numbers its a valid m2 value.
                    metros_finales.append(int(item2))
                elif len(item2)==2:
                    if int(item2)>25:  # Filter needed to avoid getting 2 rows from very big houses because they have 10 or more rooms.
                        metros_finales.append(int(item2))
        pagina += 1

    #Mean and mode for prices. Then, converted to dataframe.

    mediahecha = round(statistics.mean(precios), 2)
    modahecha = statistics.mode(precios)
    # Append to lists
    media.append(mediahecha)
    moda.append(modahecha)

    #metros_media = round(statistics.mean(metros_finales))
    #media_m2.append(metros_media)
    #media_m2frame = pd.DataFrame({'Media m2':media_2})
    # Makes them a DataFrame
    modaframe = pd.DataFrame({'Moda': moda})
    mediaframe = pd.DataFrame({'Media': media})
    # Resets index.
    modaframe = modaframe.reset_index()
    mediaframe = mediaframe.reset_index()
    # Turns m2 into a DataFrame
    metros_frame = pd.DataFrame({'m2':metros_finales})
    metros_frame.reset_index()
    #Crafts the main dataframe
    viviendas = pd.DataFrame({'Precio': precios, 'Calle': calles, 'Enlace': enlaces, 'Descripciones':descripciones})
    viviendas.reset_index()
    # Crafts the final DataFrame with all the previous ones merged, turns it into a .xls
    viviendas_finales = [viviendas, metros_frame, modaframe, mediaframe]
    archivo_viviendas = pd.concat(viviendas_finales, axis=1)
    del archivo_viviendas['index'] #Deletes index column
    archivo_viviendas.to_excel('CerdanyolaViviendasTotales.xls')

# ----------------------------- Badia del Vallès ------------------------ #

def Badia():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.idealista.com',
        'Sec-Fetch-Dest': 'document',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

    headers = {k: str(v).encode("utf-8") for k, v in headers.items()}  # Encode en UTF-8

    # Data that will be on the output dataframe

    precios = []
    calles = []
    enlaces = []
    descripciones = []
    media = []
    moda = []
    metros_finales = []
    # media_m2 = [] De momento descartada
    siguiente = True
    pagina = 1

    while siguiente:
        time.sleep(1)
        base_url = f"https://www.idealista.com/venta-viviendas/badia-del-valles-barcelona/pagina-{pagina}.htm?ordenado-por=precios-asc"
        web = requests.get(base_url, headers=headers)
        soup = bs(web.content, 'html.parser')

        precio = soup.findAll("span", attrs={"class", "item-price h2-simulated"})
        calle = soup.findAll("a", attrs={"class", "item-link"})
        enlace = soup.findAll("a", attrs={"class", "item-link", "href", "/inmueble*"})  # Enlace del inmueble
        descrip = soup.findAll("div", attrs={"class", "item-description description"})
        metros = soup.findAll("span", attrs={"class", "item-detail"})
        seguir = soup.findAll("a", attrs={"class", "icon-arrow-right-after"})

        if len(seguir) == 0:  # If there's no next page, it stops the loop.

            siguiente = False

        print(f"Vuelta {pagina}")  # Page check

        for i in precio:  # First converts the price into string, removes dots, then it converts it into a float.
            new_precio = str(i.contents[0])
            new_precio2 = new_precio.replace(".", "")
            new_precio2 = float(new_precio2)
            precios.append(new_precio2)

        for j in calle:
            new_calle = str(j.contents)
            calles.append(new_calle)

        for p in enlace:
            new_enlace = "www.idealista.com"
            new_enlace += str(p['href'])
            enlaces.append(new_enlace)

        for result in descrip:  # If it does not find any description, adds a default row to make the data rows match.

            try:
                meaning = result.find(class_="ellipsis")
                descripciones.append(meaning.text)

            except:
                descripciones.append("Sin descripción")

        # Cleans useless symbols from descriptions.

        signo1 = "["
        signo2 = "]"
        calles = [s.replace(signo1, "") for s in calles]
        calles = [s.replace(signo2, "") for s in calles]

        try:  # Makes corrections on description content, if there's no description, it just pass.

            for i in descripciones:
                descripciones = [s.replace(signo1, "") for s in descripciones]
                descripciones = [s.replace(signo2, "") for s in descripciones]
                descripciones = [s.replace('\\n', "") for s in descripciones]

        except:
            pass

        # Loop to get m2 tag. Double loop since it needs to be separated from useless data inside "metros".
        for item in metros:

            for i in item:
                item2 = str(i).strip(' ')  # Strip spaces from each "item-detail"
                if len(item2) == 3:  # If it has 3 numbers its a valid m2 value.
                    metros_finales.append(int(item2))
                elif len(item2) == 2:
                    if int(item2) > 25:  # Filter needed to avoid getting 2 rows from very big houses because they have 10 or more rooms.
                        metros_finales.append(int(item2))
        pagina += 1

    # Mean and mode for prices. Then, converted to dataframe.

    mediahecha = round(statistics.mean(precios), 2)
    modahecha = statistics.mode(precios)
    # Append to lists
    media.append(mediahecha)
    moda.append(modahecha)

    # metros_media = round(statistics.mean(metros_finales))
    # media_m2.append(metros_media)
    # media_m2frame = pd.DataFrame({'Media m2':media_2})
    # Makes them a DataFrame
    modaframe = pd.DataFrame({'Moda': moda})
    mediaframe = pd.DataFrame({'Media': media})
    # Resets index.
    modaframe = modaframe.reset_index()
    mediaframe = mediaframe.reset_index()
    # Turns m2 into a DataFrame
    metros_frame = pd.DataFrame({'m2': metros_finales})
    metros_frame.reset_index()
    # Crafts the main dataframe
    viviendas = pd.DataFrame({'Precio': precios, 'Calle': calles, 'Enlace': enlaces, 'Descripciones': descripciones})
    viviendas.reset_index()
    # Crafts the final DataFrame with all the previous ones merged, turns it into a .xls
    viviendas_finales = [viviendas, metros_frame, modaframe, mediaframe]
    archivo_viviendas = pd.concat(viviendas_finales, axis=1)
    del archivo_viviendas['index']  # Deletes index column
    archivo_viviendas.to_excel('BadiaViviendasTotales.xls')

# ----------------------------- Barberà del Vallès --------------------------- #

def Barbera():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.idealista.com',
        'Sec-Fetch-Dest': 'document',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

    headers = {k: str(v).encode("utf-8") for k, v in headers.items()}  # Encode en UTF-8

    # Data that will be on the output dataframe

    precios = []
    calles = []
    enlaces = []
    descripciones = []
    media = []
    moda = []
    metros_finales = []
    # media_m2 = [] De momento descartada
    siguiente = True
    pagina = 1

    while siguiente:
        time.sleep(1)
        base_url = f"https://www.idealista.com/venta-viviendas/barbera-del-valles-barcelona/pagina-{pagina}.htm?ordenado-por=precios-asc"
        web = requests.get(base_url, headers=headers)
        soup = bs(web.content, 'html.parser')

        precio = soup.findAll("span", attrs={"class", "item-price h2-simulated"})
        calle = soup.findAll("a", attrs={"class", "item-link"})
        enlace = soup.findAll("a", attrs={"class", "item-link", "href", "/inmueble*"})  # Enlace del inmueble
        descrip = soup.findAll("div", attrs={"class", "item-description description"})
        metros = soup.findAll("span", attrs={"class", "item-detail"})
        seguir = soup.findAll("a", attrs={"class", "icon-arrow-right-after"})

        if len(seguir) == 0:  # If there's no next page, it stops the loop.

            siguiente = False

        print(f"Vuelta {pagina}")  # Page check

        for i in precio:  # First converts the price into string, removes dots, then it converts it into a float.
            new_precio = str(i.contents[0])
            new_precio2 = new_precio.replace(".", "")
            new_precio2 = float(new_precio2)
            precios.append(new_precio2)

        for j in calle:
            new_calle = str(j.contents)
            calles.append(new_calle)

        for p in enlace:
            new_enlace = "www.idealista.com"
            new_enlace += str(p['href'])
            enlaces.append(new_enlace)

        for result in descrip:  # If it does not find any description, adds a default row to make the data rows match.

            try:
                meaning = result.find(class_="ellipsis")
                descripciones.append(meaning.text)

            except:
                descripciones.append("Sin descripción")

        # Cleans useless symbols from descriptions.

        signo1 = "["
        signo2 = "]"
        calles = [s.replace(signo1, "") for s in calles]
        calles = [s.replace(signo2, "") for s in calles]

        try:  # Makes corrections on description content, if there's no description, it just pass.

            for i in descripciones:
                descripciones = [s.replace(signo1, "") for s in descripciones]
                descripciones = [s.replace(signo2, "") for s in descripciones]
                descripciones = [s.replace('\\n', "") for s in descripciones]

        except:
            pass

        # Loop to get m2 tag. Double loop since it needs to be separated from useless data inside "metros".
        for item in metros:

            for i in item:
                item2 = str(i).strip(' ')  # Strip spaces from each "item-detail"
                if len(item2) == 3:  # If it has 3 numbers its a valid m2 value.
                    metros_finales.append(int(item2))
                elif len(item2) == 2:
                    if int(item2) > 25:  # Filter needed to avoid getting 2 rows from very big houses because they have 10 or more rooms.
                        metros_finales.append(int(item2))
        pagina += 1

    # Mean and mode for prices. Then, converted to dataframe.

    mediahecha = round(statistics.mean(precios), 2)
    modahecha = statistics.mode(precios)
    # Append to lists
    media.append(mediahecha)
    moda.append(modahecha)

    # metros_media = round(statistics.mean(metros_finales))
    # media_m2.append(metros_media)
    # media_m2frame = pd.DataFrame({'Media m2':media_2})
    # Makes them a DataFrame
    modaframe = pd.DataFrame({'Moda': moda})
    mediaframe = pd.DataFrame({'Media': media})
    # Resets index.
    modaframe = modaframe.reset_index()
    mediaframe = mediaframe.reset_index()
    # Turns m2 into a DataFrame
    metros_frame = pd.DataFrame({'m2': metros_finales})
    metros_frame.reset_index()
    # Crafts the main dataframe
    viviendas = pd.DataFrame({'Precio': precios, 'Calle': calles, 'Enlace': enlaces, 'Descripciones': descripciones})
    viviendas.reset_index()
    # Crafts the final DataFrame with all the previous ones merged, turns it into a .xls
    viviendas_finales = [viviendas, metros_frame, modaframe, mediaframe]
    archivo_viviendas = pd.concat(viviendas_finales, axis=1)
    del archivo_viviendas['index']  # Deletes index column
    archivo_viviendas.to_excel('BarberaViviendasTotales.xls')

# Gets the data one by one
Cerdanyola()
Badia()
Barbera()

messagebox.showinfo(title="Uwu", message="Viviendas descargadas, parguelas.")
window.mainloop()
