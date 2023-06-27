from config import *
#from comandos import *
import imapclient, imaplib, pyzmail, smtplib, time, os, re
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.audio import  MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename

#del modulo comandos
#from config import *
import requests, queue, threading, openai, zipfile # os,re,time,
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO



# Ampliando la limitacion imap
imaplib._MAXLINE = 1000000
global cliente
global s
global i
# Crea una lista para almacenar los mensajes
conversation = []


#-----------MODULO COMANDOS--------MODULO COMANDOS--------------------------------------

#Crear imagen con la AI   
def Bot_GPT_Img(string):
    try:
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
    except:
        return ('No se pudo generar la imagen', 'txt')




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
    /descarga Descarga un archivo desde una URL.\n
    /descarga2 Descarga un archivo desde una URL dividiendolo en partes de 5Mb.
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
    
    # Agrega el mensaje a la conversación
    conversation.append(string)
    # Si la conversación tiene más de 20 mensajes
    # elimina el mensaje más antiguo
    if len(conversation) > 20:
        conversation.pop(0)
        
    # Concatena los mensajes anteriores para crear un contexto
    context = '\n'.join(conversation)
    
    # llamada a la respuesta
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=(f"{context}\n {string}\nBot:"),
        max_tokens=1000,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    # Agrega la respuesta a la conversación
    bot_response = response.choices[0].text.strip()
    conversation.append(bot_response)
    
    return(bot_response,'text')
    #return(response.choices[0].text,'text')

        

 
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
    if string == '?':
        return ('Debe ingresar una URL de descarga.', 'text')
    else:
        try:
            # Verificar si el archivo existe y cancelar si hay demora
            respuesta = requests.head(string, timeout=10)
            if respuesta.status_code == 200:
                # Archivo aceptado para descarga
                try:
                    # Descargar el archivo y cancelar si hay demora
                    response = requests.get(string)#,timeout=40
                    #response = urllib.requests.urlopen(string)
                    file_name = string.split("/")[-1]
                    with open(file_name, 'wb') as file:
                        file.write(response.content)
                    return (file_name, 'adj')
                except requests.exceptions.RequestException as e:
                    return (f'No se pudo descargar el archivo {file_name}n Error: {str(e)}', 'text')
                except requests.exceptions.Timeout:
                    return ('Error: Tiempo de espera excedido', 'text')
            else:
                return ('El archivo no existe', 'text')
        except requests.exceptions.Timeout:
            return ('Error: Tiempo de espera excedido', 'text')
        except requests.exceptions.RequestException:
            return ('Error al verificar el archivo', 'text')
        
 
 
 
 #-------------------------------------------------------------------
def DescargaArchivo2(string):
    print('Descarga2')
    print(f'es para {cliente}')
    aquien = cliente
    parts = []
    if string == '?':
        return ('Debe ingresar una URL de descarga.', 'text')
    else:
        try:
            print('Verificando la existencia del archivo...')
            # Verificar si el archivo existe y cancelar si hay demora
            respuesta = requests.head(string, timeout=10)
            if respuesta.status_code == 200:
                # Archivo aceptado para descarga
                return ('URL aceptada, Intentando descargar!!\nEsto puede demorar unos minutos sea paciente.','text')
                try:
                    print('Existe!!, Intentando descargar...')              
                    # Descargar el archivo y cancelar si hay demora
                    # Download the file from the URL
                    response = requests.get(string)
                    file_size = int(response.headers.get("Content-Length", 0))
                    file_name = string.split("/")[-1]
                    file_path = os.path.join(os.getcwd(), file_name)
                    with open(file_path, "wb") as f:
                        for data in response.iter_content(1024):
                            f.write(data)

                    # Compress the file into a zip file
                    zip_file_name = file_name.split(".")[0] + ".zip"
                    zip_file_path = os.path.join(os.getcwd(), zip_file_name)
                    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        if file_size < 10 * 1024 * 1024:
                            zip_file.write(file_path, file_name)
                        else:
                            part_num = 1
                            with open(file_path, "rb") as f:
                                while True:
                                    part_data = f.read(10 * 1024 * 1024)
                                    if not part_data:
                                        break
                                    part_file_name = f"{file_name}.part{part_num}"
                                    zip_file.writestr(part_file_name, part_data)
                                    part_num += 1
                                    parts.append(part_filename)
                            print('Dando salida')
                            print(parts)
                            MultiEnvio(parts, aquien)
                                
                except requests.exceptions.RequestException as e:
                    return (f'No se pudo descargar el archivo {file_name}n Error: {str(e)}', 'text')
                except requests.exceptions.Timeout:
                    return ('Error: Tiempo de espera excedido en la descarga', 'text')
            else:
                return ('El archivo no existe', 'text')
        except requests.exceptions.Timeout:
            return ('Error: Tiempo de espera excedido en la respuesta del sitio', 'text')
        except requests.exceptions.RequestException:
            return ('Error al verificar el archivo', 'text')
