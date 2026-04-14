import customtkinter as ctk
from tkinter import messagebox

# Cài đặt giao diện mặc định
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ==========================================
# PHẦN 1: CẤU TRÚC RADIX TRIE
# ==========================================
class RadixNode:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.is_word = False
        self.meaning = ""
        self.children = {}

class DictionaryApp:
    def __init__(self):
        self.root = RadixNode()

    def insert(self, word, meaning):
        node = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in node.children:
                new_node = RadixNode(word[i:])
                new_node.is_word = True
                new_node.meaning = meaning
                node.children[char] = new_node
                return
            child = node.children[char]
            j = 0
            while j < len(child.prefix) and i + j < len(word) and child.prefix[j] == word[i + j]:
                j += 1
            if j == len(child.prefix):
                node = child
                i += j
            else:
                split_node = RadixNode(child.prefix[j:])
                split_node.is_word = child.is_word
                split_node.meaning = child.meaning
                split_node.children = child.children

                child.prefix = child.prefix[:j]
                child.is_word = False
                child.meaning = ""
                child.children = {split_node.prefix[0]: split_node}

                if i + j < len(word):
                    new_node = RadixNode(word[i+j:])
                    new_node.is_word = True
                    new_node.meaning = meaning
                    child.children[new_node.prefix[0]] = new_node
                else:
                    child.is_word = True
                    child.meaning = meaning
                return
        node.is_word = True
        node.meaning = meaning

    def search(self, word):
        node = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in node.children: return None
            child = node.children[char]
            prefix_len = len(child.prefix)
            if word[i:i+prefix_len] == child.prefix:
                node = child
                i += prefix_len
            else: return None
        return node.meaning if node.is_word else None

    def _merge(self, node):
        if not node.is_word and len(node.children) == 1:
            child = list(node.children.values())[0]
            node.prefix += child.prefix
            node.is_word = child.is_word
            node.meaning = child.meaning
            node.children = child.children

    def delete(self, word):
        if self.search(word) is None:
            return False

        def _delete_recursive(current, word_idx):
            if word_idx == len(word):
                current.is_word = False
                current.meaning = ""
                return len(current.children) == 0

            char = word[word_idx]
            child = current.children[char]
            prefix_len = len(child.prefix)
            
            should_delete_child = _delete_recursive(child, word_idx + prefix_len)
            
            if should_delete_child:
                del current.children[char]
            else:
                self._merge(child)
            
            return not current.is_word and len(current.children) == 0

        _delete_recursive(self.root, 0)
        for key in list(self.root.children.keys()):
            self._merge(self.root.children[key])
        return True

    def get_tree_structure(self, node=None, prefix="", is_last=True, is_root=True, highlight_node=None):
        """Hàm lấy cấu trúc có hỗ trợ Highlight node đang duyệt"""
        if node is None: 
            node = self.root
        
        result = ""
        # Đánh dấu nhánh đang duyệt
        marker = " 👈 [Đang kiểm tra...]" if node is highlight_node else ""

        if is_root:
            result += f"[ROOT]{marker}\n"
            new_prefix = ""
        else:
            branch = "└── " if is_last else "├── "
            status = f" (✅ {node.meaning})" if node.is_word else ""
            result += f"{prefix}{branch}'{node.prefix}'{status}{marker}\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            
        children = list(node.children.values())
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            result += self.get_tree_structure(child, new_prefix, is_last_child, False, highlight_node)
            
        return result

