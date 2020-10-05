import RPi.GPIO as GPIO
import time, datetime
import os
import sys
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

t = time.localtime()

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

class Lover(telepot.helper.ChatHandler):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                   InlineKeyboardButton(text='Beri pakan', callback_data='pakan'),
                   InlineKeyboardButton(text='Pengaturan', callback_data='setting')], [
                   InlineKeyboardButton(text='um ...', callback_data='no'),
                   InlineKeyboardButton(text='keluar', callback_data='keluar')
               ]])
    keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[
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
    keyboard3 = InlineKeyboardMarkup(inline_keyboard=[[
                   InlineKeyboardButton(text='Kolam 1', callback_data='kolam1'),
                   InlineKeyboardButton(text='Kolam 2', callback_data='kolam2')], [
                   InlineKeyboardButton(text='Kolam 3', callback_data='kolam3'),
                   InlineKeyboardButton(text='Semua Kolam', callback_data='kolamAll')], [
                   InlineKeyboardButton(text='Kembali', callback_data='kembali')
               ]])
    keyboard4 = InlineKeyboardMarkup(inline_keyboard=[[
                   InlineKeyboardButton(text='Kolam 1', callback_data='kolam1'),
                   InlineKeyboardButton(text='Kolam 2', callback_data='kolam2')], [
                   InlineKeyboardButton(text='Kolam 3', callback_data='kolam3'),
                   InlineKeyboardButton(text='Semua Kolam', callback_data='kolamAll')], [
                   InlineKeyboardButton(text='Kembali', callback_data='kembali')
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
        if msg['from']['id'] != 1137202289:
            bot.sendMessage(chat_id, "Maaf ini adalah bot pribadi. Akses ditolak!")
            self.close()
        self._cancel_last()
        self._propose()

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data == 'keluar':
            self._cancel_last()
            self.sender.sendMessage('Terima kasih! \nBye..')
            self.close()
                      
        elif query_data == 'setting':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Apa yang ingin anda *atur?', reply_markup=self.keyboard1)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        elif query_data == 'pakan':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Kolam mana yang ingin anda beri pakan?', reply_markup=self.keyboard2)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        elif query_data == 'waktu':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Kolam mana yang ingin anda atur *penjadwalan pakannya?', reply_markup=self.keyboard3)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        elif query_data == 'dosis':
            self.bot.answerCallbackQuery(query_id, text='Ok. Pertanyaan berikutnya...')
            self._cancel_last()
            sent = self.sender.sendMessage('Kolam mana yang ingin anda atur *dosis pakannya?', reply_markup=self.keyboard4)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        # ==pemberian pakan==
        
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


TOKEN = '1202817061:AAHLFAFoftMnaOenIt59XG_IzGIp8a7yM2M'

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, Lover, timeout=10),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