#---------------------------------------------------------------------------------------------
 
 
 
 
 
 
 #Ejecutamos un Hilo por cada entrada de descarga
def run_DescargaArchivo(string):
    rda = Multihilos2(target=DescargaArchivo, args=(string,))
    rda.start()
    rda.join()
    return rda.result   

 #este el de prueba
def run_DescargaArchivo2(string):
    rda = Multihilos2(target=DescargaArchivo2, args=(string,))
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
    
def Tiempo(string):
    return ('Mi primer retorno', 'text')
    time.sleep(5)
    return ('Retorno despues de dormir 5 seg', 'text')
 
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
    '/descarga':run_DescargaArchivo,
    '/descarga2':run_DescargaArchivo2,
    '/time':Tiempo
}

#---------TERMINA MODULO COMANDOS-------------------------------------------------------



def imap_init():
    global i
    i = imapclient.IMAPClient(imapserver)
    c = i.login(radr, pwd)
    i.select_folder('INBOX')


def smtp_init():
    global s
    s = smtplib.SMTP(smtpserver, smtpserverport,timeout=60)
    c = s.starttls()[0]
    if c != 220: # if c is not 220
        raise Exception('Conexion tls fallida: ' + str(c))
    c = s.login(radr, pwd)[0]
    if c != 235: # if c is not 235
        raise Exception('SMTP login fallido: ' + str(c))


def get_unread():
    i.select_folder('INBOX')
    uids = i.search(['UNSEEN'])
    if not uids:
        return None #no hay mensajes disponibles
    else:
        #print("Encontrados %s Sin leer" % len(uids))
        return i.fetch(uids, ['BODY[]', 'FLAGS']) #retornamos el mensaje y lo marco como leido


def mail(text, tipo):
    msg = MIMEMultipart()
    msg['From'] = radr
    msg['To'] = cliente
    msg['Subject'] = ""
    # print('mensaje saliente:'+ cliente)
    if tipo == 'text':
        msg_p = MIMEText(text, 'plain')
    elif tipo == 'multi':
        MultiEnvio(text, cliente)
        msg_p = MIMEText('Son todas las partes.\nYa puedes unirlas.', 'plain')
    elif tipo == 'html':
        msg_p = MIMEText(text, 'html')
        msg_p.add_header('content-disposition', 'attachment', filename='web_index.html')
    elif tipo == 'img':
        msg_p = MIMEText(text, 'plain')
        msg_p.add_header('content-disposition', 'attachment', filename=text)
    elif tipo == 'adj':
        archivo_adjunto = open(text, 'rb')
        msg_p = MIMEText('Archivo: '+text, 'html')
        msg_p = MIMEBase('application', "octet-stream")
        msg_p.set_payload(archivo_adjunto.read())
        encoders.encode_base64(msg_p)
        msg_p.add_header('Content-Disposition', 'attachment; filename="{}"'.format(basename(text)))
    elif tipo == 'pdf':
        with open(text, 'rb') as f:
            pdf_data = f.read()
        msg.attach(MIMEText('Encontrada la hoja de datos del: '+text, 'html'))#plain
        msg_p = MIMEApplication(pdf_data, Name=text)
        msg_p['Content-Disposition'] = f'attachment; filename={text}'
              
    msg.attach(msg_p)
    s.sendmail(radr, cliente, msg.as_string())
    s.close()
    #print('Enviado un ' +tipo+' a '+cliente )
    #print('contenido: '+text)
    if os.path.exists(text) and (tipo == 'adj'):
        os.remove(text)
    try:
        os.unlink(text)
    except:
        pass

