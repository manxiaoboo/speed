import cv2
import time
import camera
import local_status
import car_command
# import xunji
import mqttToCar
import ui

def onImageReceived(frame):
    local_status.Catch_Img = False
    cv2.imshow("Video Stream", frame)
    print('received')
    # mqttToCar.driveCar(car_command.TopicMoveT, 50)
    # time.sleep(3)
    # mqttToCar.driveCar(car_command.TopicStop, 50)
    
mqttToCar.listen()
camera.listen()
ui.show()
# driveInfo = xunji.main()
# mqttToCar.driveCar(driveInfo.topic, driveInfo.speed)
# 执行 getPictures.py, 存好图片 （目前其中是Bill提供的示例代码）

# 识别图片，判断新的行动行为 （核心代码）

# 向小车的mqtt server发送指令 （参考mqttToCar.py）