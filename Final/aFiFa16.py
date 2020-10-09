import RPi.GPIO as GPIO
import time, datetime
import shlex
import os
import sys
import telepot
import telepot.helper
from subprocess import Popen, DEVNULL, STDOUT
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import (per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

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
schedule = now.hour # time schedule citradigital
t = now.strftime('%d-%m-%Y di jam %H:%M:%S') # time sistem gangguan
t1 = now.strftime('%d-%m-%Y | %H:%M:%S') # time sistem saat booting

jadwal_1 = 9 # jadwal pakan
jadwal_2 = 9
jadwal_3 = 9

takar_1 = 'Sedang' # takaran pakan
takar_2 = 'Sedang'
takar_3 = 'Sedang'

status_1 = False # status yang meperbolehkan tidakan beresiko berjalan
status_2 = False
status_3 = False
status_4 = False # status supaya tidak error untuk menu status
status_5 = False # status apabila ada proses yang berjalan misal : memberi pakan, ambil video ##-->belum terpakai
status_6 = False # status apakah video dokumentasi mau dikirimkan atau tidak
status_7 = False # status apakah telh terjadi gangguan sinyal dan membuat sistem beralih ke mode offline
status_8 = True # status apakah sistem baru booting atau tidak


statusP_1 = False # status pakan apakah sudah? belum?
statusP_2 = False
statusP_3 = False

statusK_1 = True # status kondisi kolam berdasarkan citradigital baik? tidak?
statusK_2 = True
statusK_3 = True

statusO_1 = True # status apabila automatis telah disetujui atau tidak (agar tidak terjadi double)
statusO_2 = True # status apabila otomatis dinyalakan atau dimatikan
statusO_3 = False # statut apabila automatis sedang berjalan

keyboard1 = ReplyKeyboardMarkup(keyboard=[[ #<-- Terusan Pengaturan dari Menu Awal
                   KeyboardButton(text='Set Penjadwalan Pemberian Pakan')], [
                   KeyboardButton(text='Set Dosis Pemberian Pakan')],[
                   KeyboardButton(text='Pemberian Pakan Otomatis : OFF')
               ]], one_time_keyboard=True)
keyboardO_1 = ReplyKeyboardMarkup(keyboard=[[ 
                    KeyboardButton(text='Lanjutkan..')],[
                    KeyboardButton(text='Batalkan..')
                ]], one_time_keyboard=True)
keyboardO_2 = ReplyKeyboardRemove()
keyboardO_3 = ReplyKeyboardMarkup(keyboard=[[
                    KeyboardButton(text='Ya, Tentu..'),
                    KeyboardButton(text='Tidak Perlu..')
                ]], one_time_keyboard=True)

class Lover(telepot.helper.ChatHandler):
    keyboard = ReplyKeyboardMarkup(keyboard=[[ #<-- Menu awal
                   KeyboardButton(text='Beri Pakan'),
                   KeyboardButton(text='Pengaturan')], [
                   KeyboardButton(text='Status'),
                   KeyboardButton(text='Keluar')
               ]], one_time_keyboard=True)
    keyboard0 = ReplyKeyboardRemove()
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
                   InlineKeyboardButton(text='Batal', callback_data='batal')
               ]], )
    keyboard5 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Sedikit', callback_data='A')],[
                   InlineKeyboardButton(text='Sedang', callback_data='B')],[ 
                   InlineKeyboardButton(text='Banyak', callback_data='C')],[
                   InlineKeyboardButton(text='Batal', callback_data='batal')
               ]], )
    keyboard6 = ReplyKeyboardMarkup(keyboard=[[ 
                   KeyboardButton(text='Pakan Kolam 1'),
                   KeyboardButton(text='Pakan Kolam 2')], [
                   KeyboardButton(text='Pakan Kolam 3'),
                   KeyboardButton(text='Pakan Semua Kolam')], [
                   KeyboardButton(text='Kembali')
               ]], one_time_keyboard=True)
    keyboard7 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Berikan Pakan Dan Batalkan Penjadwalan Hari Ini', callback_data='BB')],[
                   InlineKeyboardButton(text='Berikan Pakan Tapi Tidak Membatalkan Penjadwlan', callback_data='BT')],[ 
                   InlineKeyboardButton(text='Batal', callback_data='batal'),
                ]], )
    keyboard8 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Berikan Pakan Lagi', callback_data='BL')],[
                   InlineKeyboardButton(text='Batal', callback_data='batal'),
                ]], )
    keyboard9 = InlineKeyboardMarkup(inline_keyboard=[[ #-- Terusan Pengaturan-Takaran dari Menu Awal
                   InlineKeyboardButton(text='Ambil Gambar Kolam', callback_data='AG')],[
                   InlineKeyboardButton(text='Ambil Video Kolam', callback_data='AV')],[ 
                   InlineKeyboardButton(text='Batal', callback_data='batal'),
                ]], )


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
        global status_4
        global status_5
        global status_6
        global statusP_1
        global statusP_2
        global statusP_3
        global statusO_1
        global statusO_2
        global statusO_3
        global keyboard1     

        chat_id = msg['chat']['id']
        if msg['from']['id'] != CHATID:
            bot.sendMessage(chat_id, "Maaf ini adalah bot pribadi. Akses ditolak!")
            self.close()
        
        troubleshoot = msg['text']
        if (troubleshoot == 'troubleshoot'):
            shoot = str(status_1)+' : '+str(status_2)+' : '+str(status_3)+' : '+str(status_4)+' : '+str(status_5)+' : '+str(status_6)+' : '+str(status_7)+' : '+str(status_8)+' : '+str(statusO_1)+' : '+str(statusO_2)+' : '+str(statusO_3)
            sent = self.sender.sendMessage(shoot)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
        
        print('pesan masuk')
        if (status_5) :
            sent = self.sender.sendMessage('Tunggu sebentar.. aku sedang melakukan pemrosesan otomatis atau proses sebelumnya belum selasai. \n\n Kirimi aku pesan beberapa saat lagi..', parse_mode='html')
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        if (statusO_3 == False and status_5 == False) :
            if (status_1 or status_2 or status_3 or status_4) : 
                self._cancel_last()
                status_1 = False
                status_2 = False
                status_3 = False
                status_4 = False
        
        command = msg['text']
        if (command == 'Keluar'):
            sent = self.sender.sendMessage("Have a nice day \nBye..", reply_markup=self.keyboard0)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
            self.close()
            
        #== bagian pengaturan ==
        elif (command == 'Pengaturan'):
            sent = self.sender.sendMessage('Apa yang ingin Anda atur?', reply_markup=keyboard1)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Pemberian Pakan Otomatis : OFF'):
            sent = self.sender.sendMessage('Pemberian <i>Pakan Otomatis</i> Telah <b>Dimatikan</b>', parse_mode='html', reply_markup=self.keyboard0)
            statusO_2 = False
            keyboard1 = ReplyKeyboardMarkup(keyboard=[[ #<-- Terusan Pengaturan dari Menu Awal
                            KeyboardButton(text='Set Penjadwalan Pemberian Pakan')], [
                            KeyboardButton(text='Set Dosis Pemberian Pakan')],[
                            KeyboardButton(text='Pemberian Pakan Otomatis : ON')
                        ]], one_time_keyboard=True)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Pemberian Pakan Otomatis : ON'):
            sent = self.sender.sendMessage('Pemberian <i>Pakan Otomatis</i> Telah <b>Dinyalakan</b>', parse_mode='html', reply_markup=self.keyboard0)
            statusO_2 = True
            keyboard1 = ReplyKeyboardMarkup(keyboard=[[ #<-- Terusan Pengaturan dari Menu Awal
                            KeyboardButton(text='Set Penjadwalan Pemberian Pakan')], [
                            KeyboardButton(text='Set Dosis Pemberian Pakan')],[
                            KeyboardButton(text='Pemberian Pakan Otomatis : OFF')
                        ]], one_time_keyboard=True)
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
            
        elif (command == 'Lanjutkan..' and statusO_3):
            if status_5 == False :
                sent = self.sender.sendMessage('Pemberian pakan sedang berjalan.. ', reply_markup=self.keyboard0)
                statusO_3 = False # command 'Lanjutkan..' tidak berlaku lagi
                status_5 = True
                text = 'Pemberian Pakan secara terjadwal pada kolam '                
                # ambil Video
                pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                time.sleep(5) #delay mempersiapkan kamera
                if (status_1) :
                    statusO_1 = False
                    status_1 = False
                    # motor sevo jalan kolam 1 takar 1
                    text += '1, '
                    statusP_1 = True                    
                if (status_2) :
                    statusO_1 = False
                    status_2 = False
                    # motor sevo jalan kolam 2 takar 2
                    text += '2, '
                    statusP_2 = True                    
                if (status_3) :
                    statusO_1 = False
                    status_3 = False
                    # motor sevo jalan kolam 3 takar 3
                    text += '3, '
                    statusP_3 = True                
                # stop rekam
                p.terminate()
                time.sleep(5) # delay endcoding video
                text += 'telah selesai dilakukan..'
                status_5 = False
                sent = self.sender.sendMessage(text)
                status_6 = True
                sent = self.sender.sendMessage('Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
            else :
                self.bot.answerCallbackQuery(query_id, text='Gagal Memberikan Pakan')
                sent = self.sender.sendMessage('Proses lain sedangan berjalan..')
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Batalkan..' and statusO_3):
            print(status_1,status_2,status_3)
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
            statusO_3 = False
            sent = self.sender.sendMessage('Pemberian Pakan secara terjadwal dibatalkan', reply_markup=self.keyboard0)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Ya, Tentu..' and status_6) :
            status_6 = False
            sent = self.sender.sendVideo(open('dokumentasiVideo.mp4', 'rb'), caption = 'Dokumentasi Video', supports_streaming=True, reply_markup=self.keyboard0)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        elif (command == 'Tidak Perlu..' and status_6) :
            status_6 = False
            sent = self.sender.sendMessage("Okey \nBye..", reply_markup=self.keyboard0)
            self._editor = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)
        #== end Beri Pakan ==
            
        #== Bagian Status ==
        elif (command == 'Status'):
            status_4 = True
            if statusK_1:
                tk1 = '<b>Baik</b>'
            else:
                tk1 = '<b>Tidak Baik !</b>'
            if statusP_1:
                tp1 = '<b>Telah Diberikan</b>'
            else:
                tp1 = '<b>Belum Diberikan</b>'
            if statusK_2:
                tk2 = '<b>Baik</b>'
            else:
                tk2 = '<b>Tidak Baik !</b>'
            if statusP_2:
                tp2 = '<b>Telah Diberikan</b>'
            else:
                tp2 = '<b>Belum Diberikan</b>'
            if statusK_3:
                tk3 = '<b>Baik</b>'
            else:
                tk3 = '<b>Tidak Baik !</b>'
            if statusP_3:
                tp3 = '<b>Telah Diberikan</b>'
            else:
                tp3 = '<b>Belum Diberikan</b>'
            if statusO_2:
                to = 'ON'
            else:
                to = 'OFF'
            status  = '+=== <b>Smart Fish Farm</b> ===+ \n\n'
            status += 'Status Kolam 1 : \n'
            status += '-> Kondisi = '+tk1+'\n'
            status += '-> Jadwal Pakan = <b>'+str(jadwal_1)+':00</b>\n'
            status += '-> Takaran Pakan = <b>'+takar_1+'</b>\n'
            status += '-> Status Pakan = '+tp1+'\n\n'
            status += 'Status Kolam 2 : \n'
            status += '-> Kondisi = '+tk2+'\n'
            status += '-> Jadwal Pakan = <b>'+str(jadwal_2)+':00</b>\n'
            status += '-> Takaran Pakan = <b>'+takar_2+'</b>\n'
            status += '-> Status Pakan = '+tp2+'\n\n'
            status += 'Status Kolam 3 : \n'
            status += '-> Kondisi = '+tk3+'\n'
            status += '-> Jadwal Pakan = <b>'+str(jadwal_3)+':00</b>\n'
            status += '-> Takaran Pakan = <b>'+takar_3+'</b>\n'
            status += '-> Status Pakan = '+tp3+'\n\n'
            status += 'Pakan Otomatis : '+to            
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
        global status_5
        global status_6
        global statusP_1
        global statusP_2
        global statusP_3
        
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            
        # == Setting Penjadwalan ==              
        if query_data == '1':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
        
        elif query_data == '2':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '3':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '4':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
        
        elif query_data == '5':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '6':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '7':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
        
        elif query_data == '8':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
        
        elif query_data == '9':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
        
        elif query_data == '10':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '11':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '12':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '13':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '14':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '15':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '16':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '17':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '18':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '19':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '20':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '21':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '22':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
            
        elif query_data == '23':
            self._cancel_last()
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
            self.close()
            
        elif query_data == '0':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
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
            self.close()
        # == End Setting Penjadwalan ==
        
        # == Setting Dosis ==
        elif query_data == 'A':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            text = 'Dosis pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                takar_1 = 'Kecil'
                status_1 = False
            if (status_2):
                text += '2, '
                takar_2 = 'Kecil'
                status_2 = False
            if (status_3):
                text += '3, '
                takar_3 = 'Kecil'
                status_3 = False
            text += 'telah diset dengan takaran Kecil'
            sent = self.sender.sendMessage(text)
            self.close()
            
        elif query_data == 'B':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            text = 'Dosis pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                takar_1 = 'Sedang'
                status_1 = False
            if (status_2):
                text += '2, '
                takar_2 = 'Sedang'
                status_2 = False
            if (status_3):
                text += '3, '
                takar_3 = 'Sedang'
                status_3 = False
            text += 'telah diset denga takaran Sedang'
            sent = self.sender.sendMessage(text)
            self.close()
            
        elif query_data == 'C':
            self._cancel_last()
            self.bot.answerCallbackQuery(query_id, text='Ok. Penjadwalan tersimpan..')
            text = 'Dosis pemberian Pakan pada kolam '
            if (status_1):
                text += '1, '
                takar_1 = 'Besar'
                status_1 = False
            if (status_2):
                text += '2, '
                takar_2 = 'Besar'
                status_2 = False
            if (status_3):
                text += '3, '
                takar_3 = 'Besar'
                status_3 = False
            text += 'telah diset dengan takaran Besar'
            sent = self.sender.sendMessage(text)
            self.close()
        # == End Setting Dosis ==
        
        # == Beri Pakan ==
        elif query_data == 'BB':
            self._cancel_last()
            if(status_5 == False) :
                self.bot.answerCallbackQuery(query_id, text='Ok. Perintah Dijalankan..')
                sent = self.sender.sendMessage('Pemberian pakan sedang berjalan')
                status_5 = True
                text = 'Pemberian Pakan pada Kolam '
                # ambil Video
                pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                time.sleep(5) #delay mempersiapkan kamera
                if (status_1):
                    status_1 = False
                    text += '1, '
                    # motor servo jalan
                    statusP_1 = True
                if (status_2):
                    status_2 = False
                    text += '2, '
                    # motor servo jalan
                    statusP_2 = True
                if (status_3):
                    status_3 = False
                    text += '3, '
                    # motor servo jalan
                    statusP_3 = True
                # stop rekam
                p.terminate()
                time.sleep(5) # delay endcoding video
                text += 'telah dilakukan'
                status_5 = False
                sent = self.sender.sendMessage(text)
                status_6 = True
                sent = self.sender.sendMessage('Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
            else :
                self.bot.answerCallbackQuery(query_id, text='Gagal Memberikan Pakan')
                sent = self.sender.sendMessage('Proses lain sedangan berjalan..')
            self.close()
            
        elif query_data == 'BT':
            self._cancel_last()
            if (status_5 == False) :
                self.bot.answerCallbackQuery(query_id, text='Ok. Perintah Dijalankan..')
                sent = self.sender.sendMessage('Pemberian pakan sedang berjalan')
                status_5 = True
                text = 'Pemberian Pakan pada Kolam '
                # ambil Video
                pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                time.sleep(5) #delay mempersiapkan kamera
                if (status_1):
                    status_1 = False
                    text += '1, '
                    # motor servo jalan
                if (status_2):
                    status_2 = False
                    text += '2, '
                    # motor servo jalan
                if (status_3):
                    status_3 = False
                    text += '3, '
                    # motor servo jalan
                # stop rekam
                p.terminate()
                time.sleep(5) # delay endcoding video
                text += 'telah dilakukan'
                status_5 = False
                sent = self.sender.sendMessage(text)
                status_6 = True
                sent = self.sender.sendMessage('Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
            else :
                self.bot.answerCallbackQuery(query_id, text='Gagal Memberikan Pakan')
                sent = self.sender.sendMessage('Proses lain sedangan berjalan..')
            self.close()
            
        elif query_data == 'BL':
            self._cancel_last()
            if (status_5 == False) :
                self.bot.answerCallbackQuery(query_id, text='Ok. Perintah Dijalankan..')
                sent = self.sender.sendMessage('Pemberian pakan sedang berjalan')
                status_5 == True
                text = 'Pemberian Pakan pada Kolam '
                # ambil Video
                pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                time.sleep(5) #delay mempersiapkan kamera
                if (status_1):
                    status_1 = False
                    text += '1, '
                    # motor servo jalan
                if (status_2):
                    status_2 = False
                    text += '2, '
                    # motor servo jalan
                if (status_3):
                    status_3 = False
                    text += '3, '
                    # motor servo jalan
                # stop rekam
                p.terminate()
                time.sleep(5) # delay endcoding video
                text += 'telah dilakukan lagi'
                status_5 = False
                sent = self.sender.sendMessage(text)
                status_6 = True
                self.sender.sendMessage('Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
            else :
                self.bot.answerCallbackQuery(query_id, text='Gagal Memberikan Pakan')
                sent = self.sender.sendMessage('Proses lain sedangan berjalan..')
            self.close()
        
        elif query_data == 'batal':
            status_1 = False
            status_2 = False
            status_3 = False
            self._cancel_last()
            self.close()
        # == end Beri Pakan ==
        
        # == Bagian Status ==
        elif query_data == 'AG':
            self._cancel_last()
            if (status_5 == False) :
                self.bot.answerCallbackQuery(query_id, text='Ok. Mengambil Gambar')
                status_5 = True
                # ambil gambar kirim
                ## motor bergerak ke kolam 1
                os.system('fswebcam -r 1280x720 --title Gambar-Kolam-1 takeGambar1.jpg')                
                ## motor bergerak ke kolam 2
                os.system('fswebcam -r 1280x720 --title Gambar-Kolam-2 takeGambar2.jpg')
                ## motor bergerak ke kolam 3
                os.system('fswebcam -r 1280x720 --title Gambar-Kolam-3 takeGambar3.jpg')
                status_5 = False
                sent = self.sender.sendPhoto(open('ambilGambar1.jpg', 'rb'), caption = 'Gambar Kolam 1')
                sent = self.sender.sendPhoto(open('ambilGambar2.jpg', 'rb'), caption = 'Gambar Kolam 2')
                sent = self.sender.sendPhoto(open('ambilGambar3.jpg', 'rb'), caption = 'Gambar Kolam 3')
            else :
                self.bot.answerCallbackQuery(query_id, text='Gagal Mengambil Gambar')
                sent = self.sender.sendMessage('Proses lain sedangan berjalan..')
            self.close()
        elif query_data == 'AV':
            self._cancel_last()
            if (status_5 == False) :
                self.bot.answerCallbackQuery(query_id, text='Ok. Mengambil Video')
                status_5 = True
                # ambil Video
                pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 takeVideo.mp4 -y'
                p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                time.sleep(5) #delay mempersiapkan kamera
                # motor bergerak dari kolam 1 ke 3
                # stop rekam
                p.terminate()
                time.sleep(5) # delay endcoding video
                status_5 = False
                sent = self.sender.sendVideo(open('takeVideo.mp4', 'rb'), caption = 'Pengambilan Video', supports_streaming=True)
            else :
                self.bot.answerCallbackQuery(query_id, text='Gagal Mengambil Video')
                sent = self.sender.sendMessage('Proses lain sedangan berjalan..')
            self.close()
        # == end Bagian Status ==
        else:
            self.bot.answerCallbackQuery(query_id, text='Ok. Tapi aku akan terus bertanya.')
            self._cancel_last()
            self._propose()
    
    def on__idle(self, event):
        global status_1
        global status_2
        global status_3
        global status_4
        global status_6

        if statusO_3 == False and status_5 == False :
            if status_1 or status_2 or status_3 or status_4 :                
                status_1 = False
                status_2 = False
                status_3 = False
                status_4 = False
                self.sender.sendMessage('Saya tahu Anda mungkin perlu sedikit waktu. Aku akan selalu di sini untukmu.')
                self._cancel_last()
        status_6 = False
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
    
    try:
        
        now = datetime.datetime.now()
        t = now.strftime('%d-%m-%Y di jam %H:%M:%S')
        
        if status_8 :
            bootingdown  = 'Sistem BootingUp... '+t1+'\n'
            bot.sendMessage(CHATID, bootingdown, parse_mode='html')
            bootingup = 'Seluruh Pengaturan Telah Diset <i>Default</i> \n'
            bot.sendMessage(CHATID, bootingup, parse_mode='html')
            status_8 = False
                       
        if status_7 :
            status_7 = False
            bot.sendMessage(CHATID, 'Sistem sebelumnya mengalami gangguan sinyal pada '+t+' sampai pesan ini terkirim membuat sistem melakuakan beberapa tindakan secara otomatis, harap untuk memeriksa status kolam anda')        
            
        print(now.hour,":",now.minute)
        print(jadwal_1,":",jadwal_2,":",jadwal_3,":",takar_1,":",takar_2,":",takar_3,"||",status_1,":",status_2,":",status_3,"||",statusP_1,":",statusP_2,":",statusP_3)
        
        # == Pencitraan Otomatis ==
        if (now.hour == schedule):
            statusO_1 = True
            schedule = schedule + 1
            if (schedule == 24):
                schedule = 0
                statusP_1 = False
                statusP_2 = False
                statusP_3 = False

            status_5 = True
            # ambil Gambar
            ## motor bergerak ke kolam 1            
            os.system('fswebcam --no-banner -r 1280x720 --title Citra-Kolam-1 ambilGambar1.jpg')
            # ambil Gambar
            ## motor bergerak ke kolam 2
            os.system('fswebcam --no-banner -r 1280x720 --title Citra-Kolam-2 ambilGambar2.jpg')
            # ambil Gambar
            ## motor bergerak ke kola 3
            os.system('fswebcam --no-banner -r 1280x720 --title Citra-Kolam-3 ambilGambar3.jpg')
            status_5 = False
            
            from  Pencitraan1 import deteksi1
            if (deteksi1):
                statusK_1 = False
                print("terdeteksi")
                bot.sendPhoto(CHATID, open('citra1.jpg', 'rb'), caption = 'Pencitraan Kolam 1')
                bot.sendMessage(CHATID, '<b>PERINGATAN !!</b> SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM 1 ANDA', parse_mode='html')
            else :
                statusK_1 = True
                print("tidak Terdeteksi")
                
            from  Pencitraan2 import deteksi2
            if (deteksi2):
                statusK_2 = False
                print("terdeteksi")
                bot.sendPhoto(CHATID, open('citra2.jpg', 'rb'), caption = 'Pencitraan Kolam 2')
                bot.sendMessage(CHATID, '<b>PERINGATAN !!</b> SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM 2 ANDA', parse_mode='html')
            else :
                statusK_2 = True
                print("tidak Terdeteksi")
                
            from  Pencitraan3 import deteksi3
            if (deteksi3):
                statusK_3 = False
                print("terdeteksi")
                bot.sendPhoto(CHATID, open('citra3.jpg', 'rb'), caption = 'Pencitraan Kolam 3')
                bot.sendMessage(CHATID, '<b>PERINGATAN !!</b> SISTEM MENDETEKSI TERDAPAT IKAN MATI PADA KOLAM, SEGERA PERIKSA KONDISI KOLAM 3 ANDA', parse_mode='html')
            else :
                statusK_3 = True
                print("tidak Terdeteksi")
        # == end Pencitraan Otomatis
            
        # == Pemberian Pakan Otomatis ==
        if jadwal_1 != jadwal_2 and jadwal_1 != jadwal_3 and jadwal_2 != jadwal_3 and statusO_2 :
            print('running1')
            if (statusP_1 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    status_1 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 telah dilakukan secara otomatis')
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_2 == False and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam 2 takar_2
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_2 = True
                    status_2 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 telah dilakukan secara otomatis')
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)                    
            elif (statusP_3 == False and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam 3 takar_3
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_3 = True
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
        elif jadwal_1 == jadwal_2 and jadwal_1 != jadwal_3 and jadwal_2 != jadwal_3 and statusO_2 :
            print('running2')
            if (statusP_1 == False and statusP_2 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    statusP_2 = True
                    status_1 = False
                    status_2 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_1 == False and statusP_2 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    status_1 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_2 == False and statusP_1 and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_2 = True
                    status_2 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 telah dilakukan secara otomatis')
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_3 == False and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_3 = True
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
        elif jadwal_1 != jadwal_2 and jadwal_2 == jadwal_3 and jadwal_1 != jadwal_3 and statusO_2 :
            print('running3')
            if (statusP_2 == False and statusP_3 == False and jadwal_2 == now.hour):
                statusO_3 = True
                status_3 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_3 = True
                    statusP_2 = True
                    status_2 = False
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_1 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    status_1 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_2 == False and statusP_3 and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_2 = True
                    status_2 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_3 == False and statusP_2 and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_3 = True
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
        elif jadwal_1 == jadwal_3 and jadwal_3 != jadwal_2 and jadwal_2 != jadwal_1 and statusO_2 :
            print('running4')
            if (statusP_1 == False and statusP_3 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    statusP_3 = True
                    status_1 = False
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)                    
            elif (statusP_1 == False and statusP_3 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    status_1 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_2 == False and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_2 = True
                    status_2 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_3 == False and statusP_1 and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_3 = True
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)                
        elif jadwal_1 == jadwal_3 and jadwal_3 == jadwal_2 and statusO_2 :
            print('running5')
            if (statusP_1 == False and statusP_2 == False and statusP_3 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_2 = True
                status_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1, 2 dan 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1, 2 dan 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    statusP_2 = True
                    statusP_3 = True
                    status_1 = False
                    status_2 = False
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1, 2 dan 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)                    
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_1 == False and statusP_2 == False and statusP_3 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    statusP_2 = True
                    status_1 = False
                    status_2 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 2 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_2 == False and statusP_3 == False and statusP_1 and jadwal_2 == now.hour):
                statusO_3 = True
                status_3 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_3 = True
                    statusP_2 = True
                    status_2 = False
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 dan 2 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_1 == False and statusP_3 == False and statusP_2 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam dan takar_
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    statusP_3 = True
                    status_1 = False
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 dan 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_1 == False and statusP_2 and statusP_3 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_1 = True
                    status_1 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 1 telah dilakukan secara otomatis')
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
            elif (statusP_2 == False and statusP_3 and statusP_1 and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam 2 takar_2
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_2 = True
                    status_2 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 2 telah dilakukan secara otomatis')
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)                    
            elif (statusP_3 == False and statusP_2 and statusP_1 and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 akan dilakukan.. lanjutkan ? \nAku akan melanjutkannya secara otomatis jika Anda tidak membatalkanya..', parse_mode='html', reply_markup=keyboardO_1)
                time.sleep(600)
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 sedang berjalan..', reply_markup = keyboardO_2)
                    status_5 = True
                    # ambil Video
                    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y'
                    p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
                    time.sleep(5) #delay mempersiapkan kamera
                    # motor servo jalan berdasarkan kolam 3 takar_3
                    # stop rekam
                    p.terminate()
                    time.sleep(5) # delay endcoding video
                    status_5 = False
                    statusP_3 = True
                    status_3 = False
                    status_6 = True
                    bot.sendMessage(CHATID, 'Pemberian Pakan pada Kolam 3 telah dilakukan secara otomatis')                    
                    bot.sendMessage(CHATID, 'Ingin Aku mengirimkan Video Dokumentasinya ?..', reply_markup=keyboardO_3)
                else :
                    bot.sendMessage(CHATID, 'Pemeberian pakan gagal dijalnkan, Proses lain sedangan berjalan..', reply_markup=keyboardO_1)
                    
        # == end Pembarian Pakan Otomatis ==
        
    except:
        
        #pass --> doing nothing on exception
        print('Gangguan Sinyal')
        status_7 = True
        now = datetime.datetime.now()
        print(now.hour,":",now.minute)
        print(jadwal_1,":",jadwal_2,":",jadwal_3,":",takar_1,":",takar_2,":",takar_3,"||",status_1,":",status_2,":",status_3,"||",statusP_1,":",statusP_2,":",statusP_3)
        
        # == Pencitraan Otomatis ==
        if (now.hour == schedule):
            statusO_1 = True
            schedule = schedule + 1
            if (schedule == 24):
                schedule = 0
                statusP_1 = False
                statusP_2 = False
                statusP_3 = False

            status_5 = True
            # ambil Gambar
            ## motor bergerak ke kolam 1
            os.system('fswebcam --no-banner -r 1280x720 --title Citra-Kolam-1 ambilGambar1.jpg')
            # ambil Gambar
            ## motor bergerak ke kolam 2
            os.system('fswebcam --no-banner -r 1280x720 --title Citra-Kolam-2 ambilGambar2.jpg')
            # ambil Gambar
            ## motor bergerak ke kolam 3
            os.system('fswebcam --no-banner -r 1280x720 --title Citra-Kolam-3 ambilGambar3.jpg')
            status_5 = False
            
            from  Pencitraan1 import deteksi1
            if (deteksi1):
                statusK_1 = False
                print("terdeteksi")
            else :
                statusK_1 = True
                print("tidak Terdeteksi")
                            
            from  Pencitraan2 import deteksi2
            if (deteksi2):
                statusK_2 = False
                print("terdeteksi")
            else :
                statusK_2 = True
                print("tidak Terdeteksi")
                
            from  Pencitraan3 import deteksi3
            if (deteksi3):
                statusK_3 = False
                print("terdeteksi")
            else :
                statusK_3 = True
                print("tidak Terdeteksi")
        # == end Pencitraan Otomatis
            
        # == Pemberian Pakan Otomatis ==
        if jadwal_1 != jadwal_2 and jadwal_1 != jadwal_3 and jadwal_2 != jadwal_3 and statusO_2 :
            print('jalan1')
            if (statusP_1 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_1 = True
                    status_1 = False
            elif (statusP_2 == False and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 2 takar_2
                    status_5 = False
                    status_6 = True
                    statusP_2 = True
                    status_2 = False
            elif (statusP_3 == False and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 3 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_3 = True
                    status_3 = False
        elif jadwal_1 == jadwal_2 and jadwal_1 != jadwal_3 and jadwal_2 != jadwal_3 and statusO_2 :
            print('jalan2')
            if (statusP_1 == False and statusP_2 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_1 = True
                    statusP_2 = True
                    status_1 = False
                    status_2 = False
            elif (statusP_1 == False and statusP_2 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_1 = True
                    status_1 = False
            elif (statusP_2 == False and statusP_1 and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    # motor servo jalan berdasarkan kolam 2 takar_2
                    status_6 = True
                    statusP_2 = True
                    status_2 = False
            elif (statusP_3 == False and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 3 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_3 = True
                    status_3 = False
        elif jadwal_1 != jadwal_2 and jadwal_2 == jadwal_3 and jadwal_1 != jadwal_3 and statusO_2 :
            print('jalan3')
            if (statusP_2 == False and statusP_3 == False and jadwal_2 == now.hour):
                statusO_3 = True
                status_3 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_3 = True
                    statusP_2 = True
                    status_2 = False
                    status_3 = False
            elif (statusP_1 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_1 = True
                    status_1 = False
            elif (statusP_2 == False and statusP_3 and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 2 takar_2
                    status_5 = False
                    status_6 = True
                    statusP_2 = True
                    status_2 = False
            elif (statusP_3 == False and statusP_2 and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 3 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_3 = True
                    status_3 = False
        elif jadwal_1 == jadwal_3 and jadwal_3 != jadwal_2 and jadwal_2 != jadwal_1 and statusO_2 :
            print('jalan4')
            if (statusP_1 == False and statusP_3 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_1 = True
                    statusP_3 = True
                    status_1 = False
                    status_3 = False
            elif (statusP_1 == False and statusP_3 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = FAlse
                    status_6 = True
                    statusP_1 = True
                    status_1 = False
            elif (statusP_2 == False and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 2 takar_2
                    # ambil viedeo
                    status_5 = False
                    status_6 = True
                    statusP_2 = True
                    status_2 = False
            elif (statusP_3 == False and statusP_1 and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 3 takar_1
                    status_5 = False
                    status_6 = True
                    statusP_3 = True
                    status_3 = False                
        elif jadwal_1 == jadwal_3 and jadwal_3 == jadwal_2 and statusO_2 :
            print('jalan5')
            if (statusP_1 == False and statusP_2 == False and statusP_3 == False and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_2 = True
                status_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam dan takar_
                    status_5 = False
                    statusP_1 = True
                    statusP_2 = True
                    statusP_3 = True
                    status_1 = False
                    status_2 = False
                    status_3 = False
                    status_6 = True
            elif (statusP_1 == False and statusP_2 == False and statusP_3 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam dan takar_
                    status_5 = False
                    statusP_1 = True
                    statusP_2 = True
                    status_1 = False
                    status_2 = False
                    status_6 = True
            elif (statusP_2 == False and statusP_3 == False and statusP_1 and jadwal_2 == now.hour):
                statusO_3 = True
                status_3 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam dan takar_
                    status_5 = False
                    statusP_3 = True
                    statusP_2 = True
                    status_2 = False
                    status_3 = False
                    status_6 = True
            elif (statusP_1 == False and statusP_3 == False and statusP_2 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                status_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam dan takar_
                    status_5 = False
                    statusP_1 = True
                    statusP_3 = True
                    status_1 = False
                    status_3 = False
                    status_6 = True
            elif (statusP_1 == False and statusP_2 and statusP_3 and jadwal_1 == now.hour):
                statusO_3 = True
                status_1 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 1 takar_1
                    status_5 = False
                    statusP_1 = True
                    status_1 = False
                    status_6 = True
            elif (statusP_2 == False and statusP_3 and statusP_1 and jadwal_2 == now.hour):
                statusO_3 = True
                status_2 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 2 takar_2
                    status_5 = False
                    statusP_2 = True
                    status_2 = False
                    status_6 = True                  
            elif (statusP_3 == False and statusP_2 and statusP_1 and jadwal_3 == now.hour):
                statusO_3 = True
                stauts_3 = True
                if(statusO_1 and status_5 == False):
                    statusO_3 = False
                    status_5 = True
                    # motor servo jalan berdasarkan kolam 3 takar_3
                    status_5 = False
                    statusP_3 = True
                    status_3 = False
                    status_6 = True

        # == end Pembarian Pakan Otomatis ==                
    time.sleep(10)