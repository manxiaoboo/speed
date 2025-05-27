import time
import utils.car_command as car_command
import servers.mqtt_server as mqtt_server
import utils.util as util
import local_status
    
def handleOffset(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    
    if differenceX > 120:
        local_status.CAR_BUSY = True
        mqtt_server.driveCar(car_command.TopicMoveT, 20)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveH, -40)
        time.sleep(0.7)
        stopCar()
        local_status.CAR_BUSY = False
    elif differenceX < -120:
        local_status.CAR_BUSY = True
        mqtt_server.driveCar(car_command.TopicMoveT, -20)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveH, 40)
        time.sleep(0.7)
        stopCar()
        local_status.CAR_BUSY = False
    

def handleLine(entity):
    box = entity['box']
    x1 = box['x1']
    x2 = box['x2']
    lineCenterX = util.getCenterPositionX(x1, x2)
    differenceX = util.calcDifferenceX(lineCenterX)
    handleOffset(entity)
    
    if abs(differenceX) <= 90:
        local_status.CAR_BUSY = True
        mqtt_server.driveCar(car_command.TopicMoveV, -20)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveV, -30)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveV, -45)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveV, -70)
        time.sleep(1.2)
        mqtt_server.driveCar(car_command.TopicMoveV, -45)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveV, -20)
        time.sleep(0.2)
        local_status.CAR_BUSY = False
        stopCar()
    elif 90 < abs(differenceX) <= 120:
        local_status.CAR_BUSY = True
        mqtt_server.driveCar(car_command.TopicMoveV, -20)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveV, -30)
        time.sleep(0.2)
        mqtt_server.driveCar(car_command.TopicMoveV, -60)
        time.sleep(0.7)
        mqtt_server.driveCar(car_command.TopicMoveV, -20)
        time.sleep(0.2)
        local_status.CAR_BUSY = False
        stopCar()

def handleEnd(entity):
    box = entity['box']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterY = util.getCenterPositionY(y1, y2)
    differenceY = util.calcDifferenceY(lineCenterY)
    if differenceY > 0:
        local_status.CAR_BUSY = True
        ahead(-52)
        time.sleep(0.5)
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif 180 <= abs(differenceY) <= 240:
        stopCar()
        local_status.CAR_BUSY = True
        print('==Run 1.6s End')
        ahead(-42)
        time.sleep(1.6)
        
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif 120 <= abs(differenceY) < 180:
        stopCar()
        local_status.CAR_BUSY = True
        print('==Run 2s End')
        ahead(-42)
        time.sleep(2)
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif 60 <= abs(differenceY) < 120:
        stopCar()
        local_status.CAR_BUSY = True
        ahead(-42)
        print('==Run 1.5s End')
        time.sleep(1.5)
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif abs(differenceY) < 60:
        stopCar()
        local_status.CAR_BUSY = True
        # pre action
        ahead(-42)
        print('==Run 1s End')
        time.sleep(1)
        stopCar()
        local_status.CAR_BUSY = False
        return True
        
    return False
        
def handleTruning(entity, direction):
    box = entity['box']
    y1 = box['y1']
    y2 = box['y2']
    lineCenterY = util.getCenterPositionY(y1, y2)
    differenceY = util.calcDifferenceY(lineCenterY)
    if differenceY > 0:
        print('==Trun Now Turn:' + direction)
        local_status.CAR_BUSY = True
        ahead(-52)
        time.sleep(1.4)
        # turn
        turn(direction)
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif 180 <= abs(differenceY) <= 240:
        stopCar()
        local_status.CAR_BUSY = True
        print('==Run 3.8s Turn:' + direction)
        # pre action
        ahead(-42)
        time.sleep(3.8)
        # turn
        turn(direction)
        
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif 120 <= abs(differenceY) < 180:
        stopCar()
        local_status.CAR_BUSY = True
        # pre action
        print('==Run 3s Turn:' + direction)
        ahead(-42)
        time.sleep(3)
        # turn
        turn(direction)
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif 60 <= abs(differenceY) < 120:
        stopCar()
        local_status.CAR_BUSY = True
        # pre action
        ahead(-42)
        print('==Run 2.5s Turn:' + direction)
        time.sleep(2.5)
        # turn
        turn(direction)
        stopCar()
        local_status.CAR_BUSY = False
        return True
    elif abs(differenceY) < 60:
        stopCar()
        local_status.CAR_BUSY = True
        # pre action
        ahead(-42)
        print('==Run 2s Turn:' + direction)
        time.sleep(2)
        # turn
        turn(direction)
        stopCar()
        local_status.CAR_BUSY = False
        return True
        
    return False

def ahead(speed):
    mqtt_server.driveCar(car_command.TopicMoveV, speed)

def stopCar():
    mqtt_server.driveCar(car_command.TopicStop, 50)
    
def turn(direction):
    if direction == 'left':
        mqtt_server.driveCar(car_command.TopicMoveT, -20)
    elif direction == 'right':
        mqtt_server.driveCar(car_command.TopicMoveT, 20)
    time.sleep(4.3)
    
def turnAround():
    mqtt_server.driveCar(car_command.TopicMoveT, -20)
    time.sleep(8.8)
    stopCar()

def back():
    ahead(40)
    time.sleep(0.4)
    stopCar()