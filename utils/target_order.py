import time
import enums
import utils.car_command as car_command
import servers.mqtt_server as mqtt_server
import servers.camera_server as camera_server
import utils.util as util
import local_status

def handleOffset(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    
    if differenceX > 70:
        # offsetTurn(20, 0.3, 'left')
        offsetHorizontal(40, 0.5, 'right')
    elif differenceX < -70:
        # offsetTurn(20, 0.3, 'right')
        offsetHorizontal(40, 0.5, 'left')
    
def goToABCTarget(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    if abs(differenceX) > 70:
        handleOffset(entity)
        return False
    else:
        return True

def nextOutlookPosition(entity):
    next_index = 0
    if local_status.CURRENT_OUTLOOK_INDEX == len(local_status.OUTLOOK):
        next_index = 0
    else:
        next_index = local_status.CURRENT_OUTLOOK_INDEX + 1
        
    ahead(40, 0.5)
    if (local_status.OUTLOOK[local_status.CURRENT_OUTLOOK_INDEX] == 'left'):
        offsetTurn(30, 0.3, 'right')
    else:
        offsetTurn(30, 0.3, 'left')
        
    offsetHorizontal(50, 5, local_status.OUTLOOK[local_status.CURRENT_OUTLOOK_INDEX])
    local_status.CURRENT_OUTLOOK_INDEX = next_index

def doCatch():
     mqtt_server.driveCar(car_command.TopicGet, 1)
     time.sleep(5)     

def ahead(speed, duration):
    move_car('ahead', speed, duration)

def stopCar():
    move_car('stop', 50)

def offsetTurn(speed, duration, direction):
    move_car('turn', speed, duration, direction)

def offsetHorizontal(speed, duration, direction):
    move_car('horizontal', speed, duration, direction)
    
def turn(direction):
    move_car('turn', 20, 4.3, direction)
    
def turnAround():
    local_status.setCamera('2')
    camera_server.takePhoto()
    move_car('turn', 20, 8.8, 'left')

def back():
    move_car('ahead', -40, 0.2)
    
def left():
    offsetHorizontal(40, 0.2, 'left')

def move_car(action, speed=0, duration=0, direction=None):
    local_status.CAR_BUSY = True
    if action == 'ahead':
        mqtt_server.driveCar(car_command.TopicMoveV, speed)
    elif action == 'stop':
        mqtt_server.driveCar(car_command.TopicStop, speed)
    elif action == 'turn':
        mqtt_server.driveCar(car_command.TopicMoveT, speed if direction == 'right' else -speed)
    elif action == 'horizontal':
        mqtt_server.driveCar(car_command.TopicMoveH, speed if direction == 'right' else -speed)
    if duration > 0:
        time.sleep(duration)
    if action != 'stop':
        mqtt_server.driveCar(car_command.TopicStop, 50)
    local_status.CAR_BUSY = False