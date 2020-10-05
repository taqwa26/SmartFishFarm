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

setTime1 = '2:12'
stat1 = 0
setTime2 = '2:12'
stat2 = 0
setTime3 = '2:12'
stat3 = 0

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

class Lover(telepot.helper.ChatHandler):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[ #<-- Menu awal
                   InlineKeyboardButton(text='Beri pakan', callback_data='pakan'),
                   InlineKeyboardButton(text='Pengaturan', callback_data='setting')], [
                   InlineKeyboardButton(text='um ...', callback_data='no'),
                   InlineKeyboardButton(text='keluar', callback_data='keluar')
               ]])
    keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[ #<-- Terusan Pengaturan dari Menu Awal
                   InlineKeyboardButton(text='Set penjadwalan pemberian pakan?', callback_data='waktu')], [
                   InlineKeyboardButton(text='Set dosis pemberian pakan?', callback_data='dosis')
               ]])
    keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[
                   InlineKeyboardButton(text='Kolam 1', callback_data='pknk1'),
                   InlineKeyboardButton(text='Kolam 2', callback_data='pknk2')], [
                   InlineKeyboardButton(text='Kolam 3', callback_data='pknk3'),
                   InlineKeyboardButton(text='Semua Kolam', callback_data='pknkAll')], [
                   InlineKeyboardButton(text='Kembali', callback_data='kembali')
               ]])
    keyboard3 = InlineKeyboardMarkup(inline_keyboard=[[ #<-- Terusan Pengaturan-Waktu dari Menu Awal
                   InlineKeyboardButton(text='Kolam 1', callback_data='wkolam1'),
                   InlineKeyboardButton(text='Kolam 2', callback_data='wkolam2')], [
                   InlineKeyboardButton(text='Kolam 3', callback_data='wkolam3'),
                   InlineKeyboardButton(text='Semua Kolam', callback_data='wkolamAll')], [
                   InlineKeyboardButton(text='Kembali', callback_data='kembali')
               ]])
    keyboard4 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Kolam 1', callback_data='dkolam1'),
                   InlineKeyboardButton(text='Kolam 2', callback_data='dkolam2')], [
                   InlineKeyboardButton(text='Kolam 3', callback_data='dkolam3'),
                   InlineKeyboardButton(text='Semua Kolam', callback_data='dkolamAll')], [
                   InlineKeyboardButton(text='Kembali', callback_data='kembali')
               ]])
    keyboard5 = ReplyKeyboardMarkup(keyboard=[[
                   KeyboardButton(text="1:00", callback_data='1'),
                   KeyboardButton(text="2:00", callback_data='2'),
                   KeyboardButton(text="3:00", callback_data='3'),
                   KeyboardButton(text="4:00", callback_data='4'),
                   KeyboardButton(text="5:00", callback_data='5'),
                   KeyboardButton(text="6:00", callback_data='6'),
                   KeyboardButton(text="7:00", callback_data='7'),
                   KeyboardButton(text="8:00", callback_data='8')],[
                   KeyboardButton(text="9:00", callback_data='9'),
                   KeyboardButton(text="10:00", callback_data='10'),
                   KeyboardButton(text="11:00", callback_data='11'),
                   KeyboardButton(text="12:00", callback_data='12'),
                   KeyboardButton(text="13:00", callback_data='13'),
                   KeyboardButton(text="14:00", callback_data='14'),
                   KeyboardButton(text="15:00", callback_data='15'),
                   KeyboardButton(text="16:00", callback_data='16')],[
                   KeyboardButton(text="17:00", callback_data='17'),
                   KeyboardButton(text="18:00", callback_data='18'),
                   KeyboardButton(text="19:00", callback_data='19'),
                   KeyboardButton(text="20:00", callback_data='20'),
                   KeyboardButton(text="21:00", callback_data='21'),
                   KeyboardButton(text="22:00", callback_data='22'),
                   KeyboardButton(text="23:00", callback_data='23'),
                   KeyboardButton(text="24:00", callback_data='0')
               ]])

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
        sent = self.sender.sendMessage('Apa yang bisa saya bantu?', reply_markup=self.keyboard)
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
        if msg['from']['id'] != CHATID:
            bot.sendMessage(chat_id, "Maaf ini adalah bot pribadi. Akses ditolak!")
            self.close()
        self._cancel_last()      
        self._propose()
        
        '''
        command = msg['text']
        if (command == '/hi'):
            bot.sendMessage(chat_id, "Hi")
        '''

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data == 'keluar':
            self._cancel_last()
            self.sender.sendMessage('Terima kasih! \nBye..')
            self.close()
            
        # == Setting ==              
        elif query_data == 'setting':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Apa yang ingin anda atur?', reply_markup=self.keyboard1)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        elif query_data == 'waktu':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Kolam mana yang ingin anda atur penjadwalan pakannya?', reply_markup=self.keyboard3)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        elif query_data == 'wkolam1':
            self.bot.answerCallbackQuery(query_id, text='Penjadwalan akan diset ke waktu terpilih')
            self._cancel_last()
            sent = self.sender.sendMessage('Silhkan pilih waktu yang diinginkan.. ', reply_markup=self.keyboard5)
            
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
            per_chat_id(types=['private']), create_open, Lover, timeout=10),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

#while 1: <--sama dengan true

while True:
    now = datetime.datetime.now()
    print(now.hour,":",now.minute)
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
    time.sleep(1)
