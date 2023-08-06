def validateFieldUsername(username):    
    misaludo = "{nombre}".format(nombre = username)
    saludando1 = misaludo.strip()
    saludando = saludando1.upper()
    return saludando