# ==========================================
# PHẦN 2: GIAO DIỆN (SPLIT VIEW)
# ==========================================
class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Từ Điển Thông Minh - Radix Trie")
        self.geometry("1050x650")
        self.app = DictionaryApp()

        self.title_label = ctk.CTkLabel(self, text="TỪ ĐIỂN ANH - VIỆT", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(15, 5))

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # CỘT TRÁI
        self.left_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=400)
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))

        self.input_frame = ctk.CTkFrame(self.left_panel)
        self.input_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.input_frame, text="Từ tiếng Anh:").grid(row=0, column=0, padx=10, pady=(10,5), sticky="w")
        self.word_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Nhập từ...", width=200)
        self.word_entry.grid(row=0, column=1, padx=10, pady=(10,5))

        ctk.CTkLabel(self.input_frame, text="Nghĩa tiếng Việt:").grid(row=1, column=0, padx=10, pady=(5,10), sticky="w")
        self.meaning_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Nhập nghĩa...", width=200)
        self.meaning_entry.grid(row=1, column=1, padx=10, pady=(5,10))

        self.btn_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=10)

        self.btn_add = ctk.CTkButton(self.btn_frame, text="➕ Thêm Từ", command=self.add_word, width=100)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        self.btn_search = ctk.CTkButton(self.btn_frame, text="🔍 Tìm Kiếm", command=self.start_animated_search, width=100)
        self.btn_search.grid(row=0, column=1, padx=5, pady=5)

        self.btn_delete = ctk.CTkButton(self.btn_frame, text="🗑️ Xóa Từ", command=self.delete_word, width=100, fg_color="#C0392B", hover_color="#922B21")
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkLabel(self.left_panel, text="Bảng thông báo (Log hệ thống):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        self.log_box = ctk.CTkTextbox(self.left_panel, height=250, font=ctk.CTkFont(size=13))
        self.log_box.pack(fill="both", expand=True, pady=(5, 0))

        # CỘT PHẢI
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.right_panel, text="CẤU TRÚC BỘ NHỚ (RADIX TRIE)", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.tree_box = ctk.CTkTextbox(self.right_panel, font=ctk.CTkFont(family="Courier", size=14), fg_color="#1E1E1E", text_color="#2ECC71")
        self.tree_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_message("Chào mừng! Hệ thống đã sẵn sàng.\nHãy thử nhập từ và bấm Tìm kiếm để xem thuật toán chạy.")
        self.update_tree_display()

    def log_message(self, message, append=False):
        if not append:
            self.log_box.delete("0.0", "end")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end") # Tự động cuộn xuống dòng mới nhất

    def update_tree_display(self, highlight_node=None):
        tree_data = self.app.get_tree_structure(highlight_node=highlight_node)
        self.tree_box.delete("0.0", "end")
        self.tree_box.insert("0.0", tree_data)

    def get_input_word(self):
        return self.word_entry.get().strip().lower()

    def add_word(self):
        word = self.get_input_word()
        meaning = self.meaning_entry.get().strip()
        if not word or not meaning:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập cả từ và nghĩa!")
            return
        
        self.app.insert(word, meaning)
        self.log_message(f"✅ Đã thêm: {word} -> {meaning}")
        self.word_entry.delete(0, "end")
        self.meaning_entry.delete(0, "end")
        self.update_tree_display()

    def delete_word(self):
        word = self.get_input_word()
        if not word: return
        if self.app.delete(word):
            self.log_message(f"🗑️ Đã xóa sạch '{word}' khỏi bộ nhớ.")
            self.update_tree_display()
        else:
            self.log_message(f"❌ Từ '{word}' không tồn tại để xóa.")
        self.word_entry.delete(0, "end")

    # --- CHUỖI HÀM ANIMATION TÌM KIẾM ---
    def start_animated_search(self):
        word = self.get_input_word()
        if not word: return
        
        # Khóa nút bấm trong lúc duyệt cây để tránh click chồng chéo
        self.btn_search.configure(state="disabled")
        self.btn_add.configure(state="disabled")
        self.btn_delete.configure(state="disabled")
        
        self.log_message(f"🔍 BẮT ĐẦU TÌM KIẾM TỪ: '{word}'...")
        self.log_message("⏳ Bước 1: Khởi hành từ [ROOT]", append=True)
        
        # Bắt đầu vòng lặp animation từ node root
        self.update_tree_display(highlight_node=self.app.root)
        self.after(1000, lambda: self._search_step(self.app.root, word, 0))

    def _search_step(self, current_node, word, i):
        # Nếu đã duyệt hết các ký tự của từ cần tìm
        if i == len(word):
            if current_node.is_word:
                self.log_message(f"🎉 THÀNH CÔNG! Đã khớp toàn bộ.\nNghĩa là: {current_node.meaning}", append=True)
            else:
                self.log_message(f"⚠️ Dừng lại tại '{current_node.prefix}', nhưng đây chỉ là nút trung gian, không phải từ hoàn chỉnh.", append=True)
            self._end_animated_search()
            return
            
        char = word[i]
        self.log_message(f"▶️ Tìm nhánh chứa ký tự tiếp theo '{char}'...", append=True)
        
        # Bước kiểm tra nhánh
        if char not in current_node.children:
            self.log_message(f"❌ Nhánh bị đứt! Không có đường đi nào chứa '{char}'. Tìm kiếm thất bại.", append=True)
            self._end_animated_search()
            return
            
        child = current_node.children[char]
        prefix_len = len(child.prefix)
        
        # Delay rồi mới hiển thị node tiếp theo
        self.after(800, lambda: self._check_prefix_match(child, word, i, prefix_len))

    def _check_prefix_match(self, child_node, word, i, prefix_len):
        self.update_tree_display(highlight_node=child_node)
        
        if word[i:i+prefix_len] == child_node.prefix:
            self.log_message(f"✔️ Khớp tiền tố '{child_node.prefix}'. Trượt xuống nhánh này...", append=True)
            # Delay rồi đệ quy bước tiếp theo
            self.after(1000, lambda: self._search_step(child_node, word, i + prefix_len))
        else:
            self.log_message(f"❌ Xung đột tiền tố! Cần '{word[i:i+prefix_len]}' nhưng nhánh lại là '{child_node.prefix}'. Thất bại.", append=True)
            self._end_animated_search()

    def _end_animated_search(self):
        # Mở khóa các nút
        self.btn_search.configure(state="normal")
        self.btn_add.configure(state="normal")
        self.btn_delete.configure(state="normal")
        # Xóa highlight trên cây
        self.after(1500, self.update_tree_display)

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
