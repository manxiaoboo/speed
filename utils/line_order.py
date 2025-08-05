import time
import enums
import utils.car_command as car_command
import servers.mqtt_server as mqtt_server
import servers.camera_server as camera_server
import utils.util as util
import local_status

last_diffX = 0
next_direc = ''
    
def handleOffset(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    lineWidth = util.getWidth(x1, x2)
    differenceWidth = util.calcDifferenceWidth(lineWidth)
        
    if abs(differenceX) > 110 and last_diffX == 0:
        print('handleH============>', abs(differenceX))
        handleOffsetH(entity)
        return False
    
    print('handleDirection=============>', abs(differenceWidth), abs(differenceX))
    if abs(differenceWidth) > 24 and abs(differenceX) > 20:
        handleOffsetDirection(entity)
        return False
    
    return True

def handleOffsetDirection(entity):
    global last_diffX
    global next_direc
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineWidth = util.getWidth(x1, x2)
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    differenceWidth = util.calcDifferenceWidth(lineWidth)
    if last_diffX == 0:
        last_diffX = differenceX
    turn_size = abs(differenceWidth) / 130 * 0.25
    if turn_size < 0.04:
        turn_size = 0.04
        
    print(f"differenceX: {differenceX}  x1:{x1}")
    
    # special case
    if abs(last_diffX) < abs(differenceX):
        turn_size = turn_size * 2
        last_diffX = 0
        offsetTurn(22, turn_size, next_direc)
        next_direc = ''
    else:
        next_direc = ''
        last_diffX = 0
        
        if differenceX > 0:
                offsetTurn(22, turn_size, 'right')
                next_direc = 'left'
        elif differenceX < 0:
                offsetTurn(22, turn_size, 'left')
                next_direc = 'right'
    
    

def handleOffsetH(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    horizontal_size = abs(differenceX) / 80 * 0.25
    if horizontal_size < 0.04:
        horizontal_size = 0.04
    print(f"Move H {horizontal_size}")
    if differenceX > 0:
        offsetHorizontal(40, horizontal_size, 'left')
    elif differenceX < 0:
        offsetHorizontal(40, horizontal_size, 'right')


def handleLine(entity, speed=-80, time=2):
    global last_diffX
    global next_direc
    if handleOffset(entity) == False:
        return False
    
    last_diffX = 0
    next_direc = ''
    ahead(speed, time)

def handleEnd(entity):
    print('00000000000 handleEnd')
    box = entity['box']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterY = util.getCenterPositionY(y1, y2)
    differenceY = util.calcDifferenceY(lineCenterY)
    endHeight = util.getHeight(y1, y2)
    
    handleOffset(entity)
        
    ahead(-58, abs((240 - endHeight) / 80))
    turnAround()
    return True
                
def handleTurning(entity, direction):
    box = entity['box']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterY = util.getCenterPositionY(y1, y2)
    differenceY = util.calcDifferenceY(lineCenterY)
    turnHeight = util.getHeight(y1, y2)
    
    if handleOffset(entity) == False:
        return False
    
    if differenceY >= 0:
        back()
        return False
    
    if differenceY < 0 and differenceY > -180:
        ahead(-60, abs((240 - turnHeight) / 80))
        turn(direction)
        return True
    else:
        ahead(-60, 1)
        return False
    

def ahead(speed, duration):
    move_car('ahead', speed, duration)

def stopCar():
    move_car('stop', 50)

def offsetTurn(speed, duration, direction):
    move_car('turn', speed, duration, direction)

def offsetHorizontal(speed, duration, direction):
    move_car('horizontal', speed, duration, direction)
    
def turn(direction):
    stopCar()
    time.sleep(0.2)
    if direction == 'left':
        move_car('turn', 53, 1, direction)
    else:
        move_car('turn', 53, 1, direction)
    
def turnAround():
    stopCar()
    time.sleep(0.2)
    move_car('turn', 45, 2.5, 'left')
    mqtt_server.driveCar(car_command.TopicStand, 1)
    time.sleep(1)

def back():
    move_car('ahead', 40, 0.6)
    
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