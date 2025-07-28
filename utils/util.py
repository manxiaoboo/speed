import json
from typing import List, Dict, Any
import local_status

def findTurningPoint(results):
    return findEntity(results, ['left', 'right'])

def findLine(results):
    return findEntity(results, ['line'])

def findEnd(results):
    return findEntity(results, ['end'])

def findA(results):
    return findEntity(results, ['A'])

def findB(results):
    return findEntity(results, ['B'])

def findC(results):
    return findEntity(results, ['C'])

def findTargetABC(results, target):
    if target == "A":
        return findA(results)
    elif target == "B":
        return findB(results)
    elif target == "C":
        return findC(results)
    
def findTarget123(results, target):
    if target == "1":
        return findT1(results)
    elif target == "2":
        return findT2(results)
    elif target == "3":
        return findT3(results)
    
def findALL123(results):
    findEntity(results, ["t1", "t2", "t3"])

def findAllABC(results):
    return findEntity(results, ["A", "B", "C"])


def findT1(results):
    return findEntity(results, ['t1'])

def findT2(results):
    return findEntity(results, ['t2'])

def findT3(results):
    return findEntity(results, ['t3'])

def findEntity(yolo_output_strings: List[str], labels):
    all_objects: List[Dict[str, Any]] = []

    for json_str in yolo_output_strings:
        try:
            objects_list = json.loads(json_str)
            if isinstance(objects_list, list):
                all_objects.extend(objects_list)
            else:
                print(f"Warning: Expected a JSON array, but got {type(objects_list)} from string: {json_str[:50]}...")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON string: {e} in string: {json_str[:50]}...")
        except Exception as e:
            print(f"An unexpected error occurred while processing JSON string: {e} in string: {json_str[:50]}...")

    line_objects = [
        obj for obj in all_objects
        if isinstance(obj, dict) and (obj.get('name') in labels)
    ]

    if not line_objects:
        return None
    else:
        highest_confidence_line = max(line_objects, key=lambda obj: obj['confidence'])
        return highest_confidence_line


def getCenterPositionX(x1, x2):
    return (x1 + x2) / 2.0

def getWidth(x1, x2):
    return x2 - x1

def getHeight(y1, y2):
    return y2 - y1

def getCenterPositionY(y1, y2):
    return (y1 + y2) / 2.0

def calcDifferenceX(centerX):
    return centerX - (local_status.IMAGE_WIDTH / 2.0)

def calcDifferenceY(centerY):
    return centerY - (local_status.IMAGE_HEIGHT / 2.0)

def calcDifferenceWidth(width):
    return width - local_status.NORMAL_LINE_WIDTH