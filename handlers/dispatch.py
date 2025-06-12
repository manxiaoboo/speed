from handlers import idle_handler, line1_handler, line2_handler, line3_handler, line4_handler, line5_handler, findABC_handler, find123_handler, catch_handler
import time
import cv2
import enums
import local_status
import servers.camera_server as camera_server

def next():
        img = camera_server.takePhoto()
        frame = camera_server.process_image_from_misleading_response(img)
        # cv2.imshow('car', frame)
        # cv2.waitKey(0)
        if local_status.isIDLE():
            idle_handler.onImageReceived(frame)
        elif local_status.isLINE1():
            isDone = line1_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE2)
        elif local_status.isLINE2():    
            isDone = line2_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE3)
        elif local_status.isLINE3():    
            isDone = line3_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE4)
        elif local_status.isLINE4():    
            isDone = line4_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE5)
        elif local_status.isLINE5():    
            isDone = line5_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.FindABC)
        elif local_status.isFindABC():  
            isDone = findABC_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.Find123)
        elif local_status.isFind123():
            isDone = find123_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.Catch)
        elif local_status.isCatch():
            catch_handler.onImageReceived(frame)
        else:
            time.sleep(1)
        
        next()
            
def setStatus(status):
    local_status.CAR_STATUS = status