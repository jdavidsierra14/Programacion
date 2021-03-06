from flask import Flask , render_template , request, make_response, session, url_for, redirect
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Llave_supermisteriosa"
@app.route("/", methods=["GET","POST"])
def inicio():
	"""
	Esta funcion es la de la pagina del inicio, donde el usuario ingresa sesion
	Se compone de dos formularios y dos botones, uno para iniciar sesion y otro para registrarse
	"""
	e= "Bienvenido a ChaTeo-Web"
	if request.method=="POST":
		usuario = request.form["Usuario"] #formulario de iniciar sesion 
		contrasena = request.form["contrasena"]
		
		usuario = usuario + "\n"
		contrasena = contrasena + "\n"
		
		archivo = open("usuarios.txt","r") 
		baseusuarios = archivo.readlines()
		
		archivo2 = open("contraseñas.txt","r")
		basecontraseña = archivo2.readlines()
		
		archivo.close()
		archivo2.close()
		
		 
		if usuario in baseusuarios:  #Busca que el usuario ingresado exista en archivo donde van todos los usuarios
			k = baseusuarios.index(usuario)  #El resulatado es la posicion donde se encuentra la constraseña del usuario digitado 
			if contrasena == basecontraseña[k]:
				session["usuario"] = request.form["Usuario"] #Si la constraseña coinciden se crea una sesion del usuario 
				archivo3 = open("Usuarios Conectados/Usuariosactivos.txt","a")
				archivo4 = open("Usuarios Conectados/Usuariosactivos.txt","r")
				base = archivo4.read().splitlines()
				archivo4.close()
				if  session["usuario"] not in base : 
					archivo3.write(session["usuario"]+"\n")
				archivo3.close()
				return redirect(url_for("menu"))
			else : 
				error = "Usuario y/o contraseña invalidos" 
				return render_template("base/cookie.html",e=e,login=False,error=error)
		else:
			if usuario not in baseusuarios or contrasena not in basecontraseña or usuario == "" or contrasena == "":
				error = "Usuario y/o contraseña invalidos" 
				return render_template("base/cookie.html",e=e,login=False,error=error)
	return render_template("base/cookie.html",e=e,login=False)

@app.route("/menu",methods=["GET","POST"])
def menu():
	"""
	Funcion donde se encuentra el menu donde el usuario escoge la opcion que desee.
	Lo que se encuentra aqui es cuando el usurio cierra sesion, elminando asi su nombre en el archivo de usuarios activos
	"""
	usuario = session["usuario"]
	if request.method == "POST" :
		if request.form["salir"] == "  Salir  ": #Si selecciona el boton de salir, la sesion del usuario se elimina
			archivo = open("Usuarios Conectados/Usuariosactivos.txt","r")
			base= archivo.read().splitlines()
			archivo.close()
			for i in base:
				if i == usuario:
					elemento = base.index(i)
					del base[elemento]     #Elimina el usuario del archivo usuario activos
					session.pop("usuario",None)
					archivo2= open("Usuarios Conectados/Usuariosactivos.txt","w")
					print(base)
					for a in base:
						archivo2.write(a+"\n")
					archivo2.close()
			return redirect(url_for("inicio"))
	return render_template("base/menu.html",usuario = usuario)




