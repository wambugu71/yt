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
            result = ydl.extract_info(
                args,
                download=False  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
        
        for i in video['formats']:
            link = '<a href=\"' + i['url'] + '\">' + 'link' + '</a>'

            if i.get('format_note'):
                bot.reply_to(msg, 'Quality- ' + i['format_note'] + ': ' + link, parse_mode='HTML')
            else:
                bot.reply_to(msg, link, parse_mode='HTML', disable_notification=True)
    except:
        bot.reply_to(msg, ' sorry This can\'t be downloaded by me')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id, "use command /start to welcome menu. Use /youtube <link> or /facebook <video or reel link> to download the video, choose your best quality to download.Enjoy your favorite videos.")
@bot.message_handler(commands=["facebook"])
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
#pool~start the bot
bot.polling()
