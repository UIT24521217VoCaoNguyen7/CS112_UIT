# Ứng dụng Quản lý Sinh viên - B-Tree Indexing (Animated)

Một ứng dụng Desktop trực quan giúp mô phỏng và khảo sát cách thức hoạt động của cấu trúc dữ liệu cây **B-Tree (B-Tree Indexing)** trong việc lưu trữ, tổ chức và truy xuất thông tin sinh viên. 

Dự án này giúp biến những lý thuyết cấu trúc dữ liệu khô khan thành các hoạt ảnh sinh động, dễ hiểu.

---

## ✨ Các tính năng nổi bật

* **Thêm Sinh Viên:** Nhập thông tin sinh viên mới (MSSV, Họ Tên, Giới tính). Hệ thống tự động cập nhật bản ghi vào Bảng gốc và chèn Khóa (Key) vào cây B-Tree.
* **Tìm Kiếm Trực Quan (Animated Search):** Khi tìm kiếm theo MSSV, ứng dụng hiển thị hiệu ứng hoạt ảnh di chuyển qua từng Node trên cây B-Tree, giúp người dùng dễ dàng theo dõi đường đi của thuật toán duyệt cây.
* **Xóa Sinh Viên (Soft Delete / Xóa Logic):** * *Tại Bảng gốc:* Bản ghi không bị xóa hẳn mà được đánh dấu trạng thái (Status) thành "Đã xóa" để lưu vết.
    * *Tại B-Tree:* Khóa (Key) bị loại bỏ hoàn toàn khỏi cây, và cây sẽ tự động tái cân bằng (Rebalance) để duy trì cấu trúc.
* **Tạo Dữ Liệu Thử Nghiệm (Mock Data):** Chức năng tạo nhanh 10 sinh viên ngẫu nhiên với định dạng MSSV là `XXYY` (ví dụ: `AB12`). Mỗi lần nhấn sẽ tự động reset (clear) toàn bộ dữ liệu cũ và vẽ lại cây mới.

---

## 🛠 Công nghệ sử dụng

* **Ngôn ngữ lập trình:** [C# / Java / C++ - Tùy chỉnh ngôn ngữ bạn dùng]
* **Giao diện (GUI):** [WinForms / WPF / JavaFX - Tùy chỉnh framework]
* **Cấu trúc dữ liệu chính:** B-Tree, Danh sách liên kết / Mảng (cho Bảng gốc).

---

## 🚀 Hướng dẫn cài đặt và chạy thử nghiệm

1. Clone repository này về máy:
   ```bash
   git clone [https://github.com/](https://github.com/)[Tên-Tài-Khoản-Của-Bạn]/[Tên-Repo-Của-Bạn].git