@app.route("/amigos",methods=["GET","POST"])
def amigos():
	"""
	Funcion donde te permite agregar los usuarios, en la funcion se abre el archivo del usuario que este en sesion y ademas cuando 
	envia una solicitud, su nombre aparecera en el archivo de solicitudes de quien desa agregar
	"""
	usuario= session["usuario"]
	archivo = open("Contactos/Contactos"+usuario+".txt","a") #Abre o crea el archivo con los contactos del usuario
	archivo2 = open("Contactos/Contactos"+usuario+".txt", "r")
	amigos1 = archivo2.read().splitlines()
	archivo2.close()
	archivo.close()
	if request.method =="POST":
		agregar = request.form["agregar"]  #formulario para agregar amigos 
		archivo= open("usuarios.txt", "r")
		baseusuarios = archivo.read().splitlines() 
		archivo.close()
		if agregar in baseusuarios and agregar != "": #Busca que el usuario que digito exista en archivo donde estan todos los usuarios del programa
			archivo3 = open("Solicitudes/solicitudes"+request.form["agregar"]+".txt","a")  #abre el archivo de solicitudes de quien se le va a agregar
			archivo4 = open("Solicitudes/solicitudes"+request.form["agregar"]+".txt","r")
			lectura = archivo4.read().splitlines() 
			archivo4.close()
			if usuario in lectura: #Verifica que no le se envie dos veces una solicitud sin responder
				error = "Ya has enviado una solicitud al usuario"
				return render_template("base/inicio.html", usuario = usuario,amigos1 = amigos1,error = error)
			else:
				if usuario in agregar:
					error = "No puedes enviar una solicitud a ti mismo "
					return render_template("base/inicio.html",usuario = usuario,error = error, amigos1 = amigos1)
				if agregar in amigos1:
					error= "Ya has agregado al usuario"
					return render_template("base/inicio.html",usuario = usuario,error = error, amigos1 = amigos1)
				if agregar not in lectura:
					archivo3.write(usuario+"\n")
					archivo3.close()
					enviado = "Se ha enviado la solicitud de amistad a " + request.form["agregar"]
					return render_template("base/inicio.html",usuario = usuario, amigos1 = amigos1,enviado = enviado)

		else:		
			if agregar == "":
				pass
			if agregar not in baseusuarios:
				error1 = "Usuario no existe"
				return render_template("base/inicio.html",amigos1 = amigos1, usuario = usuario, error1 = error1)
	return render_template("base/inicio.html", usuario = usuario,amigos1 = amigos1)

@app.route("/solicitudes", methods=["GET","POST"])
def solicitudes():
	"""
	Aqui apareceran las solicitudes que el usuario tenga pendiente
	"""
	usuario = session["usuario"]
	msj = "Solicitudes de "+usuario
	archivo2 = open("Solicitudes/solicitudes"+usuario+".txt","a")
	archivo = open("Solicitudes/solicitudes"+usuario+".txt","r")
	solicitudes = archivo.read().splitlines()
	archivo.close()
	archivo2.close()
	if request.method == "POST":
		for i in solicitudes:
			if request.form.get("boton_"+i,None) == "Aceptar" : #Si acepta la solicitud
				elemento = solicitudes.index(i)
				del solicitudes[elemento] #Elimina la solicitud
				archivo3= open("Contactos/Contactos"+usuario+".txt","a")
				archivo3.writelines(i+"\n") #Si acepta la solicitud agrega al usuario
				archivo3.close()
				archivo4= open("Solicitudes/solicitudes"+usuario+".txt","w")
				archivo5 = open("Contactos/Contactos"+i+".txt","a")
				archivo5.write(usuario+"\n")
				archivo5.close()
				for a in solicitudes:
					archivo4.write(a+"\n")
				archivo4.close()
			else:
				if request.form.get("boton_"+i,None) == "Rechazar": #Si rechaza la solicitud
					elemento = solicitudes.index(i)
					del solicitudes[elemento]
					archivo6 = open("Solicitudes/solicitudes"+usuario+".txt","w")
					for a in solicitudes:
						archivo6.write(a+"\n")
					archivo6.close()

		
	return render_template("base/solicitudes.html",solicitudes = solicitudes, msj = msj )



