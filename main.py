import telebot
import psycopg2
import requests

bot = telebot.TeleBot('TOP_SECRET')

conn = psycopg2.connect(dbname='playground', user='postgres', password='postgres', host='localhost')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS files (
    file_name TEXT PRIMARY KEY,
    image TEXT,
    pdf_link TEXT,
    video_link TEXT
)
''')
conn.commit()
def is_valid_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

def is_valid_youtube(url):
    return url.startswith('https://www.youtube.com/watch?v=')

unit_to_multiplier = {
    1: 10**-3,
    2: 10**-2,
    3: 10**-1,
}

@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    if message.content_type == 'text':
        map = message.text.split("\n\n")
        if len(map) == 1:
            file_name = message.text
            cur.execute('SELECT * FROM files WHERE file_name = %s', (file_name,))
            result = cur.fetchone()
            if result:
                image, pdf_link, video_link = result[1], result[2], result[3]
                bot.send_photo(message.chat.id, image, f'{file_name}\n\nОбзор: {video_link}\n\nПравила: {pdf_link}')
            else:
                bot.send_message(message.chat.id, 'Извините, я не нашел такой файл в базе данных.')
        elif len(map) == 4:
            file_name, image, pdf_link, video_link = map[0], map[1], map[3], map[2] #  message.photo[-1].file_id
            if file_name and not cur.execute('SELECT 1 FROM files WHERE file_name = %s', (file_name,)):
                if 'pdf' in pdf_link and is_valid_url(pdf_link) and is_valid_url(video_link):
                    cur.execute('INSERT INTO files VALUES (%s, %s, %s, %s)', (file_name, image, pdf_link, video_link))
                    conn.commit()
                    bot.send_message(message.chat.id, 'Файл успешно добавлен в базу данных.')
                else:
                    bot.send_message(message.chat.id,
                                     'Ошибка формата запроса.\n\nЗапрос должен выглядеть так:\n*Название*\n\n*Ссылка на правила*\n\n*Ссылка на видео*\n\nТакже нужно приложить изображение')
            else:
                bot.send_message(message.chat.id, 'Извините, я не могу добавить этот файл в базу данных. Пожалуйста, укажите уникальное название файла.')
        else:
            bot.send_message(message.chat.id, 'Извините, я не понимаю ваше сообщение. Пожалуйста, следуйте инструкциям.')
            bot.send_message(message.chat.id, 'Для добавления файла в базу данных, отправьте мне фото с названием файла в подписи. Вы также можете добавить ссылку на пдф файл и/или видео на ютубе в тексте сообщения. Для получения файла из базы данных, отправьте мне только название файла в тексте сообщения.')

bot.polling()
