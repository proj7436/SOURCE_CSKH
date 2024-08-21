import requests, os, telebot
from telebot import types
import gspread, threading, time, datetime
from google.oauth2.service_account import Credentials
import random, string
try:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
except:
    print('eror: Lỗi kết nối gg sheet')

TELEGRAM_BOT_TOKEN = '6996993496:AAFJwET1MnlWoViuCHb4__Ze_Z-5YOkWJgc'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

IMAGES_FORDEL = 'images'
VIDEOS_FORDEL = 'videos'
ID_GROUP = -1002167871661
try:
    if not os.path.exists(IMAGES_FORDEL):
        os.makedirs(IMAGES_FORDEL)
    if not os.path.exists(VIDEOS_FORDEL):
        os.makedirs(VIDEOS_FORDEL)
except:
    print('error: lõi không thể tạo thư mục')



data_initial_STORAGE_USERS_EDIT = {
    'message_id': '',
    'chat_id': '',
    'action': '',
    'question': '',
    'answer': '',
}
active_handle_files = False
STORAGE_USERS_EDIT = {
    'thanhdat06': data_initial_STORAGE_USERS_EDIT.copy(),
}
LENH = """
\n
1, thêm: thêm các vấn đề (nhắn tin riêng với BOT)
2, xóa: xóa các vấn đề (nhắn tin riêng với BOT)
3, dừng: dừng quá trình thêm hoặc xóa vấn đề (nhắn tin riêng với BOT)
4, lệnh: hiển thị các lệnh
5, hướng dẫn: hiểu thị các vấn đề
\n

"""

def get_data():
    SPREADSHEET_ID = '1KBDfvMcYnvI8X4MzXCCEskRzruaa8ZiCOO61pMWDui4'
    sheet = client.open_by_key(SPREADSHEET_ID)

    worksheet = sheet.get_worksheet(0)

    all_row = len(worksheet.col_values(1))


    data = []
    for i in range(2, all_row+1):
        question = worksheet.cell(i, 1).value
        answer = worksheet.cell(i, 2).value
        data.append((question, answer))

    return data
get_data()
def get_data_problem_default():
    SPREADSHEET_ID = '1KBDfvMcYnvI8X4MzXCCEskRzruaa8ZiCOO61pMWDui4'
    sheet = client.open_by_key(SPREADSHEET_ID)

    worksheet = sheet.get_worksheet(0)

    all_row = len(worksheet.col_values(3))


    data = []
    for i in range(2, all_row+1):
        question = worksheet.cell(i, 3).value
        answer = worksheet.cell(i, 4).value
        data.append((question, answer))

    return data
print(get_data_problem_default())
def create_button():

    data = get_data()
    keyboard = types.InlineKeyboardMarkup()

    for i in range(len(data)):
        items = data[i]
        keyboard.add(types.InlineKeyboardButton(items[0], callback_data=f"{i}"))
        
    return keyboard


