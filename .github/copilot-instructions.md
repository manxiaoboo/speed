# AI Coding Instructions for Speed Robotics Project

## Architecture Overview

This is a **Raspberry Pi robotics control system** for an autonomous car that follows lines and detects targets using YOLO computer vision. The architecture follows a **state machine pattern** with three main layers:

- **Main Loop**: `main.py` → `servers/server.py` → `handlers/dispatch.py` 
- **State Handlers**: Individual handlers in `handlers/` (line1-5, findABC, find123, etc.)
- **Hardware Control**: MQTT commands via `servers/mqtt_server.py` and camera via `servers/camera_server.py`

## Critical State Management Pattern

The system uses **global state management** via `local_status.py` with enum-based states in `enums.py`. The core pattern:

```python
# Status flows: IDLE → LINE1 → LINE2...LINE5 → FindABC → Find123 → BACK_LINE5...BACK_LINE1 → GO_BACK
if local_status.isLINE1():
    isDone = line1_handler.onImageReceived(frame)
    if isDone:
        setStatus(enums.Status.LINE2)
```

**Key State Variables**:
- `CAR_STATUS`: Current mission state from `enums.Status`
- `CAR_BUSY`: Prevents overlapping commands during movement
- `OUTLOOK[3]`: Vision detection results array for target tracking
- `CAMERA_INDEX`: Switches between line detection ('0') and target detection ('2')

## Movement Command Patterns

All car movement flows through `utils/line_order.py` with **consistent command structure**:

```python
def move_car(action, speed=0, duration=0, direction=None):
    local_status.CAR_BUSY = True
    # MQTT publish to hardware
    if duration > 0:
        time.sleep(duration)  # Blocking execution
    mqtt_server.driveCar(car_command.TopicStop, 50)  # Auto-stop
    local_status.CAR_BUSY = False
```

**Movement Types**: `ahead`, `turn` (with direction), `horizontal`, `stop` - all use MQTT topics from `utils/car_command.py`

## YOLO Vision Integration

Two separate YOLO models loaded at startup in `main.py`:
- **Line Detection**: `yolo_models/detect_line.py` - detects line, left/right turns, endpoints
- **Target Detection**: `yolo_models/detect_target.py` - detects A/B/C letters and t1/t2/t3 numbers

**Detection Pattern**:
```python
results = detect_line.predict(frame, conf=0.1)
if (entity := util.findTurningPoint(results)):  # Uses walrus operator
    do.handleTurning(entity, 'left')
```

Vision utilities in `utils/util.py` parse YOLO JSON output and calculate positioning offsets using image center coordinates (320x240 reference).

## Handler Development Conventions

Each handler in `handlers/` follows the **same interface**:
- `onImageReceived(frame)` → returns `True` when state should advance
- Use `util.find*()` functions to extract entities from YOLO results
- Call movement functions from `utils/line_order.py` or `utils/target_order.py`
- Handle `missAll()` scenarios when no vision targets detected

## Development Workflow

**Local Development**: Python files run on development machine, connect to Raspberry Pi at `192.168.1.5`
**Deployment**: Transfer files to Pi, run with virtual environment `nemoenv`

**Key Commands**:
```bash
# On Raspberry Pi
sudo su
source nemoenv/bin/activate
python flask/flaskCam.py  # Camera server
python CAR/MQTT.py        # MQTT control server

# Development machine
python main.py  # Main control loop on port 5555
```

## Critical Dependencies

- **YOLO Models**: Pre-trained `.pt` files in `yolo_models/` - do not modify without retraining
- **Network**: Hardcoded IPs (192.168.1.5 for Pi, 192.168.1.7 for remote)
- **MQTT Topics**: Defined in `car_command.py` - match hardware configuration
- **Image Dimensions**: 640x480 with center at (320,240) - vision calculations depend on this

## Error Handling Patterns

The system uses **fail-safe defaults**: when vision fails, call `back()` to reverse and retry. The `CAR_BUSY` flag prevents command conflicts during movement sequences.

**Missing Detection Response**: Each handler implements `missAll()` → calls `do.back()` → returns `False` to retry current state.
