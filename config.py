import os 
radr = os.environ.get("BOTEMAIL") # direccion a utilizar para el bot
pwd = os.environ.get("PASS") # contraseña base64.b64encode
admin = os.environ.get("MIEMAIL") # direccion de quien administra el bot
ai_token = os.environ.get("OPENAI_KEY")#token de la AI
imapserver = "imap.zoho.com"  # servidor imap "imap.gmail.com"  "imap.zoho.com"
smtpserver = "smtp.zoho.com"  # servidor smtp "smtp.gmail.com"  "smtp.zoho.com"
smtpserverport = 587  # puerto tls smtp        587 gmail         465 zohomail 
imapserverport = 993  # puerto tls imap        25  gmail         993 zohomail
check_freq = 15 #Frecuencia con la q se revisa la bandeja