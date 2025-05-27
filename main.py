import servers.server as server
from yolo_models import detect_line, detect_target

detect_line.loadModel()
detect_target.loadModel()

server.listen(5555)