import telebot
from datetime import datetime
import threading, time, random

TOKEN = '7089202361:AAGXraZCE9trFyAeb-7oc09HH_zKaRUNHc0'  
bot = telebot.TeleBot(TOKEN)

TU_NONG =  [
    "lừa đảo", "địt", "chúng mày", "lùa gà", "nừa đảo", "fuck",
    "lồn", "buồi", "cứt", "cút", "đĩ", "mả cha", "con mẹ",
    "thằng chó", "cha", "cụ mày", "cặc", "cái bướm"
]



time_good_morning = [8, 15, 0]
time_good_night = [22, 15, 0]

ID_GROUP = -1002164429437
def send_image_caption(id_chat, text, img):
    photo = open(f'images/{img}', 'rb') 
    bot.send_photo(id_chat, photo, caption=text, parse_mode='html')






def goodMorning(hour, minute, second):
    _hour = time_good_morning[0]
    _minute = time_good_morning[1]
    _second = time_good_morning[2]
    if not (hour == _hour and minute == _minute and second == _second): 
        return 
    
    caption = "\n<b>Chào buổi sáng mọi người,  điểm danh ngay nhận ngay quà khủng🎁</b>"
    i = random.randint(1, 5)
    with open(f"videos/gm{i}.mp4", 'rb') as video:
        bot.send_video(ID_GROUP,
                        video,
                        caption=caption, 
                        parse_mode='html', 
                        )
        

def goodnight(hour, minute, second):
    _hour = time_good_night[0]
    _minute = time_good_night[1]
    _second = time_good_night[2]
    if not (hour == _hour and minute == _minute and second == _second): 
        return 
    
    caption = "\n<b>Chúc mọi người ngủ ngon💤</b>"
    i = random.randint(1, 5)
    with open(f"videos/gnight{i}.mp4", 'rb') as video:
        bot.send_video(ID_GROUP,
                        video,
                        caption=caption, 
                        parse_mode='html', 
                        )
        
def get_full_name(user):
    first_name = user.last_name if user.last_name else ''
    last_name = user.first_name if user.first_name else ''
    full_name = f"{last_name} {first_name}".strip()  
    return full_name

def auto_handle():
    while True:
        hour =datetime.now().hour
        minute = datetime.now().minute
        second = datetime.now().second
        goodMorning(hour, minute, second)
        goodnight(hour, minute, second)
        time.sleep(1)
thread = threading.Thread(target=auto_handle)
thread.setDaemon(True)
thread.start()
@bot.message_handler(content_types=['text'])
def handle_message(message):
    text = message.text.lower()
    print(message.chat.id)
    if text == 'id':
        return bot.reply_to(message, message.chat.id)
    
    if any(word in text for word in TU_NONG):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.ban_chat_member(message.chat.id, message.from_user.id)
            name = get_full_name(message.from_user)
            bot.send_message(message.chat.id, f"Thành Viên <b><i>{name}</i></b> đã bị đuổi bởi gây rối", parse_mode='html')
        except Exception as e:
            print(f"An error occurred: {e}")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        name = get_full_name(new_member)
        send_image_caption(message.chat.id, f"Chào mừng chủ cửa hàng <b><i>{name}</i></b> đã tham gia nhóm Các nhà bán hàng của trung tâm mua sắm TikTok Shop !", 'wc_2.jpg')

@bot.message_handler(content_types=['left_chat_member'])
def goodbye_member(message):
    name = get_full_name(message.left_chat_member)
    send_image_caption(message.chat.id, f"Hẹn gặp lại <b><i>{name}</i></b> ! Cảm ơn bạn đã tin tưởng và kinh doanh trên nền tảng TMĐT TikTok Shop. Chúc bạn luôn buôn may bán đắt !", 'bye_2.jpg')

bot.infinity_polling(timeout=10, long_polling_timeout=5)
