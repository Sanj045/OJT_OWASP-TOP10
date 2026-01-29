# 🛡️ Web Security Demo: OWASP Top 10 (SQL Injection & IDOR)

**Mô tả:** Dự án demo các lỗ hổng bảo mật web phổ biến và cách khắc phục chúng bằng kỹ thuật Secure Coding trong Python Flask.
Dự án bao gồm 2 phiên bản đối lập:
1.  **🛑 Vulnerable App:** Ứng dụng chứa lỗ hổng (SQL Injection, IDOR, Sensitive Data Exposure).
2.  **✅ Secure App:** Ứng dụng đã được vá lỗi (Input Validation, Parameterized Query, Authorization Check).

---

## 🚀 Các lỗ hổng được Demo

| Tính năng | Lỗ hổng (Vulnerable) | Giải pháp (Secure) | Loại lỗi OWASP |
| :--- | :--- | :--- | :--- |
| **Search User** | **SQL Injection**: Cộng chuỗi trực tiếp, kẻ tấn công có thể lấy toàn bộ dữ liệu. | **Parameterized Query**: Sử dụng `?` để binding dữ liệu, ngăn chặn mã độc. | A03: Injection |
| **User Profile** | **IDOR**: Sinh viên có thể xem trộm hồ sơ Admin bằng cách đổi tham số trên URL. | **Authorization Check**: Kiểm tra quyền sở hữu (`current_user == target_user`) trước khi trả về dữ liệu. | A01: Broken Access Control |
| **Logging** | **Sensitive Data Exposure**: Ghi mật khẩu DB và query vào file log. | **Secure Logging**: Không ghi dữ liệu nhạy cảm, chỉ log các cảnh báo cần thiết. | A09: Security Logging Failures |

---

## 🛠️ Cài đặt & Chạy dự án

### 1. Yêu cầu hệ thống
* Python 3.x
* Pip

### 2. Cài đặt thư viện
Mở terminal tại thư mục dự án và chạy lệnh:
```bash
pip install flask python-dotenv
```
### 3. Cấu hình Database & Môi trường
Bước 1: Tạo file .env (nếu chưa có) và thêm nội dung sau:
```bash
DB_PATH=database.db
DB_PASSWORD=secret123
```
Bước 2: Khởi tạo dữ liệu mẫu (Reset Database):
Chạy lệnh sau để tạo database với 2 user mẫu (admin và sinhvien1):
```bash
python init_db.py
```