def handle_action(STORAGE_USERS_EDIT, username):
    try:
        id = STORAGE_USERS_EDIT[username]['message_id']
        action = STORAGE_USERS_EDIT[username]['action']
        question = STORAGE_USERS_EDIT[username]['question']
        

        SPREADSHEET_ID = '1KBDfvMcYnvI8X4MzXCCEskRzruaa8ZiCOO61pMWDui4'
        sheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.get_worksheet(0)
        if action == "add":
            answer = STORAGE_USERS_EDIT[username]['answer']
            last_row_a = len(worksheet.col_values(1)) + 1
            last_row_b = len(worksheet.col_values(2)) + 1

            worksheet.update_cell(last_row_a, 1, question)

            worksheet.update_cell(last_row_b, 2, answer)
            
            return True,'Thành công'
        if action == 'delete':
            all_data = worksheet.get_all_values()

            for idx, row in enumerate(all_data):
                if question.lower() in row[0].lower():
                    # Xóa giá trị của cột A và B của dòng đó
                    cell_list = worksheet.range(f'A{idx + 1}:B{idx + 1}')
                    for cell in cell_list:
                        cell.value = ''
                    worksheet.update_cells(cell_list)
                    return True, 'Xóa thành công'

            return False, 'Không tìm thấy câu hỏi và câu trả lời trong bảng tính'
        elif action == 'update':
            answer = STORAGE_USERS_EDIT[username]['answer']
            all_data = worksheet.get_all_values()

            for idx, row in enumerate(all_data):
                if row[0].lower() == question.lower():
                    worksheet.update_cell(idx + 1, 2, answer)  
                    return True, 'Cập nhật thành công'

            return False, 'Không tìm thấy câu hỏi trong bảng tính'
    except gspread.exceptions.APIError as e:
        return False, f"Lỗi Google Sheets API: {e}"
    except KeyError as e:
        return False, f"Lỗi thiếu khóa trong dictionary: {e}"
    except Exception as e:  
        return  False, f"Lỗi không xác định: {e}"



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global STORAGE_USERS_EDIT, data_initial_STORAGE_USERS_EDIT, active_handle_files
    content = message.text
    username = message.from_user.username
    content_type = message.content_type
    print(message.chat.id)
    if content.startswith('hướng dẫn')and len(content.split()) == 2:
        keybroad = create_button()
        return bot.reply_to(message,
                        f"\n<b>Các vấn đề hỗ trợ:</b>", 
                        parse_mode='html',
                        reply_markup=keybroad
                        )
    elif content.lower().startswith('lệnh')and len(content.split()) == 1:
        return bot.reply_to(message, f'<b>{LENH}</b>', parse_mode='html')
    




    # lệnh phải có quyền mới dùng được

  
    elif content.lower().startswith('thêm') and len(content.split()) == 1:
       
        if message.chat.id != message.from_user.id:
            return bot.reply_to(message, f'<b>Hãy nhắn trực tiếp với BOT</b>', parse_mode='html')
        
        
        if username not in STORAGE_USERS_EDIT:
            return bot.reply_to(message, f'<b>Bạn không có quyền dùng lệnh này</b>', parse_mode='html')
        STORAGE_USERS_EDIT[username]['message_id'] = message.id 
        STORAGE_USERS_EDIT[username]['chat_id'] = message.chat.id
        STORAGE_USERS_EDIT[username]['action'] = 'add'
        return bot.reply_to(message, f'<b>Hãy nhập vấn đề cần thêm:</b>', parse_mode='html')


    elif content.lower().startswith('xóa')and len(content.split()) == 1:
        if message.chat.id != message.from_user.id:
            return bot.reply_to(message, f'<b>Hãy nhắn trực tiếp với BOT</b>', parse_mode='html')
        
        
        if username not in STORAGE_USERS_EDIT:
            return bot.reply_to(message, f'<b>Bạn không có quyền dùng lệnh này</b>', parse_mode='html')
       
        STORAGE_USERS_EDIT[username]['message_id'] = message.id 
        STORAGE_USERS_EDIT[username]['chat_id'] = message.chat.id

        STORAGE_USERS_EDIT[username]['action'] = 'delete'
        return bot.reply_to(message, f'<b>Hãy nhập vấn đề cần xóa:</b>', parse_mode='html')

    elif content.lower().startswith('dừng') and len(content.split()) == 1:
        if message.chat.id != message.from_user.id:
            return bot.reply_to(message, f'<b>Hãy nhắn trực tiếp với BOT</b>', parse_mode='html')
        
        
        if username not in STORAGE_USERS_EDIT:
            return bot.reply_to(message, f'<b>Bạn không có quyền dùng lệnh này</b>', parse_mode='html')
        STORAGE_USERS_EDIT[username] = data_initial_STORAGE_USERS_EDIT

        return 
    try:
        STORAGE_USERS_EDIT[username]['action'] == ''
    except:
        pass
    if STORAGE_USERS_EDIT[username]['message_id'] + 2 == message.id and STORAGE_USERS_EDIT[username]['action'] == 'add' and STORAGE_USERS_EDIT[username]['chat_id'] == message.chat.id:
        # question
        STORAGE_USERS_EDIT[username]['question'] = content
        active_handle_files = True
        return bot.reply_to(message, f'<b>Câu trả lời cho vấn đề:</b>', parse_mode= 'html')
    
    elif STORAGE_USERS_EDIT[username]['message_id'] + 2 == message.id and STORAGE_USERS_EDIT[username]['action'] == 'delete' and STORAGE_USERS_EDIT[username]['chat_id'] == message.chat.id:
        # question
        if message.content_type == 'text':
            STORAGE_USERS_EDIT[username]['question'] = content
            status, message_repons = handle_action(STORAGE_USERS_EDIT, username)  
            STORAGE_USERS_EDIT[username] = data_initial_STORAGE_USERS_EDIT
            
            if status:
                return bot.reply_to(message, f"<b>Xóa vấn đề thành công</b>", parse_mode='html')
            else:
                return bot.reply_to(message, f"<b>Xóa vấn đề thất bại: {message_repons}</b>",parse_mode='html')
    elif STORAGE_USERS_EDIT[username]['message_id'] + 4 == message.id and STORAGE_USERS_EDIT[username]['chat_id'] == message.chat.id:
        # question
        if message.content_type =='text':
            STORAGE_USERS_EDIT[username]['answer'] = content
            status, message_repons = handle_action(STORAGE_USERS_EDIT, username)  
            STORAGE_USERS_EDIT[username] = data_initial_STORAGE_USERS_EDIT
        
            if status:
                return bot.reply_to(message, f"<b>Thêm vấn đề thành công</b>", parse_mode='html')
            else:
                return bot.reply_to(message, f"<b>Thêm vấn đề thất bại: {message_repons}</b>",parse_mode='html')
        
