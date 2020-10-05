import RPi.GPIO as GPIO
import time, datetime
import os
import sys
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

#t = time.localtime()
'''
setTime1 = '2:12'
stat1 = 0
setTime2 = '2:12'
stat2 = 0
setTime3 = '2:12'
stat3 = 0
'''

GPIO.setwarnings(False)

# Inisialisasi Pin
DIR_MTR1 = 14
DIR_MTR2 = 15
STEP_MTR1 = 12
STEP_MTR2 = 13
DRIVER = 18
RELAY = 23

# Perintah untuk menggunakan pin board GPIO Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Pengaturan GPIO 
GPIO.setup(DIR_MTR1, GPIO.OUT)
GPIO.setup(DIR_MTR2, GPIO.OUT)
GPIO.setup(STEP_MTR1, GPIO.OUT)
GPIO.setup(STEP_MTR2, GPIO.OUT)
GPIO.setup(DRIVER, GPIO.OUT)
GPIO.setup(RELAY, GPIO.OUT)

GPIO.output(RELAY, 1) #Off initially

propose_records = telepot.helper.SafeDict()  # thread-safe dict

#SetTelegram
TOKEN = '1202817061:AAHLFAFoftMnaOenIt59XG_IzGIp8a7yM2M'
CHATID = 1137202289

#set schedul/jadwal pencitraan
schedule = 0

jadwal_1 = 0
jadwal_2 = 0
jadwal_3 = 0
takar_1 = 0
takar_2 = 0
takar_3 = 0
status_1 = False
status_2 = False
status_3 = False

