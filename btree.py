import tkinter as tk
from tkinter import ttk, messagebox
import random

# ==========================================
# 1. CẤU TRÚC DỮ LIỆU B-TREE (Bậc 3 / 2-3 Tree)
# ==========================================
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []      
        self.children = []  

class BTree:
    def __init__(self):
        self.root = BTreeNode(True)
        self.order = 3  

    # Hàm search cải tiến: Trả về thêm 'path' (đường đi) để làm animation
    def search_with_path(self, k, node=None, path=None):
        if path is None: path = []
        if node is None: node = self.root
        
        path.append(node) # Ghi nhận node đang đi qua
        
        i = 0
        while i < len(node.keys) and k > node.keys[i][0]:
            i += 1
            
        if i < len(node.keys) and k == node.keys[i][0]:
            return (node, i, path)
        elif node.leaf:
            return (None, None, path)
        else:
            return self.search_with_path(k, node.children[i], path)

    def search(self, k, node=None):
        res = self.search_with_path(k, node)
        return (res[0], res[1]) if res[0] else None

    def insert(self, k_tuple):
        promoted = self._insert_recursive(self.root, k_tuple)
        if promoted:
            new_root = BTreeNode(leaf=False)
            new_root.keys = [promoted[0]]
            new_root.children = [self.root, promoted[1]]
            self.root = new_root

    def _insert_recursive(self, node, k_tuple):
        i = 0
        while i < len(node.keys) and k_tuple[0] > node.keys[i][0]:
            i += 1

        if node.leaf:
            node.keys.insert(i, k_tuple)
        else:
            promoted = self._insert_recursive(node.children[i], k_tuple)
            if promoted:
                node.keys.insert(i, promoted[0])
                node.children.insert(i + 1, promoted[1])

        if len(node.keys) > self.order - 1:
            return self._split(node)
        return None

    def _split(self, node):
        mid_index = len(node.keys) // 2
        promoted_key = node.keys[mid_index]
        
        new_right = BTreeNode(leaf=node.leaf)
        new_right.keys = node.keys[mid_index + 1:]
        
        node.keys = node.keys[:mid_index]
        
        if not node.leaf:
            new_right.children = node.children[mid_index + 1:]
            node.children = node.children[:mid_index + 1]
            
        return (promoted_key, new_right)

    def get_inorder(self, node=None, result=None):
        if result is None: result = []
        if node is None: node = self.root
        for i in range(len(node.keys)):
            if not node.leaf:
                self.get_inorder(node.children[i], result)
            result.append(node.keys[i])
        if not node.leaf:
            self.get_inorder(node.children[len(node.keys)], result)
        return result

    def delete_key(self, mssv):
        inorder_keys = self.get_inorder()
        inorder_keys = [k for k in inorder_keys if k[0] != mssv]
        self.root = BTreeNode(True)
        for k in inorder_keys:
            self.insert(k)