@app.route("/chats",methods=["GET","POST"])
def chats():
	"""
	El menu donde apareceran los amigos conectado o desconectados, una vez que el usuario desee enviarle un mensaje a un
	contacto, si el archivo no esta creado, lo crea. Si el archivo ya existe no vuelve a crear otro archivo con ese chat.	 
	"""
	usuario= session["usuario"]
	creacion = open("Contactos/Contactos"+usuario+".txt","a")
	creacion.close() 
	archivo = open("Contactos/Contactos"+usuario+".txt","r")
	amigos= archivo.read().splitlines()
	archivo.close()
	archivo2 = open("Usuarios Conectados/Usuariosactivos.txt","r")
	conectados=archivo2.read().splitlines()
	archivo2.close()
	lista= [] #lista conectados 
	lista2 = [] #lista no conectados
	for i in conectados: #Revisa la lista de conectados 
		for  a in amigos:
			if i == a: # compara la lista de amigos con los usuarios conectados
				lista.append(a)
			else:
				if a not in conectados and a not in lista2:
					lista2.append(a)
	if request.method=="POST":
		for i in lista :
			if request.form.get("boton_"+i,None) == "Enviar mensaje":
				ruta = os.path.expanduser('~')
				path = ruta+"/Desktop/Flask/flaskr/Chats" #Busca los archivos de la carpeta chats
				base = os.listdir(path)
				contador = 0 
				for a in base :  #empieza a recorrer todos los archivos de la ruta seleccionada
					buscador= a.count(i)	#empieza a buscar cuantas veces se encuentra el concato 
					buscador2 = a.count(usuario)
					if buscador == 1 and buscador2 ==1:  #si no encuentra un archivo donde no se encuentren los dos 
						contador +=1
				if contador == 0: 
					archivo3= open("Chats/Chat-"+usuario+"x"+i+"-.txt","a") #Va a crear un solo archivo para el chat de esos dos usuarios
					archivo3.close()
					verificacion = os.path.isdir(ruta+"/Desktop/Flask/flaskr/static/upload/Chat"+usuario+"-"+i)
					if verificacion == False:
						os.mkdir(ruta+"/Desktop/Flask/flaskr/static/upload/Chat"+usuario+"-"+i)	
				session["amigo"] = i #se crea la sesion de ese usuario para el chat	
				return(redirect(url_for("chatAmigos")))
		for a in lista2:
			if request.form.get("boton_"+a,None)== "Enviar mensaje":
				ruta = os.path.expanduser('~')
				path = ruta+"/Desktop/Flask/flaskr/Chats"
				base = os.listdir(path)
				contador = 0
				for m in base :
					buscador= m.count(a)
					buscador2 = m.count(usuario)
					if buscador == 1 and buscador2 ==1:  #si no encuentra un archivo donde no se encuentren los dos 
						contador +=1
				if contador == 0: 
					archivo3= open("Chats/Chat-"+usuario+"x"+a+"-.txt","a") #Va a crear un solo archivo para el chat de esos dos usuarios
					archivo3.close()
					verificacion = os.path.isdir(ruta+"/Desktop/Flask/flaskr/static/upload/Chat"+usuario+"-"+a)
					if verificacion == False:
						os.mkdir(ruta+"/Desktop/Flask/flaskr/static/upload/Chat"+usuario+"-"+a)	
				session["amigo"] = a #se crea la sesion de ese usuario para el chat	
				return(redirect(url_for("chatAmigos")))
	return render_template("base/chats.html", usuario = usuario,conectados= conectados,lista=lista,lista2=lista2)


@app.route("/chatAmigos",methods=["GET","POST"])
def chatAmigos():
	"""
	Pagina donde se encuentra el chat. Se selecciona el archivo que le pertenece al usuario en sesion y de su contacto
	Cada mensaje se va modificando el archivo de chat del respectivo usuario con su contacto
	"""
	usuario = session["usuario"]
	amigo = session["amigo"]
	ahora= time.strftime("%c")
	ruta = os.path.expanduser('~')
	path = ruta+"/Desktop/Flask/flaskr/Chats"
	imagenes = ruta+"/Desktop/Flask/flaskr/static/upload"
	archivo = os.listdir(path)
	for a in archivo:		#Busca en la carpeta de chats
		buscador= a.count(amigo)	#Busca el archivo de chat que le pertenece 
		buscador2 = a.count(usuario)
		if buscador >= 1 and buscador2 >=1: # si el nombre del usuario y del contacto es mayor es 1 en los dos es porque ese es el archivo que le pertenece
			archivo2 = open("Chats/"+a,"r")
			chat = archivo2.read().splitlines()
			archivo2.close()
			if request.method == "POST":
				if request.form["enviar"] == "Enviar Mensaje" :
						msj = request.form["Mensajes"] #envio de mensajes
						if msj != "":
							archivo3 = open("Chats/"+a,"a")
							archivo3.write(time.strftime("%b,%d ,%H:%M")+"  "+ usuario +":"+"  "+ msj+"\n")
							archivo3.close()
							archivo4 = open("Chats/"+a,"r") # "a" es el archivo que se encontro mas arriba en el codigo con el for
							chat = archivo4.read().splitlines()
							archivo4.close()
	return render_template("base/chatsAmigos.html",usuario = usuario,chat = chat,amigo = amigo)
