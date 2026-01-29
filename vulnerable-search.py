import sqlite3
import logging
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Đây là user đang đăng nhập 
CURRENT_USER_LOGGED_IN = "sinhvien1"
DB_PASSWORD = 'secret123'  # Dễ lộ nếu commit code


# LỖI 1: SQL Injection + Lộ toàn bộ dữ liệu
@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username')
    
    # Cộng chuỗi trực tiếp -> SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    # Log chứa dữ liệu nhạy cảm
    logging.info(f"Sensitive log: Username: {username}, Query: {query}, DB_PASSWORD: {DB_PASSWORD}")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query) # Thực thi query bẩn
        users = cursor.fetchall() # Lấy tất cả kết quả
        return {"results": users}, 200 # Trả về toàn bộ dữ liệu database
    except Exception as e:
        return {"error": str(e)}, 500 # Lộ chi tiết lỗi hệ thống

# LỖI 2: Broken access Control (IDOR) (Insecure Direct Object References
@app.route('/profile', methods=['GET'])
def profile():
    # Tham số target_user là người mà hacker MUỐN xem
    target_username = request.args.get('username')
    
    # Hệ thống KHÔNG kiểm tra xem 'user1' có quyền xem 'admin' hay không
    # -> Đây là IDOR

    query = f"SELECT * FROM users WHERE username = '{target_username}'"
    
    logging.info(f"IDOR Log: User '{CURRENT_USER_LOGGED_IN}' is viewing profile of: {target_username}")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        user_data = cursor.fetchone()
        
        if user_data:
            return {
                # Server vẫn chào user1, nhưng lại đưa dữ liệu của người khác
                "message": f"Chào {CURRENT_USER_LOGGED_IN}, đây là thông tin hồ sơ bạn yêu cầu.",
                "profile_data": user_data[1]
            }, 200
        else:
            return {"message": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    
if __name__ == '__main__':
    print(f"Đang chạy App Lỗi tại http://127.0.0.1:5000")
    print(f"User hiện tại đang đăng nhập là: {CURRENT_USER_LOGGED_IN}")
    app.run(debug=True, port=5000)