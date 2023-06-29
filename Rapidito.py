from config import *
import smtplib


server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
server.login(radr,pwd)
server.sendmail('from_mail',admin, 'message')
server.quit()