import threading
import signal
import sys
import time
from flask import Flask, request, jsonify
from handlers import dispatch
import servers.mqtt_server as mqtt_server
import local_status

app = Flask(__name__)

status_lock = threading.Lock()

shutdown_event = threading.Event()

@app.route('/getStatus', methods=['GET'])
def get_status():
    return jsonify({"status": str(local_status.CAR_STATUS)})

@app.route('/setStatus', methods=['POST'])
def set_status():
    data = request.get_json()

    print(f"-----------------Status updated to: {data['status']}")

    if data['status'] == 'Line':
        local_status.setLine()
    elif data['status'] == 'Catch':
        local_status.setCatch()
    elif data['status'] == 'Idle':
        local_status.setIdle()
    elif data['status'] == 'Prev':
        local_status.setPreviousStatus()

    return jsonify({"message": "Status updated successfully", "newStatus": str(local_status.CAR_STATUS) }), 200

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