def send_files(chat_id, files:list, caption_common, caption_list=None):
    """
    media: image, audio, video, document
    type files: list
    """
    if caption_list is None:

        media_group = [telebot.types.InputMediaPhoto(file, caption=caption_common, parse_mode='html') for file in files]
        return bot.send_media_group(chat_id, media_group)


    else:
        media_group = [telebot.types.InputMediaPhoto(file, caption=caption, parse_mode='html') for file, caption in zip(files, caption_list)]
        return bot.send_media_group(chat_id, media_group)

# nhận dữ liệu từ sheet về phân tích
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    try:
        data = get_data()

        for i in range(len(data)):
            if call.data != f'{i}':
                continue
            items = data[i]
            answer = items[1]
            type_answer = ''
            try:
                answer_split = answer.split()# check xem dạng nào (video, ảnh hay text)
                type_answer = answer_split[0]
            except:
                pass
            username = call.from_user.username
            first_name = call.from_user.first_name
            last_name = call.from_user.last_name
            if username is None:
                if not (first_name is None) and not (last_name is None):
                    username = f'{first_name} {last_name}'
                elif last_name is None:
                    username = f'{first_name}'
                elif first_name is None:
                    username = f'{last_name}'
       
            if items[1] is None:
                answer = 'không có dữ liệu cho vấn đề này'
            if type_answer == 'image':
                list_images_path  = [answer_split[i].replace('\\', '/') for i in range(1, len(answer_split))]
                if len(list_images_path) > 1:
                    return send_files(call.message.chat.id, list_images_path, caption=f'Trả lời {username}. [{items[0]}] Vui lòng làm theo ảnh.')
                with open(list_images_path[0], 'rb') as image:
                    bot.send_video(call.message.chat.id, image, caption=f'<u>Trả lời @{username}</u>\n\n <b>{items[0]}</b>\n\n Vui lòng làm theo ảnh.', parse_mode='html')
            elif type_answer == 'video':
                list_videos_path = [answer_split[i].replace('\\', '/') for i in range(1, len(answer_split))][0]
                with open(list_videos_path, 'rb') as video:
                    bot.send_video(call.message.chat.id, video, caption=f'<u>Trả lời @{username}</u> \n\n<b>{items[0]}</b>\n\n Vui làm theo video.', parse_mode='html')
            else:
                return bot.send_message(call.message.chat.id, f"<u>Trả lời @{username}</u>\n\n <b>{items[0]}\n\n {answer}</b>", parse_mode='html')
    except Exception as e:
        print(e)    
        



# add mem
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    data = get_data_problem_default()
    path_welcome = [item[1] for item in data if item[0] == 'welcome'][0]
    keybroad = create_button()
    for new_member in message.new_chat_members:

        username = new_member.username
        first_name = new_member.first_name
        last_name = new_member.last_name
        caption = f"Xin chào @{username}. Chào mừng bạn đến nhóm Billgatesvn.shop (fake bill chuyển khoản, biến động, số dư, cccd, giấy tờ xe,...), hân hạnh được phục vụ!"
        if not username:
            if not (first_name is None) and not (last_name is None):
                username = f'{first_name} {last_name}'
            elif last_name is None:
                username = f'{first_name}'
            elif first_name is None:
                username = f'{last_name}'
            caption = f"Xin chào {username}. Chào mừng bạn đến nhóm Billgatesvn.shop (fake bill chuyển khoản, biến động, số dư, cccd, giấy tờ xe,...), hân hạnh được phục vụ!"
        with open(path_welcome, 'rb') as photo:
            bot.send_photo(message.chat.id,
                            photo,
                            caption=caption, 
                            parse_mode='html', 
                            reply_markup=keybroad)

