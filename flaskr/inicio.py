from flask import Flask , render_template , request, make_response, session, url_for, redirect
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
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
				session["usuario"] = usuario
				return redirect(url_for("login"))
		else:
			if usuario not in baseusuarios or contrasena not in basecontraseña or usuario == "" or contrasena == "":
				error = "Usuario y/o contraseña invalidos" 
				return render_template("base/cookie.html",e=e,login=False,error=error)
		#archivo.close()
		#archivo2.close()
	return render_template("base/cookie.html",e=e,login=False)
@app.route("/login")
def login():
	usuario= session["usuario"]
	return render_template("base/inicio.html", usuario = usuario)


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
					archivo.write(usuarios)
					archivo2.write(contrasena)
					aceptado = "Usuario registrado excitosamente"
					archivo.close()	
					archivo2.close()
					return render_template("base/cookie.html",login=True,aceptado=aceptado)	
	return render_template("base/cookie.html",login=True)
	
if __name__ == "__main__":
    app.run (debug = True, port=1000)

