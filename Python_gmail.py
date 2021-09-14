import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from getpass import getpass
import pymysql
import sys
#///////////////////////////////////////////////////////////////////////////#
#Conexión a la base de datos
try:
    mydbd = pymysql.connect(
    host= 'b2wspwslqhwsx8gjmfdu-mysql.services.clever-cloud.com',
    user='uosyo14l4rzfw3k7',
    password='yDK96FLituORblDIMyjv',
    db='b2wspwslqhwsx8gjmfdu'
    )
except:
    print("Error al conectar la base de datos, por favor vuelva a intentar ")
    sys.exit(1)
#///////////////////////////////////////////////////////////////////////////#
#Conexión a gmail
#  Ingresar dato de usaurio 
username = input("Correo: ")
password = getpass("Password: ")
# Crear conexión
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# iniciar sesión
try:
    imap.login(username, password)
except:
    print("Error en usuario y/o contraseña, por favor vuelva a intentar ")
    sys.exit(1)
#///////////////////////////////////////////////////////////////////////////#
#Nos posiscionamos en la bandeja de entrada
imap.select("INBOX")
#Buscamos si hay correos que en el Subject traiga la palabra Devops y lo eliminamos
typ, data = imap.search(None, 'SUBJECT',"'devops'")
for num in data[0].split():
   imap.store(num, '+FLAGS', '\\Deleted')
#Buscamos la palabra Devops en el cuerpo del correo y sólo en los mensajes no leidos
typ, mensaje= imap.search(None, 'UNSEEN BODY', '"Devops"')
for i in mensaje[0].split():
    typ, mensaje = imap.fetch(i, '(RFC822)')
 #Extraemos el contenido del correo y decodificamos el contenido
    for respuesta in mensaje:
            if isinstance(respuesta, tuple):
                    # Obtener el contenido
                    mensaje = email.message_from_bytes(respuesta[1])
                    # decodificar el contenido
                    subject = decode_header(mensaje["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        # convertir a string
                        subject = subject.decode()
                    date= decode_header(mensaje["date"])[0][0]
                    # de donde viene el correo
                    from_= mensaje.get("From")
                    print(date)
                    print(from_)
                    print(subject)
#///////////////////////////////////////////////////////////////////////////#
     #Almacenamos los datos en la base mysql
    try:
        cursor1=mydbd.cursor()     
        query= f"INSERT INTO DevOps (fecha, email, asunto) VALUES (%s, %s, %s)" 
        val= (date,from_,subject)    
        cursor1.execute(query, val)
        mydbd.commit()
        print('Base de Datos actualizada, :) bonito día')
    except:
        print("Error al guardar la base de datos, por favor vuelva a intentar ")
        sys.exit(1)      
#////////////////////////////////////////////////////////////////////////////#
# Cerramos conexión y sesión        
imap.close()
imap.logout()