class Lover(telepot.helper.ChatHandler):
    keyboard = ReplyKeyboardMarkup(keyboard=[[ #<-- Menu awal
                   KeyboardButton(text='Beri Pakan'),
                   KeyboardButton(text='Pengaturan')], [
                   KeyboardButton(text='UMmm ...'),
                   KeyboardButton(text='Keluar')
               ]], one_time_keyboard=True)
    keyboard1 = ReplyKeyboardMarkup(keyboard=[[ #<-- Terusan Pengaturan dari Menu Awal
                   KeyboardButton(text='Set Penjadwalan Pemberian Pakan')], [
                   KeyboardButton(text='Set Dosis Pemberian Pakan')
               ]], one_time_keyboard=True)
    keyboard2 = ReplyKeyboardMarkup(keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   KeyboardButton(text='Jadwal Kolam 1'),
                   KeyboardButton(text='Jadwal Kolam 2')], [
                   KeyboardButton(text='Jadwal Kolam 3'),
                   KeyboardButton(text='Jadwal Semua Kolam')], [
                   KeyboardButton(text='Kembali')
               ]], one_time_keyboard=True)
    keyboard3 = ReplyKeyboardMarkup(keyboard=[[ #<-- Terusan Pengaturan-Waktu dari Menu Awal
                   KeyboardButton(text='Dosis Kolam 1'),
                   KeyboardButton(text='Dosis Kolam 2')], [
                   KeyboardButton(text='Dosis Kolam 3'),
                   KeyboardButton(text='Dosis Semua Kolam')], [
                   KeyboardButton(text='Kembali')
               ]], one_time_keyboard=True)
    keyboard4 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='00:00', callback_data='0'),
                   InlineKeyboardButton(text='01:00', callback_data='1'), 
                   InlineKeyboardButton(text='02:00', callback_data='2'),
                   InlineKeyboardButton(text='03:00', callback_data='3')],[
                   InlineKeyboardButton(text='04:00', callback_data='4'),
                   InlineKeyboardButton(text='05:00', callback_data='5'), 
                   InlineKeyboardButton(text='06:00', callback_data='6'),
                   InlineKeyboardButton(text='07:00', callback_data='7')],[
                   InlineKeyboardButton(text='08:00', callback_data='8'),
                   InlineKeyboardButton(text='09:00', callback_data='9'), 
                   InlineKeyboardButton(text='10:00', callback_data='10'),
                   InlineKeyboardButton(text='11:00', callback_data='11')],[
                   InlineKeyboardButton(text='12:00', callback_data='12'),
                   InlineKeyboardButton(text='13:00', callback_data='13'), 
                   InlineKeyboardButton(text='14:00', callback_data='14'),
                   InlineKeyboardButton(text='15:00', callback_data='15')],[
                   InlineKeyboardButton(text='16:00', callback_data='16'),
                   InlineKeyboardButton(text='17:00', callback_data='17'), 
                   InlineKeyboardButton(text='18:00', callback_data='18'),
                   InlineKeyboardButton(text='19:00', callback_data='19')],[
                   InlineKeyboardButton(text='20:00', callback_data='20'),
                   InlineKeyboardButton(text='21:00', callback_data='21'), 
                   InlineKeyboardButton(text='22:00', callback_data='22'),
                   InlineKeyboardButton(text='23:00', callback_data='23')],[
                   InlineKeyboardButton(text='Kembali', callback_data='kembali')
               ]], resize_keyboard=True, one_time_keyboard=True)
    keyboard5 = ReplyKeyboardMarkup(keyboard=[[ 
                   KeyboardButton(text='Pakan Kolam 1'),
                   KeyboardButton(text='Pakan Kolam 2')], [
                   KeyboardButton(text='Pakan Kolam 3'),
                   KeyboardButton(text='Pakan Semua Kolam')], [
                   KeyboardButton(text='Kembali')
               ]], one_time_keyboard=True)

    def __init__(self, *args, **kwargs):
        super(Lover, self).__init__(*args, **kwargs)

        # Retrieve from database
        global propose_records
        if self.id in propose_records:
            self._edit_msg_ident = propose_records[self.id]
            self._editor = telepot.helper.Editor(self.bot, self._edit_msg_ident) if self._edit_msg_ident else None
        else:
            self._edit_msg_ident = None
            self._editor = None

    def _propose(self):
        sent = self.sender.sendMessage('Apa yang perlu saya lakukan ?', reply_markup=self.keyboard)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    
    """
    def _propose_time(self):
        current_time = time.strftime("%H:%M", t)
        (h, m) = current_time.split(':')
        result = int(h) * 3600 + int(m) * 60
        
        (h, m) = setTime1.split(':')
        timeklm1 = int(h) * 3600 + int(m) * 60
        
        (h, m) = setTime2.split(':')
        timeklm2 = int(h) * 3600 + int(m) * 60
        
        (h, m) = setTime3.split(':')
        timeklm3 = int(h) * 3600 + int(m) * 60
    """

    def _cancel_last(self):
        if self._editor:
            self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None
            self._edit_msg_ident = None

    def on_chat_message(self, msg):
        global jadwal_1
        global jadwal_2
        global jadwal_3
        global takar_1
        global takar_2
        global takar_3
        global status_1
        global status_2
        global status_3

        chat_id = msg['chat']['id']
        if msg['from']['id'] != CHATID:
            bot.sendMessage(chat_id, "Maaf ini adalah bot pribadi. Akses ditolak!")
            self.close()
        
        command = msg['text']
        if (command == 'Keluar'):
            sent = self.sender.sendMessage("Terima kasih! \nBye..")
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        #== bagian pengaturan ==
        elif (command == 'Pengaturan'):
            sent = self.sender.sendMessage('Apa yang ingin Anda atur?', reply_markup=self.keyboard1)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Set Penjadwalan Pemberian Pakan'):
            sent = self.sender.sendMessage('Kolam mana yang ingi Anda atur <b><i>Penjadwalan</i></b> Pakannya ?', parse_mode='html', reply_markup=self.keyboard2)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Set Dosis Pemberian Pakan'):
            sent = self.sender.sendMessage('Kolam mana yang ingi Anda atur <b><i>Dosis</i></b> Pakannya ?', parse_mode='html', reply_markup=self.keyboard3)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Jadwal Kolam 1'):
            status_1 = True
            status_2 = False
            status_3 = False
            sent = self.sender.sendMessage('Silahkan pilih waktu penjadwalan pakan..', reply_markup=self.keyboard4 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Jadwal Kolam 2'):
            status_1 = False
            status_2 = True
            status_3 = False
            sent = self.sender.sendMessage('Silahkan pilih waktu penjadwalan pakan..', reply_markup=self.keyboard4 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Jadwal Kolam 3'):
            status_1 = False
            status_2 = False
            status_3 = True
            sent = self.sender.sendMessage('Silahkan pilih waktu penjadwalan pakan..', reply_markup=self.keyboard4 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Jadwal Semua Kolam'):
            status_1 = True
            status_2 = True
            status_3 = True
            sent = self.sender.sendMessage('Silahkan pilih waktu penjadwalan pakan..', reply_markup=self.keyboard4 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        #== end pengaturan ==
        else :
            self._propose()
        
        #self._cancel_last()      

    def on_callback_query(self, msg):
        global jadwal_1
        global jadwal_2
        global jadwal_3
        global takar_1
        global takar_2
        global takar_3
        global status_1
        global status_2
        global status_3
        
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            
        # == Setting Penjadwalan ==              
        if query_data == '1':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 1
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 1
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 1
                status_3 = False
            text += 'telah diset ke jam 01:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == 'dosis':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Kolam mana yang ingin anda atur dosis pakannya?', reply_markup=self.keyboard4)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        # ==pemberian pakan==            
        elif query_data == 'pakan':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Kolam mana yang ingin anda beri pakan?', reply_markup=self.keyboard2)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
                 
        elif query_data == 'pknk1':
            if setTime1 == 'null' :
                self.bot.answerCallbackQuery(query_id, text='Ok. Pemberian pakan pada kolam 1 akan dilakukan...')
                self._cancel_last()
                #!! kasi pakan, kamera jalan,
                stat1 = 1
                self.sender.sendMessage('Pemberian pakan pada kolam 1 telah selesai \nketikkan perintah /dokumentasi untuk mendapat rekaman video..')
                self.close()
            else :
                if stat1 == 0 :
                    self.bot.answerCallbackQuery(query_id, text='Peringatan !!!')
                    self._cancel_last()
                    self.sender.sendMessage('Pemberian pakan pada kolam 1 Telah dijadwlkan pada pukul' + setTime1 + '\nketikkan perintah /force1 untuk memberikan pakan sekarang juga..')
                    self.close()
            
        else:
            self.bot.answerCallbackQuery(query_id, text='Ok. Tapi aku akan terus bertanya.')
            self._cancel_last()
            self._propose()
    
    def on__idle(self, event):
        global status_1
        global status_2
        global status_3
        if status_1 or status_2 or status_3 :
            self.sender.sendMessage('Saya tahu Anda mungkin perlu sedikit waktu. Aku akan selalu di sini untukmu.')
            self._cancel_last()
        self.close()
    
    def on_close(self, ex):
        # Save to database
        global propose_records
        propose_records[self.id] = (self._edit_msg_ident)


bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, Lover, timeout=30),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

#while 1: <--sama dengan true
while True:
    now = datetime.datetime.now()
    print(now.hour,":",now.minute)
    print(jadwal_1,":",jadwal_2,":",jadwal_3,":",takar_1,":",takar_2,":",takar_3)
    if (now.hour == schedule):
        schedule = schedule + 1
        if (schedule == 24):
            schedule = 0
        from  colorDetection import deteksi
        if (deteksi):
            print("terdeteksi")
            #bot.sendMessage(CHATID, 'PERINGATAN !! SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM ANDA')
            bot.sendPhoto(CHATID, open('citra.jpg', 'rb'), caption = 'PERINGATAN !! SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM ANDA')
        else :
            print("tidak Terdeteksi")
    time.sleep(60)
