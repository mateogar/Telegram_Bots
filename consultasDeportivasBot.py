# -*- coding: utf-8 -*-
#author: Mateo García Fuentes

#Este bot funciona como una aplicación de resultados, clasificaciones ... Estoy usando la única API open data que hay sobre este tema (https://market.mashape.com/sportsop/soccer-sports-open-data) lo que limita bastante la funcionalidad del flujo, ya que esta API aún está en construcción. Por lo tanto hay operaciones que se pueden utilizar con algunos países y con otros no y viceversa.


import json
import sys
import unirest
import telepot
import time
import threading
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#Keyboard
paises = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='España', callback_data='España')],
					[InlineKeyboardButton(text='Inglaterra', callback_data='Inglaterra')],
					[InlineKeyboardButton(text='Italia', callback_data='Italia')],
					[InlineKeyboardButton(text='Holanda', callback_data='Holanda')],
               ])
opciones = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Clasificación', callback_data='Clasificación')],
                   	[InlineKeyboardButton(text='Partidos de un equipo', callback_data='Partidos de un equipo')],
                   	[InlineKeyboardButton(text='Volver atrás', callback_data='atras')],
                   	])
opcionesit = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Clasificación', callback_data='Clasificación')],
                   	[InlineKeyboardButton(text='Máximos goleadores', callback_data='Máximos goleadores')],
                   	[InlineKeyboardButton(text='Volver atrás', callback_data='atras')],
                   	])     
                   	
opcionesns = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Clasificación', callback_data='Clasificación')],
                   	[InlineKeyboardButton(text='Volver atrás', callback_data='atras')],
                   	])                
                   	
equipos = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Alavés', callback_data='alaves')],
					[InlineKeyboardButton(text='Athletic', callback_data='athletic')],
					[InlineKeyboardButton(text='Atl. Madrid', callback_data='atl_madrid')],
					[InlineKeyboardButton(text='Barcelona', callback_data='barcellona')],
					[InlineKeyboardButton(text='Betis', callback_data='betis_balompie')],
					[InlineKeyboardButton(text='Celta', callback_data='celta_vigo')],
					[InlineKeyboardButton(text='Deportivo', callback_data='deportivo')],
					[InlineKeyboardButton(text='Eibar', callback_data='eibar')],
					[InlineKeyboardButton(text='Espanyol', callback_data='espanyol')],
					[InlineKeyboardButton(text='Granada', callback_data='granada')],
					[InlineKeyboardButton(text='Las Palmas', callback_data='las_palmas')],
					[InlineKeyboardButton(text='Leganés', callback_data='leganes')],
					[InlineKeyboardButton(text='Málaga', callback_data='malaga')],
					[InlineKeyboardButton(text='Osasuna', callback_data='osasuna')],
					[InlineKeyboardButton(text='Real Madrid', callback_data='real_madrid')],
					[InlineKeyboardButton(text='Real Sociedad', callback_data='real_sociedad')],
					[InlineKeyboardButton(text='Sevilla', callback_data='siviglia')],
					[InlineKeyboardButton(text='Sporting de Gijón', callback_data='sporting_gijón')],
					[InlineKeyboardButton(text='Valencia', callback_data='valencia')],
					[InlineKeyboardButton(text='Villarreal', callback_data='villarreal')],
                   	])


#Ligas
leagues = {"España": "liga", "Inglaterra": "premier-league", "Italia": "serie-a", "Holanda": "eredivisie"}

#Jornadas
jornadas = {"22/08/16" : "1", "28/08/16": "2", "11/09/16" : "3", "19/09/16" : "4", "22/08/16": "5", "26/09/16" : "6", "02/10/16" : "7", "17/10/16": "8", "23/10/16" : "9", "31/10/16" : "10", "06/11/16": "11", "21/11/16" : "12", "28/11/16" : "13", "05/12/16": "14", "12/12/16" : "15", "19/12/16" : "16", "09/01/17": "17", "16/01/17" : "18", "23/01/17" : "19", "29/01/17": "20", "05/02/17" : "21", "12/02/17" : "22", "19/02/17": "23", "26/02/17" : "24", "01/03/17": "25", "05/03/17" : "26", "12/03/17" : "27", "19/03/17": "28", "02/04/17" : "29", "05/04/17" : "30", "09/04/17": "31", "16/04/17" : "32", "23/04/17": "33", "26/04/17" : "34", "30/04/17" : "35", "07/05/17": "36", "15/05/17" : "37", "21/05/17" : "38" }

