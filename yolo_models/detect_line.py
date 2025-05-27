import time
from ultralytics import YOLOv10
import local_status

def loadModel():
    local_status.DETECT_LINE_MODEL = YOLOv10('yolo_models/detect_line_light.pt')
    print('[Model Line Ready]')

def predict(frame):
    if local_status.DETECT_LINE_MODEL is None:
        return []
    else:
        local_status.CAR_BUSY = True
        start_time = time.time()
        results = local_status.DETECT_LINE_MODEL.predict(frame, conf=0.1)
        elapsed_time = time.time() - start_time
        print(f"模型耗时：{elapsed_time:.3f}s")
        results_dict = []
        for bbox in results:
            if len(bbox.boxes) > 0:
                results_dict.append(bbox.tojson())
        local_status.CAR_BUSY = False
        return results_dict