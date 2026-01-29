import sqlite3

connection = sqlite3.connect('database.db')

with connection:
    # 1. Tạo bảng users
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT
        );
    """)
    
    # 2. Xóa sạch dữ liệu cũ để tránh trùng lặp/lỗi
    connection.execute("DELETE FROM users;")
    connection.execute("DELETE FROM sqlite_sequence WHERE name='users';") # Reset ID về 1

    # 3. Thêm dữ liệu mẫu (Đã có sinhvien1)
    users = [
        # ID 1: Admin (Mục tiêu để hack) - Password lộ rõ
        ('admin', 'secret123', 'admin@school.edu.vn'),
        
        # ID 2: Sinh viên 1 (User chính của bạn)
        ('sinhvien1', '123456', 'sinhvien1@school.edu.vn'),
        
        # ID 3: User khác
        ('giangvien', 'gv_pass', 'gv@school.edu.vn')
    ]
    
    connection.executemany('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', users)

print("✅ Đã tạo Database thành công! Có user: admin và sinhvien1")
connection.close()