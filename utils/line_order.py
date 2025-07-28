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
        
    if abs(differenceX) > 130:
        print('handleH============>', abs(differenceX))
        handleOffsetH(entity)
        return False
    
    if abs(differenceWidth) > 25 and abs(differenceX) > 28:
        print('handleDirection=============>', abs(differenceWidth))
        handleOffsetDirection(entity)
        return False
    
    return True

def handleOffsetDirection(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineWidth = util.getWidth(x1, x2)
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    differenceWidth = util.calcDifferenceWidth(lineWidth)
    turn_size = abs(differenceWidth) / 130 * 0.25
    print(f"turn  {turn_size}")
    if turn_size < 0.04:
        turn_size = 0.04
    if differenceX > 0:
        offsetTurn(22, turn_size, 'right')
    elif differenceX < 0:
        offsetTurn(22, turn_size, 'left')
    

def handleOffsetH(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    horizontal_size = abs(differenceX) / 90 * 0.25
    if horizontal_size < 0.04:
        horizontal_size = 0.04
    print(f"Move H {horizontal_size}")
    if differenceX > 0:
        offsetHorizontal(40, horizontal_size, 'left')
    elif differenceX < 0:
        offsetHorizontal(40, horizontal_size, 'right')


def handleLine(entity):
    if handleOffset(entity) == False:
        return False
    
    # ahead(-20, 0.2)
    # ahead(-30, 0.2)
    # ahead(-45, 0.2)
    ahead(-70, 1.7)
    # ahead(-45, 0.2)
    # ahead(-20, 0.2)

def handleEnd(entity):
    box = entity['box']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterY = util.getCenterPositionY(y1, y2)
    differenceY = util.calcDifferenceY(lineCenterY)
    handleOffset(entity)
    if differenceY > 0:
        print('==TrunAround Now End')
        ahead(-48, 2.5)
        turnAround()
        return True
    elif 180 <= abs(differenceY) <= 240:
        print('==Run 4.4s End')
        ahead(-48, 4.4)
        turnAround()
        return True
    elif 120 <= abs(differenceY) < 180:
        print('==Run 4s End')
        ahead(-48, 4)
        turnAround()
        return True
    elif 60 <= abs(differenceY) < 120:
        print('==Run 3.8s End')
        ahead(-48, 3.8)
        turnAround()
        return True
    elif abs(differenceY) < 60:
        print('==Run 3.5s End')
        ahead(-48, 3.5)
        turnAround()
        return True
        
    return False
        
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
    
    if differenceY < 0:
        ahead(-62, abs((240 - turnHeight) / 72))
        turn(direction)
        return True
    
        
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
    move_car('turn', 53, 1.2, direction)
    
def turnAround():
    move_car('turn', 25, 6.2, 'left')
    mqtt_server.driveCar(car_command.TopicStand, 1)
    time.sleep(1)

def back():
    move_car('ahead', 40, 0.4)
    
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