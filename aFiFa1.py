import time, datetime
import os
import telepot
import RPi.GPIO as GPIO

from telepot.loop import MessageLoop

now = datetime.datetime.now()

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

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    #verifikasi
    if msg['from']['id'] != 1137202289:
        bot.sendMessage(chat_id, "Maaf ini adalah bot pribadi. Akses ditolak!")
        exit(1)

    print 'Received: %s' % command

    if 'on' in command:
        message = "Turned on "
        
        if 'relay' in command:
            message = message + "led"
            GPIO.output(RELAY, 1)
            telegram_bot.sendMessage (chat_id, message)

    elif 'off' in command:
        message = "Turned off "
        
        if 'relay' in command:
            message = message + "led "
            GPIO.output(RELAY, 0)
            telegram_bot.sendMessage (chat_id, message)
            
    else :
        message = "Selamat Datang di Smart Fish Farm \n"
        message = message + "============================ \n"
        message = message + "Anda dapat mengotrol sata dengan mengirimkam perintah ini :"
        telegram_bot.sendMessage (chat_id, message)

 

telegram_bot = telepot.Bot('1202817061:AAHLFAFoftMnaOenIt59XG_IzGIp8a7yM2M')
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()

print 'Up and Running....'


while 1:
    time.sleep(10)
