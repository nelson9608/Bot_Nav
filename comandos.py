from config import *
import os, re, requests, queue
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse
import threading
import openai
from PIL import Image
from io import BytesIO


#Crear imagen con la AI   
def Bot_GPT_Img(string):
    # Configurar la API key de OpenAI
    openai.api_key = ai_token

    # Generar la imagen utilizando DALL-E
    response = openai.Image.create(
    prompt=string,
    n=1,
    size="512x512"
    )
    # Obtener la URL de la imagen generada
    image_url = response['data'][0]['url']

    # Descargar la imagen y mostrarla en Python
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    # Guardar la imagen en formato JPEG
    image.save("imagen_generada.jpg", "JPEG")
    return ('imagen_generada.jpg','adj')




#Contactar al creador
def AcercaDe(string):
    texto_x = '''
    Mi creador es YoandyC  
    '''
    return (texto_x, 'text')



#si esta vacio enviamos eco, de lo contrario el eco de la palabra
def Echo(string):
    if string == '?':
        return ('Estoy activo!!!', 'text')
    else:
        return (string, 'text')
      


# Mostrando los comandos disponibles
def Help(string):
    Ayuda = '''
    Los comandos disponibles son:\n
    /eco Comando para saber si el bot se encuentra activo.\n
    /ayuda Presenta esta ayuda.\n
    /contacto Muestra el contacto del diseñador.\n
    /reporte Crea un reporte de errores encontrados, o solicitudes al creador.\n
    /bot Realiza una pregunta al bot.\n 
    /botimg Crea una imagen con AI desde una descripción\n
    /web Busca una palabra, frase o dirección URL en la web devolviendo la página html asociada.\n
    /descarga Descarga un archivo desde una URL.\n
    Nota: No abusen que soy nuevo :)
    '''
    return (Ayuda, 'text')


#recordar una ayuda diferente a los usuarios claro... :)
def AdminHelp(string):
    Ayuda = '''
    Los comandos disponibles son:\n
    /eco Comando para saber si el bot se encuentra activo.\n
    /ayuda Presenta esta ayuda.\n
    /contacto Muestra el creador (solo con fines de pruebas).\n
    /reporte Agrega un reporte (solo con fines de pruebas).\n 
    /leer Lee los reportes echos por los usuarios.\n
    /bot Realiza una pregunta al bot.\n
    /botimg Crea una imagen con AI desde una descripción\n 
    /web Busca una palabra, frase o dirección URL en la web devolviendo la página html asociada.\n
    /descarga Descarga un archivo desde una URL.
    '''
    return (Ayuda, 'text')

     
    
#si esta vacio solicitamos entre algo y sugerimos con ayuda
#de lo contrario verificamos si es una url o solo texto
def Buscador(string):
    # Verificar si el parámetro está vacío
    if not string:
        return ("Debe ingresar una palabra, frase o URL.",'text')
    else:
        # Verificar si la entrada es una URL
        if string.startswith("http"):
            try:
                # Obtener el HTML de la URL
                response = requests.get(string)
                html = response.text
            except requests.exceptions.RequestException as e:
                # Manejar la excepción y retornar un mensaje al usuario
                return (f"No se pudo obtener la página web: {str(e)}",'text')
        else:
            # Realizar la búsqueda en Google
            query = string.replace(" ", "+")
            url = f"https://google.com/search?client=opera&q={query}"
            try:
                response = requests.get(url)
                html = response.text
            except requests.exceptions.RequestException as e:
                # Manejar la excepción y retornar un mensaje al usuario
                return (f"No se pudo realizar la búsqueda: {str(e)}",'text')

        # Modificar los enlaces de la página web
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a", href=True):
            if link["href"].startswith("http"):
                email_body = f"/web {link['href']}"
                link["href"] = f"mailto:{radr}?body={urllib.parse.quote(email_body)}"
            else:
                # Convertir URL relativa a completa
                base_url = "https://www.google.com"
                complete_url = urllib.parse.urljoin(base_url, link["href"])
                email_body = f"/web {complete_url}"
                link["href"] = f"mailto:{radr}?body={urllib.parse.quote(email_body)}"

    # Retornar la HTML resultante
    return (str(soup), 'html')
    
   
   
#Chat con la AI   
def Bot_GPT(string):
    openai.api_key = ai_token
    # llamada a la respuesta
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=string,
        max_tokens=1000,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return(response.choices[0].text,'text')

        

 
#Añadiendo el reporte
def Report(string):
    # Verificar si el archivo existe
    if not os.path.isfile("Reporte.txt"):
        # Si el archivo no existe, crearlo y agregar el texto
        with open("Reporte.txt", "w") as archivo:
            archivo.write(string)
    else:
        # Si el archivo existe, agregar el texto al final
        with open("Reporte.txt", "a") as archivo:
            archivo.write("\n\n" + string)
    return ('Reporte realizado con exito.', 'text')



#leer los reportes realizados
def Leer_Report(string):
    # Verificar si el archivo existe
    if os.path.isfile('Reporte.txt'):
    # Si el archivo existe, leer su contenido
        with open('Reporte.txt', 'r') as archivo:
            contenido = archivo.read()
            return (contenido, 'text')
            # Eliminar el archivo
            os.remove('Reporte.txt')
    else:
        # Si el archivo no existe, informarlo
        return ('No existe ningun reporte.', 'text')



#Descarga de archivos
def DescargaArchivo(string):
    if string=='?':
        return ('Debe ingresar una URL de descarga.','text')    
    else:
        respuesta = requests.head(string)
        if respuesta.status_code == 200:
            #print('El archivo existe')
            try:
                response = requests.get(string)
                file_name = string.split("/")[-1]
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                return (file_name,'adj')
            except requests.exceptions.RequestException as e:
                return(f'No se pudo descargar el archivo {file_name}\n Error:{str(e)}', 'text')
        else:
            return ('El archivo no existe', 'text')
        
 
 #Ejecutamos un Hilo por cada entrada de descarga
def run_DescargaArchivo(string):
    rda = Multihilos2(target=DescargaArchivo, args=(string,))
    rda.start()
    rda.join()
    return rda.result   


#Ejecutamos un Hilo por cada entrada de busqueda
def run_Buscador(string):
    rb = Multihilos2(target=Buscador, args=(string,))
    rb.start()
    rb.join()
    return rb.result
  
#Ejecutamos un Hilo por cada entrada de busqueda
def run_BotIMG(string):
    rbi = Multihilos2(target=Bot_GPT_Img, args=(string,))
    rbi.start()
    rbi.join()
    return rbi.result  
  



#Clase para crear multi tareas con hilos de ejecucion
class Multihilos2(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._result = None
        
    def run(self):
        self._result = self._target(*self._args)
        
    @property
    def result(self):
        return self._result
    

 
#Comanod para los usuarios       
commands = {
    '/contacto':AcercaDe,
    '/eco': Echo,
    '/ayuda': Help,
    '/reporte':Report,
    '/bot':Bot_GPT,
    '/botimg':run_BotIMG,
    '/descarga':run_DescargaArchivo
}

#Comando para los administradores
admincommand = {
    '/contacto':AcercaDe,
    '/eco': Echo,
    '/ayuda': AdminHelp,
    '/reporte':Report,
    '/leer':Leer_Report,
    '/web': run_Buscador,
    '/bot':Bot_GPT,
    '/botimg':run_BotIMG,
    '/descarga':run_DescargaArchivo
}