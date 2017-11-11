from flask import Flask , render_template , request, make_response, session, url_for, redirect

app = Flask(__name__)
app.secret_key = "Llave_supermisteriosa"
@app.route("/", methods=["GET","POST"])
def inicio():
	e= "Bienvenido a ChaTeo-Web"
	if request.method=="POST":
		usuario = request.form["Usuario"]
		contrasena = request.form["contrasena"]
		
		usuario = usuario + "\n"
		contrasena = contrasena + "\n"
		
		archivo = open("usuarios.txt","r") 
		baseusuarios = archivo.readlines()
		
		archivo2 = open("contraseñas.txt","r")
		basecontraseña = archivo2.readlines()
		
		archivo.close()
		archivo2.close()
		
		 
		if usuario in baseusuarios:
			k = baseusuarios.index(usuario)
			if contrasena == basecontraseña[k]:
				session["usuario"] = request.form["Usuario"]
				archivo3 = open("Usuarios Conectados/Usuariosactivos.txt","a")
				archivo3.write(session["usuario"]+"\n")
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
	usuario = session["usuario"]
	if request.method == "POST" :
		if request.form["Salir"] == "salir":
			archivo = open("Usuarios Conectados/Usuariosactivos.txt","r")
			usuarios= archivo.read().splitlines()
			archivo.close()
			for i in usuarios:
				if i == usuarios:
					elemento = usuarios.index(i)
					del usuarios[elemento]
					session.pop("usuario",None)
					archivo2= open("Usuario Contactos/Usuariosactivos.txt","a")
					for a in usuarios:
						archivo2.write(a+"\n")
					archivo2.close()
			return render_template("base/menu.html",usuario = usuario)
	return render_template("base/menu.html",usuario = usuario)




@app.route("/amigos",methods=["GET","POST"])
def amigos():
	usuario= session["usuario"]
	archivo = open("Contactos/Contactos"+usuario+".txt","a")
	archivo2 = open("Contactos/Contactos"+usuario+".txt", "r")
	amigos1 = archivo2.read().splitlines()
	archivo2.close()
	archivo.close()
	if request.method =="POST":
		agregar = request.form["agregar"]
		archivo= open("usuarios.txt", "r")
		baseusuarios = archivo.read().splitlines()
		archivo.close()
		if agregar in baseusuarios and agregar != "":
			archivo3 = open("Solicitudes/solicitudes"+request.form["agregar"]+".txt","a")
			archivo4 = open("Solicitudes/solicitudes"+request.form["agregar"]+".txt","r")
			lectura = archivo4.read().splitlines() 
			archivo4.close()
			if usuario in lectura:
				error = "Ya has enviado una solicitud al usuario"
				return render_template("base/inicio.html", usuario = usuario,amigos1 = amigos1,error = error)
			else:
				if agregar in amigos1:
					error= "Ya has agregado al usuario"
					return render_template("base/inicio.html",usuario = usuario,error = error, amigos1 = amigos1)
				if agregar not in lectura:
					archivo3.write(usuario+"\n")
					archivo3.close()
					enviado = "Se ha enviado la solicitud de amistad a " + request.form["agregar"]
					return render_template("base/inicio.html",usuario = usuario, amigos1 = amigos1,enviado = enviado)
				if agregar in lectura:
					error = "No puedes enviarte una solicitud a ti mismo "
		else:
			if agregar == "":
				pass
			if agregar not in baseusuarios:
				error1 = "Usuario no existe"
				return render_template("base/inicio.html",amigos1 = amigos1, usuario = usuario, error1 = error1)
	return render_template("base/inicio.html", usuario = usuario,amigos1 = amigos1)

@app.route("/solicitudes", methods=["GET","POST"])
def solicitudes():
	usuario = session["usuario"]
	msj = "Solicitudes de "+usuario
	archivo2 = open("Solicitudes/solicitudes"+usuario+".txt","a")
	archivo = open("Solicitudes/solicitudes"+usuario+".txt","r")
	solicitudes = archivo.read().splitlines()
	archivo.close()
	archivo2.close()
	if request.method == "POST":
		for i in solicitudes:
			if request.form.get("boton_"+i,None) == "Aceptar" :
				elemento = solicitudes.index(i)
				del solicitudes[elemento]
				archivo3= open("Contactos/Contactos"+usuario+".txt","a")
				archivo3.writelines(i)
				archivo3.close()
				archivo4= open("Solicitudes/solicitudes"+usuario+".txt","w")
				archivo5 = open("Contactos/Contactos"+i+".txt","a")
				archivo5.write(usuario+"\n")
				archivo5.close()
				for a in solicitudes:
					print(solicitudes)
					archivo4.write(a+"\n")
				archivo4.close()
	
				#return render_template("base/solicitudes.html",solicitudes = solicitudes, msj = msj )		
	return render_template("base/solicitudes.html",solicitudes = solicitudes, msj = msj )



@app.route("/chats")
def chats():
	usuario= session["usuario"]
	archivo = open("Contactos/Contactos"+usuario+".txt","r")
	amigos= archivo.read().splitlines()
	archivo.close()
	archivo2 = open("Usuarios Conectados/Usuariosactivos.txt","r")
	conectados=archivo2.read().splitlines()
	archivo2.close()
	lista= []
	for i in conectados:
		for a in amigos:
			if i == a:
				lista.append(a)
	
	return render_template("base/chats.html",conectados= conectados,amigos=amigos,lista=lista)
	




@app.route("/registro", methods=["GET","POST"])
def registro():
	if request.method=="POST":
		if request.form["Usuario"] == "" or request.form["contrasena"] == "":
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
				if usuarios in verificacion2:
					error = "Usuario ya existe"
					return render_template("base/cookie.html",error = error, login= True )
				else:
					archivo.write(usuarios) #Registra el usuario
					archivo2.write(contrasena)
					aceptado = "Usuario registrado excitosamente"
					archivo.close()	
					archivo2.close()
					return render_template("base/cookie.html",login=True,aceptado=aceptado)	
	return render_template("base/cookie.html",login=True)
	
if __name__ == "__main__":
    app.run (debug = True, port=1000)