#---------------------------------------------------------------------------
def MultiEnvio(files, user):   
    # Loop del multi envio
    for file in files:
        #creando el email
        msg = MIMEMultipart()
        msg['From'] = radr
        msg['To'] = cliente
        msg['Subject'] = ""
        msg.attach(MIMEText('Se supone es un texto'))

        # preparandolos
        with open(file, 'rb') as f:
            attachment = MIMEApplication(f.read())
            msg.attach(attachment)

        # enviandolo
        #with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        #    server.login(sender_email, password)
            
        s.sendmail(radr, cliente, msg.as_string())

        #print('Enviado un ' +tipo+' a '+cliente )
        #print('contenido: '+text)
        if os.path.exists(file):
            os.remove(file)
#---------------------------------------------------------------------------


def analyze_msg(raws, a):
    global cliente
    global cmd
    msg = pyzmail.PyzMessage.factory(raws[a][b'BODY[]'])
    frm = msg.get_addresses('from')
    cliente = frm[0][1]

    # Get text from message and remove signature
    text = msg.text_part.get_payload().decode(msg.text_part.charset)
    text = re.sub(r'--\s*\n.*', '', text, flags=re.DOTALL)

    # Extract command from text
    match = re.search(r'^/(\w+)', text.strip())
    if match:
        cmd = '/'+match.group(1)
        print(cmd)
        if frm[0][1] != admin:
            
            if cmd not in commands:
                return False
            else:
                try:
                    arg = text.split(' ', 1)[1]
                except IndexError:
                    arg = '?'
                return [cmd, arg]
        else:
            if cmd not in admincommand:
                return False
            else:
                try:
                    arg = text.split(' ', 1)[1]
                except IndexError:
                    arg = '?'
                return [cmd, arg]
    else:
        return False
    
    

"""def analyze_msg(raws, a):
    global cliente
    msg = pyzmail.PyzMessage.factory(raws[a][b'BODY[]'])
    frm = msg.get_addresses('from')
    cliente = frm[0][1] # obtenemos a quien responder la solicitud      
    #print(cliente)
    # Administracion del bot
    if frm[0][1] != admin:
        print('Cliente: '+cliente)
        text = msg.text_part.get_payload().decode(msg.text_part.charset)
        cmds = text.replace('\r\n', '').split(' ', 1)
        #print('Comando solicitado: '+cmds)
        if cmds[0] not in commands:
             #Para USUARIOS
             #verificando si existe el comando
            #print("El comando %s no es válido" % cmds[0])
            return False
        else: # si no hay accion asignamos un esacio de array
            try:
                cmds[1]
                return cmds
            except IndexError:
                cmds.append('?')
                return cmds
    else: #Para ADMIN
        #print('Admin: ' + admin)
        text = msg.text_part.get_payload().decode(msg.text_part.charset)
        cmds = text.replace('\r\n', '').split(' ', 1)
        if cmds[0] not in admincommand:
         #verificando si existe el comando
        #print("El comando %s no es válido" % cmds[0])
            return False
        else: # si no hay accion asignamos un esacio de array
            try:
                cmds[1]
                return cmds
            except IndexError:
                cmds.append('?')
                return cmds"""



if __name__ == '__main__':
    imap_init()
    print(f'Bot iniciado en ({radr})')
     

    
    
while True:  # Revicion constante
    print('En espera...')
    try:
        msgs = get_unread()
        while msgs is None:# si no hay esperamos un tiempo para revisar nuevamente
            time.sleep(check_freq)
            msgs = get_unread()#reintento
        for a in msgs.keys():
            if type(a) is not int:#Clasificarlo
                continue
            cmds = analyze_msg(msgs, a)#lo analizamos en busca e comandos
            if cmds is None:
                continue
            elif cmds is False:  # Comando no valido
                print('Comando no valido')
                Nota = 'Comando no valido\nEnvíe el comando /ayuda para ver una lista de los que se encuentran  disponibles.'
                smtp_init()
                mail(Nota, 'text') #enviamos un email de tipo texto"""
                continue            
            else:
                if cliente != admin: #Salida para los clientes
                    print('USER: '+cliente)
                    salida = commands[cmds[0]](cmds[1])
                    smtp_init()
                    mail(salida[0], salida[1])
                else: #salida para el admin
                    print('ADMIN')                    
                    print(cliente)
                    salida = admincommand[cmds[0]](cmds[1])
                    smtp_init()
                    mail(salida[0], salida[1])
                                   
    except OSError as e:
        print("Error de tipo:", type(e).__name__)
        time.sleep(30)
        imap_init()
        continue
    except smtplib.SMTPServerDisconnected:
        print("Re intento de conexion en breve")
        time.sleep(30)
        imap_init()
        continue
    