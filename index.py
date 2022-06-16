import json
import time
#Libraries
import RPi.GPIO as GPIO
import socket
from rpi_TM1638 import TMBoards


# Variable global para guardar el estado
estados = {
    "encenderLed": False,
    "encenderMotor": False
}

def actualiceConfig():
    global estados

    with open('config.json',) as f:
        config = json.load(f)
        # Convertir de string a booleano
        config['encenderLed'] = True if config['encenderLed'] == "True" else False
        config['encenderMotor'] = True if config['encenderMotor'] == "True" else False

        estados = config
        f.close()

def actualiceFile(distancia):
    global estados

    with open('config.json','w') as f:
        newData = {
            "encenderLed": "True" if estados['encenderLed'] else "False",
            "encenderMotor": "True" if estados['encenderMotor'] else "False",
            "distancia": distancia
        }
        # Serializing json
        json_object = json.dumps(newData, separators=(',', ':'))

        # Writing to sample.json
        f.write(json_object)
        f.close()

if __name__ == '__main__':
    while(1):
        actualiceConfig()
        if estados['encenderLed'] == True:
            #TM Para imprimir en modilo tm-1638
            DIO = 19 #pin 35
            CLK = 13 #pin 33
            STB = 26 #pin 37
            TM = TMBoards(DIO, CLK, STB, 0)
            TM.clearDisplay()


            #GPIO Mode (BOARD / BCM)
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

            #set GPIO Pins
            GPIO_TRIGGER = 18
            GPIO_ECHO = 24


            #set GPIO direction (IN / OUT)
            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO, GPIO.IN)

            def distance():
            # set Trigger to HIGH
            #GPIO.output(GPIO_TRIGGER, True) 
                GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
            # set Trigger after 0.01ms to LOW
                time.sleep(0.00001)
                GPIO.output(GPIO_TRIGGER, False)

                StartTime = time.time()
                StopTime = time.time()

            # save StartTime
                while GPIO.input(GPIO_ECHO) == 0:
                    StartTime = time.time()

            # save time of arrival
                while GPIO.input(GPIO_ECHO) == 1:
                    StopTime = time.time()

            # time difference between start and arrival
                TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
                distance = (TimeElapsed * 34300) / 2

                return distance
            if __name__ == '__main__':
                try:
                   # while True:
                        dist = distance()
                        print ("La distancia es: = %.1f cm" % dist)
                        y=10
                        if dist<y:

                            print ("La distancia es menor a 10 cm") #Imprime que la distancia es menor a 10 cm y lo manda al TM
                            print ("Esperando 10 segundos")
                            # Se actualiza el archivo con la distancia medida
                            actualiceFile(dist)
                            TM.segments[0]= 'D'
                            TM.segments[1]= 'I'
                            TM.segments[2]= 'S'
                            TM.segments[3]= 'T'
                            TM.segments[4]= 'A'
                            TM.segments[5]= '-'
                            TM.segments[6]= '1'
                            TM.segments[7]= '0'

                            GPIO.setup(23, GPIO.OUT)
                            GPIO.output(23, GPIO.HIGH)
                            time.sleep(10)
                            GPIO.output(23, GPIO.LOW)
                            TM.segments[0]= ' '
                            TM.segments[1]= ' '
                            TM.segments[2]= ' '
                            TM.segments[3]= ' '
                            TM.segments[4]= ' '
                            TM.segments[5]= ' '
                            TM.segments[6]= ' '
                            TM.segments[7]= ' '


                        time.sleep(1)


    

            # Reset by pressing CTRL + C
                except KeyboardInterrupt:
                 print("Medir distancia detenido por el usuario. ")
                 TM.clearDisplay()
                 GPIO.cleanup()

        if estados['encenderMotor'] == True:
            print("Comprobando estado Para detener presiona control+C")
        #print('Led: ', 'encendido' if estados['encenderLed'] == True else 'apagado' )
        #print('Motor: ', 'encendido' if estados['encenderMotor'] == True else 'apagado' )
        #print('\n')
        time.sleep(1)

