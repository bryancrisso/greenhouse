import threading, time, sys

water_level = 80
water_leak = 5
bucket = 10
temperature = 25
door_open = False
temperature_change = 1
choice = None
threads = None

def explanation():
    print('''Mr Potts the gardener has a very old green house and some very sensitive plants. Can you help him keep his plants alive?
You must make sure that the water level never drops below 50 liters (you can top up the tank using the 10 liter bucket) and that the
temperature is never above 30c or below 20c… you can regulate this by opening and closing the green house door... but there is a problem
the water is leaking at 5 liters a minute, the bucket holds 10 liters and takes 1 minute fill. When the greenhouse door is open the
temperature drops by 1c minute when it is closed the temperature raises by 1c minute.

  --->  *IMPORTANT: The time speed is x6 so a minute is 10 seconds*  <---  ''')

#changes the water level
class WaterLeak(threading.Thread):
    global threads
    def run(self):
        global water_level, water_leak, threads
        while threads:
            time.sleep(10)
            water_level -= water_leak
            if water_level <= 60:
                print('WARNING: Water level is at ' + str(water_level) + ' litres and must not get below 50 litres. Fill the water tank up now!')

#changes the temperature
class TemperatureChange(threading.Thread):
    global threads
    def run(self):
        global temperature, temperature_change, door_open, threads
        while threads:
            time.sleep(10)
            if door_open:
                temperature -= temperature_change
                if temperature <= 22:
                    print('WARNING: Temperature is at ' + str(temperature) + ' Centigrade. Do not let it get below 20 degrees. Close the door!')
            else:
                temperature += temperature_change
                if temperature >= 28:
                    print('WARNING: Temperature is at ' + str(temperature) + ' Centigrade. Do not let it get over 30 degrees. Open the door!')

#the thread that manages the stats
class StatsManager(threading.Thread):
    global threads
    def run(self):
        global temperature, water_level, door_open, threads
        while threads:
            if water_level < 50:
                print('''
THE WATER LEVEL HAS FALLEN
    BENEATH 50 LITRES
    GAME        OVER''')
                time.sleep(3)
                threads = False
            elif temperature < 20:
                print('''
THE TEMPERATURE HAS FALLEN
   BENEATH 20 DEGREES
    GAME        OVER''')
                time.sleep(3)
                threads = False
            elif temperature > 30:
                print('''
THE TEMPERATURE HAS RISEN
    OVER 30 DEGREES
    GAME       OVER''')
                time.sleep(3)
                threads = False

#fill up water with bucket
def fillwater():
    global water_level, water_leak
    if water_level <= 70:
            print('Filling up water with bucket by 10 litres')
            time.sleep(10)
            water_level += 10
            print('Water Tank filled by 10 litres')
            print('Water level is at ' + str(water_level) + ' litres')
    elif water_level > 70 and water_level < 80:
        amounttofill = 80 - water_level
        print('Filling up water with bucket by ' + str(amounttofill) + ' litres')
        time.sleep(amounttofill)
        water_level += amounttofill
        print('Water Tank filled by ' + str(amounttofill) + ' litres')
        print('Water level is at ' + str(water_level) + ' litres')
    else:
        print('Water tank is full!')

#open or close the door
def changedoor():
    global door_open
    if door_open == False:
        door_open = True
        print('Door Opened!')
    elif door_open == True:
        door_open = False
        print('Door Closed!')
    else:
        print('error')

def menu():
    global temperature, door_open, water_level, threads
    explanation()
    input('Press Enter to Start')
    startthreads()
    while threads:
        print('''
Main Menu
[0]Exit
[1]Check Stats (Keep up with always)
[2]Fill Up Water Tank With Bucket
[3]Open/Close Door
    ''')
        choice = input('Choice [')
        if choice == '0':
            sys.exit()
        if choice == '1':
            if door_open == False:
                print('\nWater level is at ' + str(water_level) + ' litres')
                print('Temperature is at ' + str(temperature) + ' Centigrade')
                print('The door is closed')
                print('\nThreads Running: ' + str(threads) + ' (ignore)')
            elif door_open == True:
                print('Water level is at ' + str(water_level) + ' litres')
                print('Temperature is at ' + str(temperature) + ' Centigrade')
                print('The door is open')
                print('\nThreads Running: ' + str(threads) + ' (ignore)')
            else:
                print('There was an error in viewing stats')
        if choice == '2':
            fillwater()
        if choice == '3':
            changedoor()
    sys.exit()
def startthreads():
    global threads
    threads = True
    leaking_water = WaterLeak()
    manage_stats = StatsManager()
    temperature_changing = TemperatureChange()

    leaking_water.start()
    manage_stats.start()
    temperature_changing.start()
menu()