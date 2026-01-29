import sqlite3
import logging
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

app = Flask(__name__)
DB_PATH = os.getenv('DB_PATH') # Lấy đường dẫn DB từ env
DB_PASSWORD = os.getenv('DB_PASSWORD')  # Minh họa secrets management (dù SQLite không cần, nhưng dùng env/secret store)

# Chỉ log Warning trở lên, không log Info rác
logging.basicConfig(level=logging.WARNING)

# Giả lập Session: Người đang đăng nhập là 'sinhvien1'
CURRENT_USER_LOGGED_IN = "sinhvien1"

#Secure search app
@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username')

    # 1. Input Validation
    if not username:
        return jsonify({"message": "Vui lòng nhập username"}), 400
    
    # Chỉ cho phép chữ cái và số (chặn ký tự đặc biệt như ' - ;)
    if not username.isalnum():
        logging.warning(f"Phát hiện input không hợp lệ") 
        return jsonify({"message": "Username chứa ký tự không hợp lệ"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 2. Parameterized Query (Chống SQL Injection)
        sql = "SELECT username, email FROM users WHERE username = ?"
        cursor.execute(sql, (username,))
        
        user = cursor.fetchone()
        
        if user:
            # 3. Output Encoding (Trả về JSON sạch)
            return jsonify({
                "username": user[0],
                "email": user[1]
                # Không trả về password hay id
            }), 200
        else:
            return jsonify({"message": "Không tìm thấy user"}), 404

    except Exception:
        # 4. Error Handling an toàn
        logging.error("Lỗi kết nối CSDL") 
        return jsonify({"message": "Lỗi hệ thống, vui lòng thử lại sau"}), 500
    finally:
        conn.close()

# Secure profile app 
@app.route('/profile', methods=['GET'])
def profile():
    target_username = request.args.get('username')

    # 1. AUTHORIZATION CHECK (Kiểm tra quyền)
    # Nếu người muốn xem (target) KHÁC người đang đăng nhập (current) -> CẤM
    if target_username != CURRENT_USER_LOGGED_IN:
        logging.warning(f"Cảnh báo: User '{CURRENT_USER_LOGGED_IN}' cố tình truy cập trái phép vào '{target_username}'")
        return jsonify({
            "error": "TRUY CẬP BỊ TỪ CHỐI ",
            "message": "Bạn chỉ được xem hồ sơ của chính mình!"
        }), 403

    # Nếu đúng là chính chủ, mới cho kết nối DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Dùng Parameterized Query luôn cho chắc
        sql = "SELECT * FROM users WHERE username = ?"
        cursor.execute(sql, (target_username,))
        user_data = cursor.fetchone()
        
        if user_data:
            return {
                "message": f"Chào {CURRENT_USER_LOGGED_IN}, đây là thông tin hồ sơ của bạn.",
                # Trả về object đẹp như bạn muốn
                "profile_data": {
                    "username": user_data[1],
                    "email": user_data[3]
                }
            }, 200
        else:
            return jsonify({"message": "User not found"}), 404
            
    except Exception:
        return jsonify({"message": "Lỗi hệ thống"}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    print("Đang chạy APP BẢO MẬT tại http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
