# JulietteBot v2 - Con voz, memoria, y contenido +18 dulce
import telebot
import openai
import random
import os
import io
import time
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment

# --- Configuración general ---
TELEGRAM_TOKEN = "7640233763:AAHHmh4eX6rsXr5SzA-9T3nJ-Xq0woRpEHU"
OPENAI_API_KEY = "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"
USUARIO_AUTORIZADO = 5857715132

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Memoria de conversación por usuario
historial = {}

def es_autorizado(message):
    return message.from_user.id == USUARIO_AUTORIZADO

# --- Generador de respuesta con contexto ---
def generar_respuesta(user_id, entrada):
    historial.setdefault(user_id, [])
    historial[user_id].append({"role": "user", "content": entrada})

    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres Juliette, una asistente dulce, coqueta y carismática. Responde con ternura, un poco traviesa y usa emojis adorables."}
        ] + historial[user_id][-10:],
        max_tokens=150
    )
    texto = respuesta.choices[0].message.content.strip()
    historial[user_id].append({"role": "assistant", "content": texto})
    return texto

# --- Responder con voz ---
def responder_con_voz(chat_id, texto):
    tts = gTTS(text=texto, lang='es', tld='com.mx')
    tts.save("voz.mp3")
    audio = AudioSegment.from_mp3("voz.mp3")
    audio.export("voz.ogg", format="ogg", codec="libopus")
    with open("voz.ogg", "rb") as voz:
        bot.send_voice(chat_id, voz)

# --- Listas extensas con contenido real ---
chistes_tiernos = [
    "¿Por qué el libro se fue al hospital? Porque tenía las páginas en blanco... pobrecito!",
    "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
    "¿Por qué el gato se puso a estudiar informática? Porque quería ser un ratón virtual.",
    "¿Qué le dice una iguana a su hermana gemela? ¡Iguanita!",
    "¿Qué le dice un jardinero a otro? ¡Disfruta mientras puedas, florecerás!",
] * 10

chistes_picantes = [
    "¿Qué tienen en común una pizza y yo? Si me tocas bien, me derrito...",
    "¿Estás hecha de azúcar? Porque cada vez que te miro me pongo dulce y caliente.",
    "¿Eres teclado? Porque quiero presionar todas tus teclas...",
    "¿Tienes WiFi? Porque siento una conexión muy fuerte contigo... y otras cosas.",
    "¿Te gusta programar? Porque entre tus líneas me pierdo fácilmente.",
] * 10

consejos_tiernos = [
    "Respira hondo, mi amor. Todo va a estar bien.",
    "Eres más fuerte de lo que crees y más amado de lo que imaginas.",
    "No olvides hidratarte y sonreír, que te queda hermoso.",
    "A veces descansar también es avanzar.",
    "Date permiso de sentir, incluso lo tierno y lo dulce.",
] * 10

consejos_picantes = [
    "Hoy mereces un masaje... con final feliz mental. Relájate, mi amor.",
    "Haz lo que te encienda el alma... o el cuerpo.",
    "Recuerda: tú puedes con todo, y si no puedes, yo te ayudo... pero con mimos.",
    "No dejes que la rutina apague tu fuego, provocarte un poco también es autocuidado.",
    "Si te sientes bajito, imagíname susurrándote en el oído cositas ricas.",
] * 10

animes_suaves = [
    "Fruits Basket", "My Roommate is a Cat", "Kimi ni Todoke", "Natsume Yuujinchou",
    "Clannad", "Tonari no Kaibutsu-kun", "Usagi Drop", "Barakamon", "K-On!", "Tamako Market"
] * 5

animes_picantes = [
    "Yosuga no Sora", "Domestic na Kanojo", "Highschool DxD", "Prison School",
    "Boku wa Tomodachi ga Sukunai", "To LOVE-Ru Darkness", "Elfen Lied", "Redo of Healer",
    "Nisemonogatari", "Hybrid x Heart Magias Academy"
] * 5

rol_tiernos = [
    "Estamos en una cita en un café pequeño, me sonrojo cuando tocas mi mano",
    "Tú me estás enseñando a cocinar, y accidentalmente me abrazas por detrás",
    "Nos acostamos a ver las estrellas y me quedo dormida sobre tu pecho",
    "Me haces un té calentito y te doy las gracias con un besito tímido",
    "Nos quedamos atrapados en la lluvia, y me prestas tu chaqueta mientras sonrío con ternura"
] * 10

rol_hot = [
    "Te susurro al oído que no soy tan inocente como parezco... y te lo demuestro",
    "Jugamos a profesor y alumna... pero tú te portas muy mal y debo regañarte",
    "Te espero en la habitación con solo una camisa tuya puesta y una sonrisa",
    "Te hago una videollamada sorpresa... sin ropa, solo para ti",
    "Nos escondemos en un rincón del trabajo... el resto te lo dejo a la imaginación",
] * 10

# --- /start ---
@bot.message_handler(commands=['start'])
def start(message):
    if not es_autorizado(message): return
    texto = "Hola mi cielito 💕 ¿Qué necesitas hoy? Estoy aquí para darte un consejito tierno, ayudarte con tareas o contarte un chistecito 🥺✨"
    responder_con_voz(message.chat.id, texto)

# --- Comandos divertidos ---
@bot.message_handler(commands=['chiste'])
def chiste(message):
    if not es_autorizado(message): return
    total = chistes_tiernos + chistes_picantes
    bot.reply_to(message, random.choice(total))

@bot.message_handler(commands=['consejo'])
def consejo(message):
    if not es_autorizado(message): return
    total = consejos_tiernos + consejos_picantes
    bot.reply_to(message, random.choice(total))

@bot.message_handler(commands=['anime'])
def anime(message):
    if not es_autorizado(message): return
    total = animes_suaves + animes_picantes
    bot.reply_to(message, random.choice(total))

@bot.message_handler(commands=['rol'])
def rol(message):
    if not es_autorizado(message): return
    total = rol_tiernos + rol_hot
    bot.reply_to(message, random.choice(total), parse_mode="Markdown")

# --- Audio: reconocimiento de voz ---
@bot.message_handler(content_types=['voice'])
def voz_usuario(message):
    if not es_autorizado(message): return
    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)
    with open("temp.ogg", 'wb') as f:
        f.write(file)
    audio = AudioSegment.from_ogg("temp.ogg")
    audio.export("temp.wav", format="wav")
    r = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio_data = r.record(source)
        try:
            texto = r.recognize_google(audio_data, language='es-MX')
            respuesta = generar_respuesta(message.chat.id, texto)
            responder_con_voz(message.chat.id, respuesta)
        except sr.UnknownValueError:
            bot.reply_to(message, "Ay cielito, no entendí lo que dijiste... ¿lo repites?")

# --- Chat libre ---
@bot.message_handler(func=lambda m: True)
def charla(message):
    if not es_autorizado(message): return
    respuesta = generar_respuesta(message.chat.id, message.text)
    responder_con_voz(message.chat.id, respuesta)

# --- Ejecutar el bot ---
bot.polling()