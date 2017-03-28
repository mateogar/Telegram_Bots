# -*- coding: utf-8 -*-
#author: Mateo García Fuentes
import telepot
import time
import threading
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#Este bot realiza un test de 10 preguntas sobre conocimientos futbolísticos
#Por ahora las 10 preguntas se repiten y están en el mismo orden
#En un futuro implementaré una función random y añadiré más preguntas

#DECLARACION KEYBOARDS (RESPUESTAS DEL TEST)
keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='RC Deportivo', callback_data='depor')],
					[InlineKeyboardButton(text='Real Sociedad', callback_data='real')],
					[InlineKeyboardButton(text='Betis', callback_data='betis')],
					[InlineKeyboardButton(text='Celta de Vigo', callback_data='celta')],
               ])

keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='FC Barcelona', callback_data='barca')],
					[InlineKeyboardButton(text='Zaragoza', callback_data='zgz')],
					[InlineKeyboardButton(text='Elche', callback_data='elche')],
					[InlineKeyboardButton(text='UD Las Palmas', callback_data='laspalmas')],
               ])

keyboard3 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Espanyol', callback_data='esp')],
					[InlineKeyboardButton(text='Zaragoza', callback_data='zgz')],
					[InlineKeyboardButton(text='Betis', callback_data='betis')],
					[InlineKeyboardButton(text='Villareal', callback_data='villareal')],
               ])

keyboard4 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Cristiano Ronaldo', callback_data='cr7')],
					[InlineKeyboardButton(text='Zarra', callback_data='zarra')],
					[InlineKeyboardButton(text='Messi', callback_data='messi')],
					[InlineKeyboardButton(text='Hugo Sánchez', callback_data='hugo')],
               ])

keyboard5 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Liverpool', callback_data='liverpool')],
					[InlineKeyboardButton(text='Ajax', callback_data='ajax')],
					[InlineKeyboardButton(text='Arsenal', callback_data='arsenal')],
					[InlineKeyboardButton(text='Olympique de Marseille', callback_data='marsella')],
               ])

keyboard6 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Hungría', callback_data='hungria')],
					[InlineKeyboardButton(text='Serbia', callback_data='serbia')],
					[InlineKeyboardButton(text='Ucrania', callback_data='ukra')],
					[InlineKeyboardButton(text='Dinamarca', callback_data='dinamarca')],
               ])

keyboard7 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='PSG', callback_data='psg')],
					[InlineKeyboardButton(text='PSV', callback_data='psv')],
					[InlineKeyboardButton(text='Olympique de Marseille', callback_data='marsella')],
					[InlineKeyboardButton(text='Borussia Dortmund', callback_data='dortmund')],
               ])

keyboard8 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Bayern München', callback_data='bayern')],
					[InlineKeyboardButton(text='Juventus', callback_data='juve')],
					[InlineKeyboardButton(text='Benfica', callback_data='benfica')],
					[InlineKeyboardButton(text='Milan', callback_data='milan')],
               ])

keyboard9 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='RC Deportivo', callback_data='depor')],
					[InlineKeyboardButton(text='Villareal', callback_data='villa')],
					[InlineKeyboardButton(text='Valencia', callback_data='val')],
					[InlineKeyboardButton(text='Athletic', callback_data='ath')],
               ])

keyboard10 = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Estadio Azteca', callback_data='azte')],
					[InlineKeyboardButton(text='Wembley', callback_data='wemb')],
					[InlineKeyboardButton(text='Maracaná', callback_data='mara')],
					[InlineKeyboardButton(text='Parque de los Príncipes', callback_data='parq')],
               ])

#Preguntas
p1 = '¿Cúal de estos equipos no ha ganado ningún título de liga?'
p2 = '¿Cúal de estos equipos recibió la goleada más abultada en toda la historia de la Liga?'
p3 = '¿Cúal de estos equipos no está en top10 de equipos con más puntos en la Liga?'
p4 = '¿Quién es el máximo goleador de la Liga?'
p5 = '¿Con qué equipo ningún jugador ha logrado ganar un Balón de Oro?'
p6 = '¿Qué país no cuenta con ningún jugador que haya logrado un Balón de Oro?'
p7 = '¿Qué equipo nunca ha ganado una Champions?'
p8 = '¿Qué equipo perdió más finales de Champions?'
p9 = '¿Cúal de estos equipos no ha llegado a semifinales de la Champions?'
p10 = '¿Cúal es el único estadio que no ha sido sede de una final de un Mundial?'


#Errores
e1 = 'El Celta de Vigo no ha ganado ningún título de liga'
e2 = 'El FC Barcelona perdió 12-1 contra el Athletic en 1931'
e3 = 'El Villareal es el 20º en la clasificación histórica, el Betis es 10º, el Zaragoza 9º y el Espanyol 7º'
e4 = 'Messi es el máximo goleador con 320 goles, le siguen C. Ronaldo con 265, Zarra con 251 y Sánchez con 234. (Actualizado a 6 de noviembre de 2016)'
e5 = 'En el 2001 Owen lo ganó con el Liverpool, en 1991 Jean-Pierre Papin con en el O. Marseille y en 1971 Cruyff con el Ajax'
e6 = 'El húngaro F. Albert lo ganó en 1967, el danés Simonsen en 1977 y el ucraniano Shevchenko en el 2004'
e7 = 'El PSV la ganó en la temporada 1986-87, el O. Marseille en la 1992-93 y el Dortmund en las 1996-97'
e8 = 'La Juventus perdió 6 finales, el Bayern y el Benfica 5 y el Milan 4'
e9 = 'El Villareal llegó a las semis en la temporada 2005-06, el Dépor en la 2003-04 y el Valencia en 2 ocasiones (1999-00 y 2000-01)'
e10 = 'La final Mundial de Francia no se jugó en el Parque de los Príncipes sino en el estadio de Saint-Denis'