# out mem
@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):

    data = get_data_problem_default()
    path_bye = [item[1] for item in data if item[0] == 'bye'][0]
    left_member = message.left_chat_member
    username = left_member.username
    first_name = left_member.first_name
    last_name = left_member.last_name
    caption = f"Hẹn gặp lại @{username}. Chúc bạn một ngày tốt lành !"
    if not username:
        if not (first_name is None) and not (last_name is None):
            username = f'{first_name} {last_name}'
        elif last_name is None:
            username = f'{first_name}'
        elif first_name is None:
            username = f'{last_name}'
        caption = f"Hẹn gặp lại {username}. Chúc bạn một ngày tốt lành !"
    with open(path_bye, 'rb') as photo:
        bot.send_photo(message.chat.id,
                        photo,
                        caption=caption, 
                        parse_mode='html', 
                        )


@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    global STORAGE_USERS_EDIT, data_initial_STORAGE_USERS_EDIT
    username = message.from_user.username
    global active_handle_files
    if not active_handle_files:
        return
    if not (message.chat.id == message.from_user.id and message.from_user.username in STORAGE_USERS_EDIT):
        return 
    try:
        if message.content_type == 'photo':
            # Nhận thông tin file_id của ảnh (chọn độ phân giải cao nhất)
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path

            # Tải ảnh về từ server của Telegram
            photo_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'
            photo_data = requests.get(photo_url)

            # Tạo tên file mới
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            photo_file_path = os.path.join(IMAGES_FORDEL, f'image_{random_string}.jpg')

            # Lưu ảnh vào thư mục local
            with open(photo_file_path, 'wb') as photo_file:
                photo_file.write(photo_data.content)
            active_handle_files = False
            STORAGE_USERS_EDIT[username]['answer'] = f'image {photo_file_path}'
        elif message.content_type == 'video':
            # Nhận thông tin file_id của video
            file_id = message.video.file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path

            # Tải video về từ server của Telegram
            video_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'
            video_data = requests.get(video_url)

            # Tạo tên file mới
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            video_file_path = os.path.join(VIDEOS_FORDEL, f'video_{random_string}.mp4')
            # Lưu video vào thư mục local
            with open(video_file_path, 'wb') as video_file:
                video_file.write(video_data.content)

            active_handle_files = False
            STORAGE_USERS_EDIT[username]['answer'] = f'video {video_file_path}'
        
        status, message_repons = handle_action(STORAGE_USERS_EDIT, username)  
        STORAGE_USERS_EDIT[username] = data_initial_STORAGE_USERS_EDIT
        if status:
                return bot.reply_to(message, f"<b>Thêm vấn đề thành công</b>", parse_mode='html')
        else:
            return bot.reply_to(message, f"<b>Thêm vấn đề thất bại: {message_repons}</b>",parse_mode='html')
    except Exception as e:
        return bot.reply_to(message, f"Đã xảy ra lỗi: {e}")
# Khởi động bot
# while True:
#     try:
#         bot.polling()
#     except Exception:
#         pass

def goodMorning(hour, minute, second):
    _hour = 7
    _minute = 30
    _second = 0
    if not (hour == _hour and minute == _minute and second == _second): 
        return 
    
    caption = "\n<b>Buổi sáng tối lành cả nhà yêuu🥱👁👁</b>"
    i = random.randint(1, 5)
    with open(f"{VIDEOS_FORDEL}/gm{i}.mp4", 'rb') as video:
        bot.send_video(ID_GROUP,
                        video,
                        caption=caption, 
                        parse_mode='html', 
                        )
        
def goodnoon(hour, minute, second):
    _hour = 11
    _minute = 0
    _second = 0
    if not (hour == _hour and minute == _minute and second == _second): 
        return 
    
    caption = "\n<b>Buổi trưa vui vẻ không quạo😤🥶</b>"
    i = random.randint(1, 5)
    with open(f"{VIDEOS_FORDEL}/gn{i}.mp4", 'rb') as video:
        bot.send_video(ID_GROUP,
                        video,
                        caption=caption, 
                        parse_mode='html', 
                        )
def goodnight(hour, minute, second):
    _hour = 22
    _minute = 30
    _second = 0
    if not (hour == _hour and minute == _minute and second == _second): 
        return 
    
    caption = "\n<b>Ngủ thôi nhà mình ơi😴😴</b>"
    i = random.randint(1, 4)
    with open(f"{VIDEOS_FORDEL}/gnight{i}.mp4", 'rb') as video:
        bot.send_video(ID_GROUP,
                        video,
                        caption=caption, 
                        parse_mode='html', 
                        )
def auto_handle():
    while True:
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        goodMorning(hour, minute, second)
        # goodnoon(hour, minute, second)
        # goodnight(hour, minute, second)
        time.sleep(1)
thread = threading.Thread(target=auto_handle)
thread.setDaemon(True)
thread.start()


bot.infinity_polling(timeout=10, long_polling_timeout = 5)