import numpy as np
import cv2
import time
import requests
import local_status

# def listen(callback):
    # 设置树莓派视频流地址
    # video_url = "http://192.168.1.5:5000/video_feed/0"  # 替换为树莓派的实际 IP 地址
    # 打开视频流请求
    # stream = requests.get(video_url, stream=True)
    
    # if stream.status_code != 200:
    #     print(f"Failed to connect to video stream: {stream.status_code}")
    #     exit()
    

    
    # callback("pictures5/captured_image_20250516_152539.jpg")
    
    # time_index = 1
    
    # 读取 HTTP 响应内容
    # byte_data = b""
    # for chunk in stream.iter_content(chunk_size=1024):
    #     byte_data += chunk
    #     # 搜索 JPEG 图片的开始和结束位置
    #     start = byte_data.find(b'\xff\xd8')  # JPEG 开始标志
    #     end = byte_data.find(b'\xff\xd9')  # JPEG 结束标志
    #     if start != -1 and end != -1:
    #             # 提取 JPEG 数据
    #             jpg_data = byte_data[start:end+2]
    #             byte_data = byte_data[end+2:]
    #             # 将 JPEG 数据解码为图像
    #             frame = cv2.imdecode(np.frombuffer(jpg_data, np.uint8), cv2.IMREAD_COLOR)
    #             callback(frame)
    #             # if time_index > 5:
    #             #     timestamp = time.strftime("%Y%m%d_%H%M%S")
    #             #     filename = f'pictures5/captured_image_{timestamp}.jpg'
    #             #     # 保存照片
    #             #     cv2.imwrite(filename, frame)
    #             #     print(f"照片已保存！文件名: {filename}")
    #             #     time_index = 1
    #             # time_index += 1
    #         # cv2.imwrite("./pictures/pic_now2.jpg", frame)
    #         # local_status.Catch_Img = False
    #         # callback(frame)
    
def takePhoto():
    start_time = time.time()
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    res = requests.get(local_status.getImageUrl(), headers=headers)
    res = requests.get(local_status.getImageUrl(), headers=headers)
    # local_status.updateImage(res.content)
    elapsed_time = time.time() - start_time
    print(f"图片请求：{elapsed_time:.3f}s")
    return res.content

def listen():
    try:
        while not local_status.CAR_BUSY:
            start_time = time.time()
            res = requests.get(local_status.getImageUrl())
            local_status.updateImage(res.content)
            elapsed_time = time.time() - start_time
            print(f"图片请求：{elapsed_time:.3f}s")
    except requests.RequestException as e:
        print(f"请求失败: {e}")
    except KeyboardInterrupt:
        print("程序终止")

def process_image_from_misleading_response(response_content: bytes):
    start_time = time.time()
    if not isinstance(response_content, bytes):
        print("Error: Input must be bytes (the raw response content).")
        return None

    try:
        # Convert the raw bytes into a NumPy array buffer.
        # This doesn't interpret it as an image yet, just wraps the bytes data.
        img_buffer = np.frombuffer(response_content, np.uint8)

        # Use cv2.imdecode to interpret the buffer as an image and decode it.
        # cv2.IMREAD_COLOR reads the image in color (BGR format, which is OpenCV's default).
        # This function is robust and can often guess the image format (JPEG, PNG etc.)
        # from the bytes data itself, ignoring the HTTP header.
        image_array = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

        if image_array is None:
            print("Error: cv2.imdecode failed to decode the bytes as an image.")
            print("This likely means the bytes data is not valid image format (e.g., not JPEG, PNG, etc.),")
            print("or the data is corrupted.")
            return None

        print(f"Successfully decoded bytes into image array with shape: {image_array.shape}")
        print(f"Data type: {image_array.dtype}")

        # The returned array is typically (Height, Width, Channels) in BGR format, uint8 type.
        # This is a common format for subsequent image processing steps before feeding to YOLOv10.
        elapsed_time = time.time() - start_time
        print(f"图片转换：{elapsed_time:.3f}s")
        return image_array

    except Exception as e:
        # Catch potential errors during np.frombuffer or other unexpected issues
        print(f"An error occurred during image processing: {e}")
        return None