#Almacena las tuplas de todas las partidas
test = {}

#Inicia el hilo de cada partida
def inicio(chat_id):
	tupla = [1, 0] #tupla -> Preguntas, Aciertos
	t = threading.Thread(target=preguntas, args=(chat_id,))
	t.setDaemon = True
	test[chat_id] = tupla
	print('Nuevo hilo')
	t.start()

#Realiza las preguntas y muestra las opciones
def preguntas(chat_id):
	tupla = test[chat_id]
	cont = tupla[0]	
	if cont == 1:
		bot.sendMessage(chat_id, 'Primera pregunta')
		bot.sendMessage(chat_id, p1, reply_markup=keyboard1)			
	elif cont == 2:
		bot.sendMessage(chat_id, 'Segunda pregunta')
		bot.sendMessage(chat_id, p2, reply_markup=keyboard2)
	elif cont == 3:
		bot.sendMessage(chat_id, 'Tercera pregunta')
		bot.sendMessage(chat_id, p3, reply_markup=keyboard3)
	elif cont == 4:
		bot.sendMessage(chat_id, 'Cuarta pregunta')
		bot.sendMessage(chat_id, p4, reply_markup=keyboard4)
	elif cont == 5:
		bot.sendMessage(chat_id, 'Quinta pregunta')
		bot.sendMessage(chat_id, p5, reply_markup=keyboard5)
	elif cont == 6:
		bot.sendMessage(chat_id, 'Sexta pregunta')
		bot.sendMessage(chat_id, p6, reply_markup=keyboard6)
	elif cont == 7:
		bot.sendMessage(chat_id, 'Séptima pregunta')
		bot.sendMessage(chat_id, p7, reply_markup=keyboard7)
	elif cont == 8:
		bot.sendMessage(chat_id, 'Octava pregunta')
		bot.sendMessage(chat_id, p8, reply_markup=keyboard8)
	elif cont == 9:
		bot.sendMessage(chat_id, 'Novena pregunta')
		bot.sendMessage(chat_id, p9, reply_markup=keyboard9)
	elif cont == 10:
		bot.sendMessage(chat_id, 'Décima pregunta')
		bot.sendMessage(chat_id, p10, reply_markup=keyboard10)

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	if content_type == 'text':
		if msg['text'] == '/start':
			bot.sendMessage(chat_id, 'Este bot evaluará tus conocimientos de fútbol con un sencillo test')
			inicio(chat_id)#Inicia el test
		else:
			tupla = test[chat_id]
			cont = tupla[0]	
			if cont == 11:
				if content_type == 'text':
					if msg['text'] == 'Si' or msg['text'] == 'si':
						inicio(chat_id)#Reinicia el test
						print('Reiniciando ...')
						bot.sendMessage(chat_id, 'Reiniciando test ...')					
					elif msg['text'] == 'No' or msg['text'] == 'no':
						tupla = [1, 0]
						test[chat_id] = tupla#Resetea los valores pero no el test
						bot.sendMessage(chat_id, 'De acuerdo. Gracias por participar')
					else:
						bot.sendMessage(chat_id, '¿Quieres volver a intentarlo? Responde si o no')
			else:#Pasa de pregunta
				preguntas(chat_id)

#"Corrige" las respuestas y suma la puntuación
def on_callback_query(msg):
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

	tupla = test[from_id]
	cont = tupla[0]	
	aciertos = tupla[1]
	if cont == 1:
		if query_data == 'celta':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e1)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 2:
		if query_data == 'barca':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e2)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 3:
		if query_data == 'villareal':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			time.sleep(2)
			bot.sendMessage(from_id, e3)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 4:
		if query_data == 'messi':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e4)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 5:
		if query_data == 'arsenal':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e5)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 6:
		if query_data == 'serbia':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e6)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 7:
		if query_data == 'psg':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e7)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 8:
		if query_data == 'juve':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e8)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 9:
		if query_data == 'ath':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e9)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
	elif cont == 10:
		if query_data == 'parq':
			bot.answerCallbackQuery(query_id, text='¡Correcto!')
			aciertos = aciertos + 1
			print('Pregunta '+ str(cont), 'Acierto', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		else:
			bot.answerCallbackQuery(query_id, text='¡Error!')
			bot.sendMessage(from_id, e10)
			time.sleep(2)
			print('Pregunta '+ str(cont), 'Error', 'Total actual: '+ str(aciertos)+ '/'+ str(cont))
		bot.sendMessage(from_id, 'Tu puntuación: '+ str(aciertos)+ '/'+ str(cont))
		bot.sendMessage(from_id, '¿Quieres volver a intentarlo? Responde si o no')

	cont = cont + 1
	tupla[0] = cont
	tupla[1] = aciertos
	test[from_id] = tupla
	preguntas(from_id)


TOKEN = 'TOKEN'
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})
print ('Listening ...')

while 1:
	time.sleep(10)