jornadasE = {"22/08/16" : "1", "28/08/16": "2", "11/09/16" : "3", "19/09/16" : "4", "22/08/16": "5", "26/09/16" : "6", "02/10/16" : "7", "17/10/16": "8", "23/10/16" : "9", "31/10/16" : "10", "06/11/16": "11", "21/11/16" : "12", "28/11/16" : "13", "05/12/16": "14", "12/12/16" : "15", "19/12/16" : "16", "09/01/17": "17", "16/01/17" : "18", "23/01/17" : "19", "29/01/17": "20", "05/02/17" : "21", "12/02/17" : "22", "19/02/17": "23", "26/02/17" : "24", "01/03/17": "25", "05/03/17" : "26", "12/03/17" : "27", "19/03/17": "28", "02/04/17" : "29", "05/04/17" : "30", "09/04/17": "31", "16/04/17" : "32", "23/04/17": "33", "26/04/17" : "34"}

#Hilos de cada usuario
hilos = {}

#Cada hilo contendrá esta clase
class Consulta:
	def __init__(self):
		self.opcion = 0
		self.pais = "España"

#Inicia sesion
def init(cid):
	t = threading.Thread(target=menu, args=(cid,0,))
	t.setDaemon = True
	print('Nuevo hilo')
	hilos[cid] = Consulta()
	t.start()
	bot.sendMessage(cid, '¿Quieres saber el máximo goleador de una liga, las jornadas, los partidos de tu equipo, etc? Elige entre los países que te ofrecemos y explora todas las posibilidades que te ofrecemos')


def menu(cid, op):
	if hilos[cid].opcion == 0:		
		hilos[cid].opcion = 1
		bot.sendMessage(cid, "Elige un país" ,reply_markup=paises)
	elif hilos[cid].opcion == 1:
		hilos[cid].opcion = 2
		hilos[cid].pais = op
		if op == "España":
			bot.sendMessage(cid, "Ahora elige lo que quieres ver" ,reply_markup=opciones)
		elif op == "Italia":
			bot.sendMessage(cid, "Ahora elige lo que quieres ver" ,reply_markup=opcionesit)
		else:
		 	bot.sendMessage(cid, "Ahora elige lo que quieres ver" ,reply_markup=opcionesns)
	elif hilos[cid].opcion == 2:
		hilos[cid].opcion = 3
		bot.sendMessage(cid, "Elige un equipo" ,reply_markup=equipos)



def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	if content_type == 'text':
		if msg['text'] == '/start':
			bot.sendMessage(chat_id, 'Bienvenido')
			init(chat_id)#Inicia sesión con el usuario



def on_callback_query(msg):
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
	if hilos[from_id].opcion == 1:
		menu(from_id, query_data)
	elif hilos[from_id].opcion == 2:
		if query_data == "Clasificación":
			clasificacion(from_id, hilos[from_id].pais)
		elif query_data == "Partidos de un equipo":
			menu(from_id, hilos[from_id].opcion)
		elif query_data == "Máximos goleadores":
			topScorer(from_id)
		elif query_data == "atras":
			hilos[from_id].opcion == 0
			menu(from_id, 0)
	elif hilos[from_id].opcion == 3:
		partidosEquipo(from_id, query_data)
		
		
#Muestra la clasificación del país seleccionado		
def clasificacion(cid, op):
	bot.sendMessage(cid, "Te mostramos la clasificación en " + op)
	liga = leagues[op.encode('utf-8')]
	
	response = unirest.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/"+ liga +"/seasons/16-17/standings",
	  headers={
		"X-Mashape-Key": "Your X-Mashape-Key",
		"Accept": "application/json"
	  }
	)
	
	try: 
		js = response.body
		cont = 0
		if liga == "eredivisie":
			equipos = 18
		else:
			equipos = 20
		string = ""
		while cont != equipos:			
			string = string + str(js["data"]["standings"][cont]["position"]) + " - "
			string = string + js["data"]["standings"][cont]["team"] + " con "
			string = string + str(js["data"]["standings"][cont]["overall"]["points"]) + " puntos\n"
			cont = cont + 1			
		bot.sendMessage(cid, string)
		
	except: 
		bot.sendMessage(cid, 'Ha ocurrido un error al procesar los datos')
		print 'Ha ocurrido un error al procesar los datos'
	hilos[cid].opcion = 0
	menu(cid, 0)	
		
		

