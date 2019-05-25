import datetime
import astral
import pytz
import time
import motor
from twilio.rest import Client
import RPi.GPIO as GPIO

account_sid = 'mytwiliosid'
auth_token = 'mytwiliotoken'
client = Client(account_sid, auth_token)



a = astral.Astral()
city_name = 'Omaha'
city = a[city_name]
timezone = city.timezone
sun = city.sun(date=datetime.date.today(), local=True)
dt = datetime.datetime.now(tz=pytz.UTC)
dt_central_now = dt.astimezone(pytz.timezone('US/Central'))
delta = datetime.timedelta(seconds=20)
test_sunset = dt_central_now + delta

##print('sunrise is: ', sunrise, 'today.')
##print('sunset is: ', sunset, 'today.')

##print(dt_central_now - sunrise)

try:
    mode = 1
    evening_message = 0
    morning_message = 0
    while True:
        
        if motor.button(11):
            time.sleep(.5)
            motor.open_door()
            mode = mode*-1
            print(mode)
            
        elif motor.button(13):
            time.sleep(.5)
            motor.close_door()
            mode = mode*-1
            print(mode)
            
        dt = datetime.datetime.now(tz=pytz.UTC)
        dt_central_now = dt.astimezone(pytz.timezone('US/Central'))
        sun = city.sun(date=datetime.date.today(), local=True)
        sunrise = sun['sunrise']
        sunset = sun['sunset']
        sunset_delta = datetime.timedelta(minutes=10)
        
##        if dt_central_now < sunrise:
##            print("door opening in ", sunrise - dt_central_now)
##            time.sleep(60)
        if dt_central_now >= sunrise and dt_central_now < sunset and not motor.reed_pin(16) and mode == 1 and morning_message == False:
            print("opening door")
            try:
                client.messages.create(body = "The sun is up! The chicken door is opening!" , from_='phonenumber', to='phonenumber')
            except:
                print("unable to send message, check connection.")
                
        if dt_central_now >= sunrise and dt_central_now < sunset and not motor.reed_pin(16) and mode == 1:
            motor.open_door()
            morning_message = True
            evening_message = False
            
##        elif dt_central_now < sunset:
##            print("door closing in ", sunset - dt_central_now)
##            time.sleep(1000)
        elif dt_central_now >= sunset and dt_central_now > sunrise and not motor.reed_pin(15) and mode == 1 and evening_message == False:
            print("sun down, closing door in 10 minutes")
            try:
                client.messages.create(body = "The sun has set! Make sure your birds are indoors.  Door closes in 10 minutes!" , from_='+phonenumber', to='phonenumber')
                
            except:
                print("unable to send message, check connection.")
            morning_message = False
            evening_message = True
            
        elif dt_central_now >= sunset + sunset_delta and dt_central_now > sunrise and not motor.reed_pin(15) and mode == 1:
            motor.close_door()
##            print("closing door")
        
finally:
    GPIO.cleanup()
