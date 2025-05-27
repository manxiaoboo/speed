import threading
import signal
import sys
import time
from flask import Flask, request, jsonify
from handlers import dispatch
import servers.mqtt_server as mqtt_server

app = Flask(__name__)

status_lock = threading.Lock()
current_status = "unknown"

shutdown_event = threading.Event()

@app.route('/getStatus', methods=['GET'])
def get_status():
    return jsonify({"status": current_status})

@app.route('/setStatus', methods=['POST'])
def set_status():
    data = request.get_json()
    print(f"Status updated to: {data}")
    #  with status_lock:
    #         global current_status # 声明要修改全局变量
    #         current_status = new_status
    #         print(f"Status updated to: {current_status}")
    # if data and 'status' in data:
    #     new_status = data['status']
    #     global current_status # 声明要修改全局变量
    #     current_status = new_status
    #     print(f"Status updated to: {current_status}")
    #     # 返回成功消息和新的状态
    #     return jsonify({"message": "Status updated successfully", "new_status": current_status}), 200
    # else:
    #     print("Invalid request: Missing or invalid JSON body")
    #     # 如果请求体不符合要求，返回错误信息和 400 状态码
    #     return jsonify({"error": "Invalid request. Please provide a JSON body with a 'status' key."}), 400
    return jsonify({"message": "Status updated successfully", "new_status": current_status}), 200

def run_flask_server(port):
    app.run(host='localhost', port=port)

def run_mqtt_server():
    mqtt_server.listen()
    
def run_go():
    dispatch.next()

def signal_handler(signum, frame):
    shutdown_event.set()

def listen(port):
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    flask_thread = threading.Thread(target=run_flask_server, args=(port,), daemon=True)
    mqtt_thread = threading.Thread(target=run_mqtt_server, daemon=True)
    go_thread = threading.Thread(target=run_go, daemon=True)
    flask_thread.start()
    mqtt_thread.start()
    go_thread.start()
    while not shutdown_event.is_set():
        time.sleep(0.1)
    print("Application shutting down.")
    sys.exit(0)