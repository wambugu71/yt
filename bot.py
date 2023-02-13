#required packages
import telebot
import requests
import yt_dlp
import time
from pytube import YouTube
import os
from PyDictionary import *
import json, youtube_dl
#TELEGRAM_TOKEN= 5686577136:AAF8NGC6p-Jqw17XWCL4Z-7DW9WafzsVHzY
#Config vars
#token = os.environ['TELEGRAM_TOKEN']
#token = os.environ['5686577136:AAF8NGC6p-Jqw17XWCL4Z-7DW9WafzsVHzY']
TOKEN= "5686577136:AAF8NGC6p-Jqw17XWCL4Z-7DW9WafzsVHzY"
#	with open('config.json') as f:
# token = json.load(f)
  
#Intitialize YouTube downloader
ydl_opts = {}
ydl = yt_dlp.YoutubeDL(ydl_opts)



#initialise  bot
#bot = telebot.TeleBot(token)
bot = telebot.TeleBot(TOKEN)
x = bot.get_me()
print(x)

#   handling /commands  #

# works when /start is given
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.send_message(message.chat.id, "Welcome user this is a YouTube downloader made by @wambugu_kinyua.\n Usage:\n /youtube <link>\n /Facebook <link> to download videos and reels")

# works when /motivate is given
@bot.message_handler(commands=['motivate'])
def send_quotes(message):
        quote = requests.request(url='https://api.quotable.io/random',method='get')
        bot.send_message(message.chat.id, quote.json()['content'])

@bot.message_handler(commands=["facebook","Facebook", "Twitter", "twitter"])
def facebook(message):
    args = message.text.split()[1]
    #bot.send_message(message.chat.id, text= os.system(f"youtube-dl {args} -g") )
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
 #       yvd=ydl.download([args]
        try:
            with ydl:
                info = ydl.extract_info( args,download=False)

            if 'entries' in info:
                # Can be a playlist or a list of videos
                video = info['entries'][0]
            else:
                # Just a video
                video = info
            
            for i in video['formats']:
                link = '<a href=\"' + i['url'] + '\">' + 'link' + '</a>'
    
                if i.get('format_note'):
                    bot.reply_to(message, 'Quality- ' + i['format_note'] + ': ' + link, parse_mode='HTML')
                else:
                    bot.reply_to(message, link, parse_mode='HTML', disable_notification=True)
        except:
            bot.reply_to(message, ' sorry This can\'t be downloaded by me')
@bot.message_handler(commands=['start','hello', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id, "use command /start to welcome menu. Use /youtube <link> to download the video, choose your best quality to download.Enjoy your favorite videos.")
@bot.message_handler(commands=["meaning"])
def find_meaning(message):
    args= message.text.split()[1]
    dc = PyDictionary()
    try:
        my_meaning = dc.meaning(args)
        bot.send_message(message.chat.id, text=my_meaning["Noun"])
    except:
        bot.send_message(message.chat.id,"As a backend model, Am Unable to search for the word, my training data has no that word.")

@bot.message_handler(commands=["YouTube", "youtube", "download", "Youtube","video"])
def yt(message):
    args= message.text.split()[1]
#    from pytube import YouTube
    ken = YouTube(args)
    try:
        z = ken.streams.filter(file_extension='mp4').get_by_itag(22).url
        link = '<a href=\"' + z + '\">' + 'link' + '</a>'
        bot.reply_to(message, 'Congrats!🎊\nVideo found.🥳🥳\n'  + ': ' + link+ "Credits: @wambugu_kinyua", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "Unable to download the video🥲🥲🙂")
        
#pool~start the bot
bot.polling()