@app.route("/imagenes",methods=["GET","POST"])
def imagenes():
	usuario = session["usuario"]
	amigo = session["amigo"]
	ruta = os.path.expanduser('~')
	imagenes = ruta+"/Desktop/Flask/flaskr/static/upload"
	imagenes2 = os.listdir(imagenes)
	for img in imagenes2:
		busqueda = img.count(amigo)
		busqueda2 = img.count(usuario)
		if busqueda >=1 and busqueda2 >=1:
			imagenes3 = ruta+"/Desktop/Flask/flaskr/static/upload/"+img
	app.config["imagenes3"] = imagenes3	
	if request.method == "POST":
		if request.form["imagen"] == "Enviar Imagen" :
			if 'file' not in request.files:
				return redirect(request.url)
			if request.files["file"] == "":
				return redirect(request.url)
			file = request.files['file']

			if file.filename == "":
				redirect(request.url)

			filename = secure_filename(file.filename)
			destination = "/".join([imagenes3, filename])
			file.save(destination)
			ruta = os.path.expanduser('~')
			path = ruta+"/Desktop/Flask/flaskr/Chats"
			archivo = os.listdir(path)
			for a in archivo:		#Busca en la carpeta de chats
				buscador= a.count(amigo)	#Busca el archivo de chat que le pertenece 
				buscador2 = a.count(usuario)
				if buscador >= 1 and buscador2 >=1: # si el nombre del usuario y del contacto es mayor es 1 en los dos es porque ese es el archivo que le pertenece
					archivo2 = open("Chats/"+a,"a")
					chat = archivo2.write(time.strftime("%b,%d ,%H:%M")+"  "+ usuario +":"+"  "+ destination+"\n")
					archivo2.close()
			return redirect(url_for("chatAmigos"))
	return render_template("base/imagenes.html")

@app.route("/registro", methods=["GET","POST"])
def registro():
	"""
	Funcion donde puede registrarse el usuario. Una vez registrado, su nombre usuario pasa a un archivo donde se encuentran
	todos los usuarios que esten registrados
	"""
	if request.method=="POST":
		if request.form["Usuario"] == "" or request.form["contrasena"] == "": #Verifica que los campos del registro no sean vacios
			error1="Ingrese datos validos"
			return render_template("base/cookie.html",error1 = error1,login=True)
		else:
			if request.form["Usuario"] != "" and request.form["contrasena"] != "":
				usuarios=request.form["Usuario"]
				contrasena=request.form["contrasena"]
				usuarios = usuarios + "\n" 
				contrasena = contrasena  + "\n" 
				archivo = open("usuarios.txt","a")
				archivo2 = open("contraseñas.txt", "a")
				verificacion = open("usuarios.txt","r")
				verificacion2 = verificacion.readlines() 
				verificacion.close()
				if usuarios in verificacion2: #Verifica si el usuario ya existes
					error = "Usuario ya existe"
					return render_template("base/cookie.html",error = error, login= True )
				else:
					archivo.write(usuarios) #Registra el usuario
					archivo2.write(contrasena) #Registra su contraseña 
					aceptado = "Usuario registrado excitosamente"
					archivo.close()	
					archivo2.close()
					return render_template("base/cookie.html",login=True,aceptado=aceptado)	
	return render_template("base/cookie.html",login=True)
	
if __name__ == "__main__":
    app.run (debug = True, port=1000)

