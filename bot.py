import telebot
import os
import io
from network import main
from telebot import apihelper

TOKEN = '1100674609:AAF3HHC7R-8eaw97T0GGhkdmuxRLFVM0igM'

apihelper.proxy = {'https': 'socks5://student:TH8FwlMMwWvbJF8FYcq0@178.128.203.1:1080'}
bot = telebot.TeleBot(TOKEN)

START_MSG = '''Hello, User! I'm Neural Style Transfer Telegram bot.
You can send me two pictures and I'll transfer style from one pictures to another.
To get more information send me /help.'''

HELP_MSG = '''Okay, send me one picture with style you want to use. \
Don't forget to write "Style" in the same message. Then send me \
another picture with content with the word "Content". After that type /process \
and wait a little.'''

S_RECEPTION_MSG = 'Okay, I got your style image'
C_RECEPTION_MSG = 'Okay, I got your content image'

FORGOT_MSG = 'Oh... It seems like you forgot to send me style or content image'

PROCESSING_MSG = 'Starting to process your images... It will take about four minutes'

WORD_MISTAKE_MSG = 'Oh... It seems like you made a mistake in the word "style" or "content". Try again'
WORD_FORGOT_MSG = 'Oh... It seems like you forgot to specify a keyword. Send one and any photo in the same message'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, START_MSG)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, HELP_MSG)


@bot.message_handler(content_types=['photo'])
def receive_photos(message):
    if (message.caption is not None) and ((message.caption == 'Style') or (message.caption == 'style')):
        style_photo_id = message.photo[-1].file_id
        style_photo_info = bot.get_file(style_photo_id)
        style_photo = bot.download_file(style_photo_info.file_path)
        with open('style' + str(message.chat.id) + '.jpg', 'wb') as style:
            style.write(style_photo)
        bot.send_message(message.chat.id, S_RECEPTION_MSG)
    elif (message.caption is not None) and ((message.caption == 'Content') or (message.caption == 'content')):
        content_photo_id = message.photo[-1].file_id
        content_photo_info = bot.get_file(content_photo_id)
        content_photo = bot.download_file(content_photo_info.file_path)
        with open('content' + str(message.chat.id) + '.jpg', 'wb') as content:
            content.write(content_photo)
        bot.send_message(message.chat.id, C_RECEPTION_MSG)
    elif message.caption is not None:
        bot.send_message(message.chat.id, WORD_MISTAKE_MSG)
    else:
        bot.send_message(message.chat.id, WORD_FORGOT_MSG)


@bot.message_handler(commands=['process'])
def process_photos(message):
    style_photo_path = 'style' + str(message.chat.id) + '.jpg'
    if not os.path.exists(style_photo_path):
        bot.send_message(message.chat.id, FORGOT_MSG)
        return 0
    content_photo_path = 'content' + str(message.chat.id) + '.jpg'
    if not os.path.exists(content_photo_path):
        bot.send_message(message.chat.id, FORGOT_MSG)
        return 0
    bot.send_message(message.chat.id, PROCESSING_MSG)
    output, _, _ = main(style_photo_path, content_photo_path)
    output_bytes = io.BytesIO()
    output.save(output_bytes, format='PNG')
    output_bytes = output_bytes.getvalue()
    bot.send_photo(message.chat.id, output_bytes)
    os.remove(style_photo_path)
    os.remove(content_photo_path)
    del output
    del output_bytes


if __name__ == '__main__':
    bot.infinity_polling(True)
