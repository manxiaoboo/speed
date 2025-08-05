import time
from ultralytics import YOLOv10
import local_status

def loadModel():
    local_status.DETECT_LINE_MODEL = YOLOv10('yolo_models/detect_line.pt')
    print('[Model Line Ready]')

def predict(frame, conf = 0.1):
    if local_status.DETECT_LINE_MODEL is None:
        return []
    else:
        local_status.CAR_BUSY = True
        results = local_status.DETECT_LINE_MODEL.predict(frame, conf=conf)
        results_dict = []
        for bbox in results:
            if len(bbox.boxes) > 0:
                results_dict.append(bbox.tojson())
        local_status.CAR_BUSY = False
        print(results_dict)
        return results_dict