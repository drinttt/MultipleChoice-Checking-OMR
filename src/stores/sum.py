# from flask import Flask, jsonify, request
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # เพิ่มเพียงบรรทัดนี้

# @app.route('/api/add', methods=['POST'])
# def add_numbers():
#     data = request.json
#     result = data['num1'] + data['num2']
#     return jsonify({'result': result})

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, send_file
# from flask_cors import CORS
# import cv2
# import numpy as np
# import tempfile
# import os

# app = Flask(__name__)
# CORS(app)

# @app.route('/api/upload', methods=['POST'])
# def upload_image():
#     file = request.files['file']
#     npimg = np.frombuffer(file.read(), np.uint8)
#     img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

#     # แปลงภาพเป็นขาวดำ
#     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # บันทึกภาพลงในไฟล์ชั่วคราว
#     _, temp_file = tempfile.mkstemp(suffix='.png')
#     cv2.imwrite(temp_file, gray_image)

#     # ส่งไฟล์กลับไปยัง client
#     response = send_file(temp_file, mimetype='image/png')

#     # ลบไฟล์ชั่วคราวหลังจากส่งไฟล์
#     os.remove(temp_file)

#     return response

# if __name__ == '__main__':
#     app.run(debug=True)


# ----------------------------------------width height
# flask_app.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import cv2
# import numpy as np

# app = Flask(__name__)
# CORS(app)

# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     npimg = np.frombuffer(file.read(), np.uint8)
#     img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

#     if img is None:
#         return jsonify({'error': 'Invalid image'}), 400

#     height, width = img.shape[:2]

#     return jsonify({'width': width, 'height': height})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, send_file
from flask_cors import CORS
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/upload-and-convert', methods=['POST'])
def upload_and_convert():
    file = request.files['file']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # แปลงภาพเป็นขาวดำ
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # สร้าง in-memory file
    is_success, buffer = cv2.imencode(".png", gray_image)
    io_buf = BytesIO(buffer)

    return send_file(io_buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
