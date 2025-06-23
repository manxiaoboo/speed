from enum import Enum

class Status(Enum):
    IDLE = 'idle'
    LINE1 = 'line1'
    LINE2 = 'line2'
    LINE3 = 'line3'
    LINE4 = 'line4'
    LINE5 = 'line5'
    BACK_LINE1 = 'backline1'
    BACK_LINE2 = 'backline2'
    BACK_LINE3 = 'backline3'
    BACK_LINE4 = 'backline4'
    BACK_LINE5 = 'backline5'
    GO_BACK = 'goback'
    FindABC = 'findABC'
    Find123 = 'find123'
    Catch = 'catch'
    
class CameraIndex(Enum):
    LINE = '0'
    TARGET = '1'
    
class YOLOLineModelClasses(Enum):
    line = 0
    left = 1
    right = 2
    end = 3
    
class YOLOTargetModelClasses(Enum):
    A = 0
    B = 1
    C = 2
    t1 = 3
    t2 = 4
    t3 = 5