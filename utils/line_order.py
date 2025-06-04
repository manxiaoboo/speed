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
    
    if differenceX > 140:
        offsetTurn(20, 0.25, 'right')
        offsetHorizontal(40, 0.6, 'left')
    elif differenceX < -140:
        offsetTurn(20, 0.25, 'left')
        offsetHorizontal(40, 0.6, 'right')
    

def handleLine(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    handleOffset(entity)
    
    if abs(differenceX) <= 110:
        ahead(-20, 0.2)
        ahead(-30, 0.2)
        ahead(-45, 0.2)
        ahead(-70, 1.2)
        ahead(-45, 0.2)
        ahead(-20, 0.2)
    elif 110 < abs(differenceX) <= 140:
        ahead(-20, 0.2)
        ahead(-30, 0.2)
        ahead(-60, 0.7)
        ahead(-20, 0.2)

def handleEnd(entity):
    box = entity['box']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterY = util.getCenterPositionY(y1, y2)
    differenceY = util.calcDifferenceY(lineCenterY)
    if differenceY > 0:
        print('==TrunAround Now End')
        ahead(-52, 0.5)
        turnAround()
        return True
    elif 180 <= abs(differenceY) <= 240:
        print('==Run 1.6s End')
        ahead(-42, 1.6)
        turnAround()
        return True
    elif 120 <= abs(differenceY) < 180:
        print('==Run 2s End')
        ahead(-42, 2)
        turnAround()
        return True
    elif 60 <= abs(differenceY) < 120:
        print('==Run 1.5s End')
        ahead(-42, 1.5)
        turnAround()
        return True
    elif abs(differenceY) < 60:
        print('==Run 1s End')
        ahead(-42, 1)
        turnAround()
        return True
        
    return False
        
def handleTurning(entity, direction):
    box = entity['box']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterY = util.getCenterPositionY(y1, y2)
    differenceY = util.calcDifferenceY(lineCenterY)
    if differenceY > 0:
        print('==Trun Now Turn:' + direction)
        ahead(-52, 1.4)
        turn(direction)
        return True
    elif 180 <= abs(differenceY) <= 240:
        print('==Run 3.8s Turn:' + direction)
        ahead(-42, 3.8)
        turn(direction)
        return True
    elif 120 <= abs(differenceY) < 180:
        print('==Run 3s Turn:' + direction)
        ahead(-42, 3)
        turn(direction)
        return True
    elif 60 <= abs(differenceY) < 120:
        print('==Run 2.5s Turn:' + direction)
        ahead(-42, 2.5)
        turn(direction)
        return True
    elif abs(differenceY) < 60:
        print('==Run 2s Turn:' + direction)
        ahead(-42, 2)
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
    move_car('turn', 20, 4.3, direction)
    
def turnAround():
    local_status.setCamera('2')
    camera_server.takePhoto()
    move_car('turn', 20, 8.8, 'left')
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