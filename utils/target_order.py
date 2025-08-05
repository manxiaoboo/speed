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
    lineWidth = util.getWidth(x1, x2)
    differenceWidth = util.calcDifferenceWidth(lineWidth)
        
    if abs(differenceX) > 150:
        handleOffsetH(entity)
        return False
    
    if abs(differenceWidth) > 45 and abs(differenceX) > 30:
        handleOffsetDirection(entity)
        return False
    
    return True

def handle123Offset(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    targetHeight = y2 - y1
    lineWidth = util.getWidth(x1, x2)
    differenceWidth = util.calcDifferenceWidth(lineWidth)
        
    
    # if abs(differenceWidth) > 51:
    #     handleOffsetDirection(entity)
    #     return False
    
    if abs(differenceX) > 60:
        handleOffsetH(entity)
        return False
    
    if targetHeight < 200:
        ahead(30, 0.6)
        return False
    
    if targetHeight >= 200 and targetHeight < 286:
        time.sleep(0.2)
        ahead(35, abs(targetHeight) / 320)
        # handleOffsetDirection(entity)
        time.sleep(0.2)
        doCatch()
        return True
    
    if targetHeight >= 286 and targetHeight <= 290:
        # handleOffsetDirection(entity)
        doCatch()
        return True
    
    if targetHeight > 290:
        ahead(-30, 0.2)
        return False
    
def handleOffsetDirection(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineWidth = util.getWidth(x1, x2)
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    differenceWidth = util.calcDifferenceWidth(lineWidth)
    turn_size = abs(differenceWidth) / 100 * 0.25
    print(f"turn  {turn_size}")
    if differenceX > 0:
        offsetTurn(28, turn_size, 'right')
    elif differenceX < 0:
        offsetTurn(28, turn_size, 'left')
    

def handleOffsetH(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    horizontal_size = abs(differenceX) / 65 * 0.25
    print(f"Move H {horizontal_size}")
    if differenceX > 0:
        offsetHorizontal(40, horizontal_size, 'right')
        local_status.OFFSET += horizontal_size
    elif differenceX < 0:
        offsetHorizontal(40, horizontal_size, 'left')
        local_status.OFFSET -= horizontal_size
    
def goToABCTarget(entity):
    if handleOffset(entity) == False:
        return False
    else:
        return True
    
def goTo123Target(entity):
    if handle123Offset(entity) == False:
        return False
    else:
        return True

def nextOutlookPosition():
    next_index = 0
    if local_status.CURRENT_OUTLOOK_INDEX == len(local_status.OUTLOOK):
        next_index = 0
    else:
        next_index = local_status.CURRENT_OUTLOOK_INDEX + 1
        
    offsetHorizontal(50, 5.5, local_status.OUTLOOK[local_status.CURRENT_OUTLOOK_INDEX])
    local_status.CURRENT_OUTLOOK_INDEX = next_index

def doCatch():
    local_status.CAR_BUSY = True
    mqtt_server.driveCar(car_command.TopicGet, 1)
    time.sleep(10)
    local_status.CAR_BUSY = False

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

def bounce():
    move_car('ahead', -20, 0.1)
    
def left():
    offsetHorizontal(40, 0.3, 'left')

def right():
    offsetHorizontal(40, 0.3, 'right')

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