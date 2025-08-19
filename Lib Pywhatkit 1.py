# importamos el modulo
import pywhatkit 
   
# utilizaremos controles de excepciones
try: 
     
  # enviando mensaje al receptor
  # usando pywhatkit 
  pywhatkit.sendwhatmsg("+524493697103",  
                        "Hola desde Mi Diario Python",  
                        16, 45) 
  print("Envio Exitoso!") 
   
except: 
     
  # manejo de excepcion
  # e impresion del error
  print("Ha ocurrido un error!")