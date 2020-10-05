import RPi.GPIO as GPIO
import time, datetime
import os
import sys
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

#t = time.localtime()

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
now = datetime.datetime.now()
schedule = now.hour

jadwal_1 = 4
jadwal_2 = 4
jadwal_3 = 9
takar_1 = 2
takar_2 = 2
takar_3 = 2
status_1 = False
status_2 = False
status_3 = False

statusP_1 = False
statusP_2 = False
statusP_3 = False
statusK_1 = True
statusK_2 = True
statusK_3 = True

statusO_1 = True

class Lover(telepot.helper.ChatHandler):
    keyboard = ReplyKeyboardMarkup(keyboard=[[ #<-- Menu awal
                   KeyboardButton(text='Beri Pakan'),
                   KeyboardButton(text='Pengaturan')], [
                   KeyboardButton(text='Status'),
                   KeyboardButton(text='Keluar')
               ]], one_time_keyboard=True)
    keyboard0 = ReplyKeyboardRemove()
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
               ]], resize_keyboard=True)
    keyboard5 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Sedikit', callback_data='A')],[
                   InlineKeyboardButton(text='Sedang', callback_data='B')],[ 
                   InlineKeyboardButton(text='Banyak', callback_data='C')],[
                   InlineKeyboardButton(text='Kembali', callback_data='kembali')
               ]], resize_keyboard=True)
    keyboard6 = ReplyKeyboardMarkup(keyboard=[[ 
                   KeyboardButton(text='Pakan Kolam 1'),
                   KeyboardButton(text='Pakan Kolam 2')], [
                   KeyboardButton(text='Pakan Kolam 3'),
                   KeyboardButton(text='Pakan Semua Kolam')], [
                   KeyboardButton(text='Kembali')
               ]], one_time_keyboard=True)
    keyboard7 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Berikan Pakan Dan Batalkan Penjadwalan Hari Ini', callback_data='BB')],[
                   InlineKeyboardButton(text='Berikan Pakan Tapi Tidak Membatalkan Penjadwlan Hari Ini', callback_data='BT')],[ 
                   InlineKeyboardButton(text='Batal', callback_data='batal'),
                ]], resize_keyboard=True)
    keyboard8 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Berikan Pakan Lagi', callback_data='BL')],[
                   InlineKeyboardButton(text='Batal', callback_data='batal'),
                ]], resize_keyboard=True)
    keyboard9 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Ambil Gambar Kolam', callback_data='AG')],[
                   InlineKeyboardButton(text='Ambil Video Kolam', callback_data='AV')],[ 
                   InlineKeyboardButton(text='Batal', callback_data='batal'),
                ]], resize_keyboard=True)


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
        global statusP_1
        global statusP_2
        global statusP_3
        global statusO_1

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
            sent = self.sender.sendMessage('Silahkan pilih waktu penjadwalan pakan..', reply_markup=self.keyboard4 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Jadwal Kolam 2'):
            status_2 = True
            sent = self.sender.sendMessage('Silahkan pilih waktu penjadwalan pakan..', reply_markup=self.keyboard4 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Jadwal Kolam 3'):
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
        elif (command == 'Dosis Kolam 1'):
            status_1 = True
            sent = self.sender.sendMessage('Silahkan pilih dosis penjadwalan pakan..', reply_markup=self.keyboard5 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Dosis Kolam 2'):
            status_2 = True
            sent = self.sender.sendMessage('Silahkan pilih dosis penjadwalan pakan..', reply_markup=self.keyboard5 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Dosis Kolam 3'):
            status_3 = True
            sent = self.sender.sendMessage('Silahkan pilih dosis penjadwalan pakan..', reply_markup=self.keyboard5 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Dosis Semua Kolam'):
            status_1 = True
            status_2 = True
            status_3 = True
            sent = self.sender.sendMessage('Silahkan pilih dosis penjadwalan pakan..', reply_markup=self.keyboard5 )
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        #== end pengaturan ==
            
        #== Bagian Beri Pakan ==
        elif (command == 'Beri Pakan'):
            sent = self.sender.sendMessage('Kolam mana yang ingi Anda <b><i>Beri Pakan</i></b> ?', parse_mode='html', reply_markup=self.keyboard6)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Pakan Kolam 1'):
            status_1 = True
            if statusP_1 == False :
                sent = self.sender.sendMessage('Pemberian Pakan pada Kolam 1 telah terjadwal...', reply_markup=self.keyboard7)
            else :
                sent = self.sender.sendMessage('Pemberian Pakan pada Kolam 1 telah dilakukan...', reply_markup=self.keyboard8)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Pakan Kolam 2'):
            status_2 = True
            if statusP_2 == False :
                sent = self.sender.sendMessage('Pemberian Pakan pada Kolam 2 telah terjadwal...', reply_markup=self.keyboard7)
            else :
                sent = self.sender.sendMessage('Pemberian Pakan pada Kolam 2 telah dilakukan...', reply_markup=self.keyboard8)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Pakan Kolam 3'):
            status_3 = True
            if statusP_3 == False :
                sent = self.sender.sendMessage('Pemberian Pakan pada Kolam 3 telah terjadwal...', reply_markup=self.keyboard7)
            else :
                sent = self.sender.sendMessage('Pemberian Pakan pada Kolam 3 telah dilakukan...', reply_markup=self.keyboard8)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Pakan Semua Kolam'):
            status_1 = True
            status_2 = True
            status_3 = True
            if statusP_1 == False or statusP_2 == False or status_3 == False :
                sent = self.sender.sendMessage('Pemberian Pakan pada semua Kolam telah terjadwal...', reply_markup=self.keyboard7)
            else :
                pesan = ''
                if statusP_1 == True :
                    pesan +='Pemberian Pakan pada Kolam 1 telah dilakukan... \n'
                if statusP_2 == True :
                    pesan +='Pemberian Pakan pada Kolam 2 telah dilakukan... \n'
                if statusP_3 == True :
                    pesan +='Pemberian Pakan pada Kolam 3 telah dilakukan... \n'
                sent = self.sender.sendMessage(pesan, parse_mode='html', reply_markup=self.keyboard8)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            
        elif (command == 'Lanjutkan..'):
            sent = self.sender.sendMessage('Pemberian pakan sedang berjalan..', reply_markup=self.keyboard0)
            text = 'Pemberian Pakan secara terjadwal pada kolam '
            if status_1 :
                # motor sevo jalan kolam 1 takar 1
                # ambil video
                text += '1, '
                status_1 = False
                statusP_1 = True
                statusO_1 = False
            if status_2 :
                # motor sevo jalan kolam 2 takar 2
                # ambil video
                text += '2, '
                status_2 = False
                statusP_2 = True
                statusO_1 = False
            if status_3 :
                # motor sevo jalan kolam 3 takar 3
                # ambil video
                text += '3, '
                status_3 = False
                statusP_3 = True
                statusO_1 = False
            text += 'telah selesai dilakukan..'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Batalkan..'):
            if status_1 :
                status_1 = False
                statusP_1 = True
                statusO_1 = False
            if status_2 :
                status_2 = False
                statusP_2 = True
                statusO_1 = False
            if status_3 :
                status_3 = False
                statusP_3 = True
                statusO_1 = False
            sent = self.sender.sendMessage('Pemberian Pakan secara terjadwal dibatalkan', reply_markup=self.keyboard0)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        #== end Beri Pakan ==
            
        #== Bagian Status ==
        elif (command == 'Status'):
            status  = '+=== <b>Smart Fish Farm</b> ===+ \n'
            status += 'Status Kolam 1 : \n'
            status += '-> Satatus = '
            sent = self.sender.sendMessage(status, parse_mode='html', reply_markup=self.keyboard9)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        #== end Bagian Status ==
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
        global statusP_1
        global statusP_2
        global statusP_3
        
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
        
        elif query_data == '2':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 2
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 2
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 2
                status_3 = False
            text += 'telah diset ke jam 02:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '3':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 3
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 3
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 3
                status_3 = False
            text += 'telah diset ke jam 03:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '4':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 4
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 4
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 4
                status_3 = False
            text += 'telah diset ke jam 04:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        
        elif query_data == '5':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 5
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 5
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 5
                status_3 = False
            text += 'telah diset ke jam 05:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '6':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 6
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 6
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 6
                status_3 = False
            text += 'telah diset ke jam 06:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '7':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 7
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 7
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 7
                status_3 = False
            text += 'telah diset ke jam 07:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        
        elif query_data == '8':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 8
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 8
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 8
                status_3 = False
            text += 'telah diset ke jam 08:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        
        elif query_data == '9':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 9
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 9
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 9
                status_3 = False
            text += 'telah diset ke jam 09:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        
        elif query_data == '10':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 10
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 10
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 10
                status_3 = False
            text += 'telah diset ke jam 10:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '11':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 11
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 11
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 11
                status_3 = False
            text += 'telah diset ke jam 11:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '12':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 12
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 12
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 12
                status_3 = False
            text += 'telah diset ke jam 12:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '13':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 13
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 13
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 13
                status_3 = False
            text += 'telah diset ke jam 13:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '14':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 14
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 14
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 14
                status_3 = False
            text += 'telah diset ke jam 14:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '15':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 15
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 15
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 15
                status_3 = False
            text += 'telah diset ke jam 15:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '16':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 16
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 16
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 16
                status_3 = False
            text += 'telah diset ke jam 16:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '17':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 17
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 17
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 17
                status_3 = False
            text += 'telah diset ke jam 17:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '18':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 18
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 18
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 18
                status_3 = False
            text += 'telah diset ke jam 18:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '19':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 19
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 19
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 19
                status_3 = False
            text += 'telah diset ke jam 19:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '20':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 20
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 20
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 20
                status_3 = False
            text += 'telah diset ke jam 20:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '21':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 21
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 21
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 21
                status_3 = False
            text += 'telah diset ke jam 21:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '22':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 22
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 22
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 22
                status_3 = False
            text += 'telah diset ke jam 22:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '23':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 23
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 23
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 23
                status_3 = False
            text += 'telah diset ke jam 23:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == '0':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Penjadwalan pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                jadwal_1 = 0
                status_1 = False
            if (status_2):
                text += '2, '
                jadwal_2 = 0
                status_2 = False
            if (status_3):
                text += '3, '
                jadwal_3 = 0
                status_3 = False
            text += 'telah diset ke jam 00:00'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        # == End Setting Penjadwalan ==
        
        # == Setting Dosis ==
        elif query_data == 'A':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Dosis pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                takar_1 = 1
                status_1 = False
            if (status_2):
                text += '2, '
                takar_2 = 1
                status_2 = False
            if (status_3):
                text += '3, '
                takar_3 = 1
                status_3 = False
            text += 'telah diset dengan takran Kecil'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == 'B':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Dosis pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                takar_1 = 2
                status_1 = False
            if (status_2):
                text += '2, '
                takar_2 = 2
                status_2 = False
            if (status_3):
                text += '3, '
                takar_3 = 2
                status_3 = False
            text += 'telah diset denga takaran Sedang'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == 'C':
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            self._cancel_last()
            text = 'Dosis pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                takar_1 = 3
                status_1 = False
            if (status_2):
                text += '2, '
                takar_2 = 3
                status_2 = False
            if (status_3):
                text += '3, '
                takar_3 = 3
                status_3 = False
            text += 'telah diset dengan takaran Besar'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        # == End Setting Dosis ==
        
        # == Beri Pakan ==
        elif query_data == 'BB':
            self.bot.answerCallbackQuery(query_id, text='Ok. Perintah Dijalankan..')
            self._cancel_last()
            text = 'Pemberian Pakan pada Kolam '
            if (status_1):
                text += '1, '
                # motor servo jalan
                # ambil video
                statusP_1 = True
                status_1 = False
            if (status_2):
                text += '2, '
                # motor servo jalan
                # ambil video
                statusP_2 = True
                status_2 = False
            if (status_3):
                text += '3, '
                # motor servo jalan
                # ambil video
                statusP_3 = True
                status_3 = False
            text += 'telah dilakukan'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == 'BT':
            self.bot.answerCallbackQuery(query_id, text='Ok. Perintah Dijalankan..')
            self._cancel_last()
            text = 'Pemberian Pakan pada Kolam '
            if (status_1):
                text += '1, '
                # motor servo jalan
                # ambil video
                status_1 = False
            if (status_2):
                text += '2, '
                # motor servo jalan
                # ambil video
                status_2 = False
            if (status_3):
                text += '3, '
                # motor servo jalan
                # ambil video
                status_3 = False
            text += 'telah dilakukan'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        elif query_data == 'BL':
            self.bot.answerCallbackQuery(query_id, text='Ok. Perintah Dijalankan..')
            self._cancel_last()
            text = 'Pemberian Pakan pada Kolam '
            if (status_1):
                text += '1, '
                # motor servo jalan
                # ambil video
                status_1 = False
            if (status_2):
                text += '2, '
                # motor servo jalan
                # ambil video
                status_2 = False
            if (status_3):
                text += '3, '
                # motor servo jalan
                # ambil video
                status_3 = False
            text += 'telah dilakukan lagi'
            sent = self.sender.sendMessage(text)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        
        elif query_data == 'batal':
            status_1 = False
            status_2 = False
            status_3 = False
            self._cancel_last()
            self.close()
        # == end Beri Pakan ==
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
            status_1 = False
            status_2 = False
            status_3 = False
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
bootingdown  = 'Sistem BootingUp...\n'
bot.sendMessage(CHATID, bootingdown, parse_mode='html')
bootingup  = 'aFiFa Telah Aktif \n'
bootingup += 'Seluruh Pengaturan Telah Diset Default \n'
bot.sendMessage(CHATID, bootingup, parse_mode='html')

#while 1: <--sama dengan true
while True:
    now = datetime.datetime.now()
    print(now.hour,":",now.minute)
    print(jadwal_1,":",jadwal_2,":",jadwal_3,":",takar_1,":",takar_2,":",takar_3,"||",status_1,":",status_2,":",status_3,"||",statusP_1,":",statusP_2,":",statusP_3)
    
    # == Pencitraan Automatis ==
    if (now.hour == schedule):
        statusO_1 = True
        schedule = schedule + 1
        if (schedule == 24):
            schedule = 0

        #ambil Gambar
        from  Pencitraan1 import deteksi1
        if (deteksi1):
            statusK_1 = False
            print("terdeteksi")
            bot.sendPhoto(CHATID, open('citra1.jpg', 'rb'), caption = 'Pencitraan Kolam 1')
            bot.sendMessage(CHATID, '<b>PERINGATAN !!</b> SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM 1 ANDA', parse_mode='html')
        else :
            statusK_1 = True
            print("tidak Terdeteksi")
            
        #ambil Gambar
        from  Pencitraan2 import deteksi2
        if (deteksi2):
            statusK_2 = False
            print("terdeteksi")
            bot.sendPhoto(CHATID, open('citra2.jpg', 'rb'), caption = 'Pencitraan Kolam 2')
            bot.sendMessage(CHATID, '<b>PERINGATAN !!</b> SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM 2 ANDA', parse_mode='html')
        else :
            statusK_2 = True
            print("tidak Terdeteksi")
            
        #ambil Gambar
        from  Pencitraan3 import deteksi3
        if (deteksi3):
            statusK_3 = False
            print("terdeteksi")
            bot.sendPhoto(CHATID, open('citra3.jpg', 'rb'), caption = 'Pencitraan Kolam 3')
            bot.sendMessage(CHATID, '<b>PERINGATAN !!</b> SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM 3 ANDA', parse_mode='html')
        else :
            statusK_3 = True
            print("tidak Terdeteksi")
    # == end Pencitraan Automatis
        
    # == Pemberian Pakan Automatis ==
    if jadwal_1 != jadwal_2 != jadwal_3 :
        if (statusP_1 == False and jadwal_1 == now.hour):
            status_1 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 telah dilakukan secara otomatis')
                statusP_1 = True
        if (statusP_2 == False and jadwal_2 == now.hour):
            status_2 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 2 takar_2
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 telah dilakukan secara otomatis')
                statusP_2 = True
        if (statusP_3 == False and jadwal_3 == now.hour):
            stauts_3 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 3 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 telah dilakukan secara otomatis')
                statusP_3 = True
    
    elif jadwal_1 == jadwal_2 != jadwal_3 :
        if (statusP_1 == False and jadwal_1 == now.hour):
            status_1 = True
            status_2 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 telah dilakukan secara otomatis')
                statusP_1 = True
                statusP_2 = True
        if (statusP_3 == False and jadwal_3 == now.hour):
            status_3 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 telah dilakukan secara otomatis')
                statusP_3 = True
    elif jadwal_1 != jadwal_2 == jadwal_3 :
        if (statusP_2 == False and jadwal_2 == now.hour):
            status_3 = True
            status_2 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 telah dilakukan secara otomatis')
                statusP_3 = True
                statusP_2 = True
        if (statusP_1 == False and jadwal_1 == now.hour):
            status_1 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 telah dilakukan secara otomatis')
                statusP_1 = True
    elif jadwal_1 == jadwal_3 != jadwal_2 :
        if (statusP_1 == False and jadwal_1 == now.hour):
            status_1 = True
            status_3 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 telah dilakukan secara otomatis')
                statusP_1 = True
                statusP_3 = True
        if (statusP_2 == False and jadwal_2 == now.hour):
            status_2 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 telah dilakukan secara otomatis')
                statusP_2 = True
                
    else :
        if (statusP_1 == False and jadwal_1 == now.hour):
            status_1 = True
            status_2 = True
            status_3 = True
            keyboard = ReplyKeyboardMarkup(keyboard=[[ 
                       KeyboardButton(text='Lanjutkan..')],[
                       KeyboardButton(text='Batalkan..')
                   ]], one_time_keyboard=True)
            keyboard1 = ReplyKeyboardRemove()
            bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1, 2 dan 3 akan dilakukan Lanjutkan ? \nAku akan melanjutkannya secara automatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboard)
            time.sleep(600)
            if(statusO_1):
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1, 2 dan 3 sedang berjalan..', reply_markup = keyboard1)
                # motor servo jalan berdasarkan kolam 1 takar_1
                # ambil viedeo
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1, 2 dan 3 telah dilakukan secara otomatis')
                statusP_1 = True
                statusP_2 = True
                statusP_3 = True
                
    # == end Pembarian Pakan Automatis ==
            
    time.sleep(60)