# ==========================================
# 2. GIAO DIỆN NGƯỜI DÙNG (Tkinter UI)
# ==========================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Quản lý Sinh viên - B-Tree Indexing (Animated)")
        self.root.geometry("1150x750")

        self.students = {} 
        self.pointer_counter = 1
        self.btree = BTree()
        
        # Cờ trạng thái để khóa nút bấm khi đang chạy animation
        self.is_animating = False 

        self.setup_ui()

    def setup_ui(self):
        left_frame = tk.Frame(self.root, width=320, bg="#f0f0f0", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left_frame, text="THÔNG TIN SINH VIÊN", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        tk.Label(left_frame, text="Mã SV (MSSV):", bg="#f0f0f0").pack(anchor="w")
        self.entry_mssv = tk.Entry(left_frame, font=("Arial", 12))
        self.entry_mssv.pack(fill=tk.X, pady=5)

        tk.Label(left_frame, text="Họ và Tên:", bg="#f0f0f0").pack(anchor="w")
        self.entry_name = tk.Entry(left_frame, font=("Arial", 12))
        self.entry_name.pack(fill=tk.X, pady=5)

        tk.Label(left_frame, text="Giới tính:", bg="#f0f0f0").pack(anchor="w")
        self.cb_gender = ttk.Combobox(left_frame, values=["Nam", "Nữ", "Khác"], font=("Arial", 12), state="readonly")
        self.cb_gender.current(0)
        self.cb_gender.pack(fill=tk.X, pady=5)

        tk.Button(left_frame, text="➕ Thêm Sinh Viên", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.add_student).pack(fill=tk.X, pady=5)
        
        # Nút Tạo dữ liệu mẫu
        tk.Button(left_frame, text="⚡ Tạo 10 SV Test", bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), command=self.generate_test_data).pack(fill=tk.X, pady=5)
        
        tk.Label(left_frame, text="-"*40, bg="#f0f0f0").pack(pady=5)
        
        tk.Button(left_frame, text="🔍 Tìm Kiếm (Có Hoạt Ảnh)", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=self.search_student).pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="🗑️ Xóa Sinh Viên", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=self.delete_student).pack(fill=tk.X, pady=5)

        self.lbl_status = tk.Label(left_frame, text="", bg="#f0f0f0", fg="blue", wraplength=280, font=("Arial", 11, "bold"))
        self.lbl_status.pack(pady=20)

        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Frame(right_frame, height=400, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        tk.Label(self.canvas_frame, text="Minh họa B-Tree Index (Key: MSSV)", font=("Arial", 10, "bold"), bg="white").pack(anchor="nw")
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.on_canvas_resize)

        bottom_frame = tk.Frame(right_frame, height=250)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        frame_asc = tk.Frame(bottom_frame, width=200)
        frame_asc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_asc, text="Index: MSSV_asc (Từ B-Tree)", font=("Arial", 10, "bold")).pack()
        self.tree_asc = ttk.Treeview(frame_asc, columns=("MSSV", "Pointer"), show="headings", height=10)
        self.tree_asc.heading("MSSV", text="MSSV")
        self.tree_asc.heading("Pointer", text="Pointer")
        self.tree_asc.column("MSSV", width=80)
        self.tree_asc.column("Pointer", width=60, anchor='center')
        self.tree_asc.pack(fill=tk.BOTH, expand=True)

        frame_sv = tk.Frame(bottom_frame, width=500)
        frame_sv.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_sv, text="Bảng Gốc: SinhVien", font=("Arial", 10, "bold")).pack()
        self.tree_sv = ttk.Treeview(frame_sv, columns=("Pointer", "MSSV", "HoTen", "GioiTinh", "Status"), show="headings", height=10)
        for col, width in zip(("Pointer", "MSSV", "HoTen", "GioiTinh", "Status"), (60, 80, 180, 80, 100)):
            self.tree_sv.heading(col, text=col)
            self.tree_sv.column(col, width=width, anchor='center' if col in ("Pointer", "GioiTinh", "Status") else 'w')
        self.tree_sv.pack(fill=tk.BOTH, expand=True)
        
        self.tree_sv.tag_configure('deleted', background='#ffe0e0', foreground='gray')
        self.tree_sv.tag_configure('highlight', background='#fff0b3')

    def on_canvas_resize(self, event):
        """Được gọi mỗi khi kích thước canvas thay đổi"""
        # Lưu lại chiều rộng mới
        self.current_canvas_width = event.width
        # Chỉ vẽ lại nếu hệ thống không đang chạy animation để tránh giật lag
        if not self.is_animating:
            self.draw_btree()
    # ==========================================
    # 3. CÁC THAO TÁC XỬ LÝ
    # ==========================================
    
    # HÀM MỚI: Tạo mã ngẫu nhiên định dạng XXYY
    def _tao_mssv_ngau_nhien(self):
        char1 = chr(random.randint(65, 90))
        char2 = chr(random.randint(65, 90))
        num1 = random.randint(0, 9)
        num2 = random.randint(0, 9)
        return f"{char1}{char2}{num1}{num2}"

    # CẬP NHẬT: Hàm tạo 10 sinh viên test giống logic C#
    def generate_test_data(self):
        if self.is_animating: return
        
        # 1. Reset toàn bộ dữ liệu hiện có
        self.students.clear()
        self.btree = BTree()  # Tạo lại cây B-Tree mới tinh
        self.pointer_counter = 1
        
        # 2. Tạo 10 sinh viên mới
        for _ in range(10):
            # Đảm bảo MSSV không trùng
            while True:
                mssv_moi = self._tao_mssv_ngau_nhien()
                # Nếu search trong cây chưa có thì thoát vòng lặp
                if not self.btree.search(mssv_moi):
                    break
            
            # Random giới tính
            gioi_tinh = "Nam" if random.randint(0, 1) == 0 else "Nữ"
            pointer = self.pointer_counter
            
            # Khởi tạo dữ liệu SV
            self.students[pointer] = {
                "MSSV": mssv_moi, 
                "HoTen": f"Sinh viên {mssv_moi}", 
                "GioiTinh": gioi_tinh, 
                "isDeleted": False
            }
            
            # 3. Thêm vào danh sách và B-Tree
            self.btree.insert((mssv_moi, pointer))
            self.pointer_counter += 1
                
        self.lbl_status.config(text="⚡ Đã reset và tạo tự động 10 sinh viên mới!")
        self.refresh_ui()

    def add_student(self):
        if self.is_animating: return
        mssv = self.entry_mssv.get().strip().upper()
        name = self.entry_name.get().strip()
        gender = self.cb_gender.get()

        if not mssv or not name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đủ MSSV và Họ Tên!")
            return

        if self.btree.search(mssv):
            messagebox.showwarning("Lỗi", "MSSV đã tồn tại trong hệ thống!")
            return

        pointer = self.pointer_counter
        self.students[pointer] = {"MSSV": mssv, "HoTen": name, "GioiTinh": gender, "isDeleted": False}
        self.pointer_counter += 1

        self.btree.insert((mssv, pointer))

        self.lbl_status.config(text=f"✅ Đã thêm sinh viên: {mssv}")
        self.entry_mssv.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.refresh_ui()

    def delete_student(self):
        if self.is_animating: return
        mssv = self.entry_mssv.get().strip().upper()
        if not mssv: return

        node_idx = self.btree.search(mssv)
        if not node_idx:
            messagebox.showerror("Lỗi", "Không tìm thấy MSSV trong chỉ mục!")
            return

        node, idx = node_idx
        pointer = node.keys[idx][1]

        self.students[pointer]["isDeleted"] = True
        self.btree.delete_key(mssv)

        self.lbl_status.config(text=f"🗑️ Đã xóa sinh viên: {mssv}")
        self.refresh_ui()

    def search_student(self):
        if self.is_animating: return
        mssv = self.entry_mssv.get().strip().upper()
        if not mssv: return

        # Reset UI trước khi tìm
        self.refresh_ui()
        self.lbl_status.config(text=f"⏳ Đang tìm kiếm {mssv}...")
        
        # Lấy kết quả và đường đi
        node, idx, path = self.btree.search_with_path(mssv)
        pointer = node.keys[idx][1] if node else None

        # Bắt đầu chạy Animation
        self.is_animating = True
        self.animate_search(path, node, pointer, 0)

    # ==========================================
    # 4. HOẠT ẢNH (ANIMATION) & RENDER UI
    # ==========================================
    def animate_search(self, path, target_node, pointer, step):
        if step < len(path):
            current_node = path[step]
            node_id = id(current_node)
            
            # Đổi màu node đang duyệt thành Cam (Orange)
            self.canvas.itemconfig(f"rect_{node_id}", fill="#ffe0b2", outline="#fb8c00", width=3)
            self.root.update()
            
            # Đợi 600ms rồi highlight node tiếp theo
            self.root.after(600, self.animate_search, path, target_node, pointer, step + 1)
        else:
            # Khi duyệt xong đường đi
            if target_node:
                # Nếu tìm thấy: Chuyển node đích thành Xanh lá (Green)
                self.canvas.itemconfig(f"rect_{id(target_node)}", fill="#c8e6c9", outline="#4caf50", width=3)
                self.lbl_status.config(text=f"🎯 TÌM THẤY {pointer}!\nHệ thống tốn {len(path)} bước (O(log N))")
                self.update_tables(highlight_pointer=pointer)
            else:
                self.lbl_status.config(text=f"❌ Không tìm thấy mã sinh viên này.")
            
            # Mở khóa các nút bấm
            self.is_animating = False

    def refresh_ui(self, highlight_pointer=None):
        self.update_tables(highlight_pointer)
        self.draw_btree()

    def update_tables(self, highlight_pointer=None):
        for row in self.tree_asc.get_children(): self.tree_asc.delete(row)
        for row in self.tree_sv.get_children(): self.tree_sv.delete(row)

        inorder_keys = self.btree.get_inorder()
        for k in inorder_keys:
            self.tree_asc.insert("", "end", values=(k[0], k[1]))

        for ptr, data in self.students.items():
            status = "Đã xóa" if data["isDeleted"] else "Hoạt động"
            tags = ()
            if data["isDeleted"]:
                tags = ('deleted',)
            elif ptr == highlight_pointer:
                tags = ('highlight',)
            
            self.tree_sv.insert("", "end", values=(ptr, data["MSSV"], data["HoTen"], data["GioiTinh"], status), tags=tags)

    def draw_btree(self):
        self.canvas.delete("all")
        if not self.btree.root.keys:
            return
            
        # Lấy chiều rộng hiện tại của canvas (hoặc giá trị mặc định nếu chưa render xong)
        canvas_width = getattr(self, 'current_canvas_width', self.canvas.winfo_width())
        if canvas_width < 10:
            canvas_width = 800 # Giá trị dự phòng
            
        # Tọa độ X bắt đầu sẽ nằm chính giữa Canvas
        start_x = canvas_width / 2
        
        # Độ giãn ngang (dx) cho các node con sẽ tỷ lệ thuận với chiều rộng màn hình
        # Tránh việc dx quá to hoặc quá nhỏ
        dx = max(100, canvas_width / 4) 
        
        # Bắt đầu vẽ
        self.draw_node(self.btree.root, start_x, 30, dx)

    def draw_node(self, node, x, y, dx):
        keys_str = " | ".join([k[0] for k in node.keys])
        box_width = max(60, len(keys_str) * 10)
        
        # Thêm ID định danh vào thẻ tag của canvas để lát nữa gọi animation
        node_id = id(node)
        self.canvas.create_rectangle(
            x - box_width/2, y, x + box_width/2, y + 30, 
            fill="#e1f5fe", outline="#0288d1", width=2,
            tags=f"rect_{node_id}"
        )
        self.canvas.create_text(x, y + 15, text=keys_str, font=("Arial", 10, "bold"))

        if not node.leaf:
            num_children = len(node.children)
            start_x = x - dx
            step_x = (2 * dx) / (num_children - 1) if num_children > 1 else 0
            
            for i, child in enumerate(node.children):
                child_x = start_x + i * step_x
                child_y = y + 80
                
                # Vẽ đường nối
                self.canvas.create_line(x, y + 30, child_x, child_y, fill="#0288d1", width=1.5)
                # Đệ quy
                self.draw_node(child, child_x, child_y, dx / 1.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()