from ultralytics import YOLOv10
import local_status

def loadModel():
    local_status.DETECT_TARGET_MODEL = YOLOv10('yolo_models/detect_target.pt')
    print('[Model Target Ready]')

def predict(frame):
    if local_status.DETECT_TARGET_MODEL is None:
        return []
    else:
        results = local_status.DETECT_TARGET_MODEL.predict(frame, conf=0.08)
        results_dict = []
        for bbox in results:
            if len(bbox.boxes) > 0:
                results_dict.append(bbox.tojson())
        return results_dict