#Este metodo no se puede utilizar hasta que actualicen la bd
def jornada(cid):
	liga = leagues[hilos[cid].pais.encode('utf-8')]
	if liga == "eredivisie":
		rondas = 34
		jorn = jornadasE
	else:
		rondas = 38
		jorn = jornadas
	number = -1
	fechaAct = time.strftime("%x")
	for f in jorn:
		if str(fechaAct) < str(f):
			number = jorn[f]
			break
	
	bot.sendMessage(cid, "Te mostramos los partidos correspondientes a la jornada " + number + " de la "+ liga)
	
	response = unirest.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/"+liga+"/seasons/16-17/rounds/"+number+"/matches",
  headers={
    "X-Mashape-Key": "Your X-Mashape-Key",
    "Accept": "application/json"
  }
)
	try: 
		js = response.body
		cont = 0		
		string = ""
		while cont != rondas:			
			string = string + js["data"]["matches"][cont]["home"]["team"] + " vs "
			string = string + js["data"]["matches"][cont]["away"]["team"]
			if js["data"]["matches"][cont]["played"] == 1:
				string = string + " -> " + js["data"]["matches"][cont]["match_result"] + "\n"
			else:
				string = string + "\n"
			cont = cont + 1			
		bot.sendMessage(cid, string)
		
	except: 
		bot.sendMessage(cid, 'Ha ocurrido un error al procesar los datos')
		print 'Ha ocurrido un error al procesar los datos'
	hilos[cid].opcion = 0
	menu(cid, 0)
	
	
#Por ahora solo con equipos españoles, muestra todos los enfrentamientos de la temporada
def partidosEquipo(cid, equipo):
	response = unirest.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/liga/seasons/16-17/teams",
  headers={
    "X-Mashape-Key": "Your X-Mashape-Key",
    "Accept": "application/json"
  }
)	
	try: 
		js = response.body
		cont = 0
		_id = -1
		while cont != 20:	
			if js["data"]["teams"][cont]["team_slug"] == equipo:
				_id = js["data"]["teams"][cont]["identifier"]
				break
			cont = cont + 1		
	except: 
		bot.sendMessage(cid, 'Ha ocurrido un error al procesar los datos')
		print 'Ha ocurrido un error al procesar los datos'
	
	response2 = unirest.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/liga/seasons/16-17/rounds?team_identifier="+_id,
  headers={
    "X-Mashape-Key": "Your X-Mashape-Key",
    "Accept": "application/json"
  }
)
	try: 
		js2 = response2.body
		cont = 0		
		string = ""
		while cont != 38:				
			string = string + "Jornada " + str(cont+1) + ": "+ js2["data"]["rounds"][cont]["home_team"]
			string = string + " vs " + js2["data"]["rounds"][cont]["away_team"] + "\n"
			cont = cont + 1	
		bot.sendMessage(cid, string)	
				
	except: 
		bot.sendMessage(cid, 'Ha ocurrido un error al procesar los datos')
		print 'Ha ocurrido un error al procesar los datos'
	hilos[cid].opcion = 0
	menu(cid, 0)



#Muestra el top 10 de los máximos goleadores, por ahora solo para Italia
def topScorer(cid):	
	response = unirest.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/topscorers",
  headers={
    "X-Mashape-Key": "Your X-Mashape-Key",
    "Accept": "application/json"
  }
)
	try: 
		js = response.body
		cont = 0		
		string = ""
		while cont != 10:				
			string = string + str(cont+1) + ". "+ js["data"]["topscorers"][cont]["fullname"]
			string = string + " con " + js["data"]["topscorers"][cont]["goals"] + " goles\n"
			cont = cont + 1	
		bot.sendMessage(cid, string)	
				
	except: 
		bot.sendMessage(cid, 'Ha ocurrido un error al procesar los datos')
		print 'Ha ocurrido un error al procesar los datos'
	hilos[cid].opcion = 0
	menu(cid, 0)		


reload(sys)
sys.setdefaultencoding('utf-8')
bot = telepot.Bot('TOKEN')
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})
print ('Listening ...')

while 1:
	time.sleep(10)

