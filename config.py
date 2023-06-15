import os 
radr = os.environ.get("BOTEMAIL") # direccion a utilizar para el bot
pwd = os.environ.get("PASS") # contraseña base64.b64encode
admin = os.environ.get("MIEMAIL") # direccion de quien administra el bot
ai_token = os.environ.get("OPENAI_KEY")#token de la AI
imapserver = "imap.gmail.com"  # servidor imap
smtpserver = "smtp.gmail.com"  # servidor smtp
smtpserverport = 587  # puerto tls smtp
check_freq = 15 #Frecuencia con la q se revisa la bandeja