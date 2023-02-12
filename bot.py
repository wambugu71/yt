#required packages
import telebot
import requests
import yt_dlp
import os
import json, youtube_dl
#Config vars
#token = os.environ['TELEGRAM_TOKEN']

#with open('config.json') as f:
# token = json.load(f)
TOKEN = "5686577136:AAF8NGC6p-Jqw17XWCL4Z-7DW9WafzsVHzY"
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
  bot.send_message(message.chat.id, "Welcome user this is a YouTube downloader made by @wambugu_kinyua.\n Usage type:\t1. '/youtube <link>'\n\t2. '/facebook <video/reel link>")

# works when /motivate is given
@bot.message_handler(commands=['motivate'])
def send_quotes(message):
        quote = requests.request(url='https://api.quotable.io/random',method='get')
        bot.send_message(message.chat.id, quote.json()['content'])

# works when /ytdl <link> is given
@bot.message_handler(commands=['youtube'])
def down(msg):
    args = msg.text.split()[1]
    try:
        with ydl:
            video = ydl.extract_info(args, download=False )
            json_object = json.dumps(video, indent=4)
    # Writing to sample.json
            with open("kinyua.json", "w") as outfile:
                outfile.write(json_object)
        
        f = open("kinyua.json")  
        data = json.load(f) 
        frames = []
        for i in range(15, 70):
            frames.append(i)
        mydata= frames
        quality = [720,360,2160]
    #print("frames {}".format(mydata))
        for i in data["formats"]:
            if i["fps"]  in mydata and i["height"] in quality:
    #    for i in data['formats']:
                shit = i["url"]
                link = '<a href="{}"> link </a>'.format(shit)
                if i.get('format_note'):
                    bot.reply_to(msg, 'Quality- ' + i['format_note'] + ': ' + link, parse_mode='HTML')
                else:
                    bot.reply_to(msg, link, parse_mode='HTML', disable_notification=True)
        f.close()

    except:
       bot.reply_to(msg, ' sorry This can\'t be downloaded by me')
#pool~start the bot
bot.polling()
