# -*- coding: utf-8 -*-
import random
import re
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Đảm bảo load file kv nếu tên class không khớp hoàn toàn với tên file kv
# (Mặc dù SabianOracleApp sẽ tự tìm sabianoracle.kv, nhưng load trực tiếp an toàn hơn)
try:
    Builder.load_file('sabianoracle.kv')
except:
    pass # Nếu file kv đã được load tự động

def get_sabian_symbol(dice1, dice2):
    try:
        # Xác định đường dẫn file txt nằm cùng thư mục với main.py
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "1158872025.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        symbol_key = f"{dice1}-{dice2}"
        
        # --- PHẦN SỬA LỖI REGEX ---
        # Giải thích Regex mới:
        # 1. \\s* -> Tìm phần và khoảng trắng
        # 2. {symbol_key}\:     -> Tìm đúng cặp số (ví dụ: 5-1:)
        # 3. (.*?)              -> Lấy nội dung (nhóm chính)
        # 4. (?=\n\\s*{symbol_key}\:(.*?)(?=\n\
            fallback_pattern = rf"{symbol_key}\:.*?(\n\d+\-\d+\:|\Z)"
            match_old = re.search(fallback_pattern, content, re.DOTALL)
            if match_old:
                return re.sub(r"\n\d+\-\d+\:.*$", "", match_old.group(0), flags=re.DOTALL).strip()
            
            return f"❌ Không tìm thấy thông điệp cho biểu tượng {symbol_key}"

    except FileNotFoundError:
        return "⚠️ Lỗi: Không tìm thấy file '1158872025.txt'. Hãy đảm bảo file này nằm cùng thư mục với main.py."
    except Exception as e:
        return f"⚠️ Lỗi không xác định: {str(e)}"


class SabianLayout(BoxLayout):
    def roll_dice(self):
        # Xúc xắc 1: 12 Cung Hoàng Đạo (hoặc 12 mức năng lượng)
        dice1 = random.randint(1, 12)
        # Xúc xắc 2: 30 Độ của mỗi cung
        dice2 = random.randint(1, 30)
        
        result_text = f"🎲 Kết quả: {dice1}-{dice2}\n"
        result_text += "-" * 30 + "\n"
        result_text += get_sabian_symbol(dice1, dice2)
        
        # Cập nhật giao diện
        self.ids.output_box.text = result_text


class SabianOracleApp(App):
    def build(self):
        self.title = "Sabian Oracle 🎲🔮"
        return SabianLayout()


if __name__ == "__main__":
    SabianOracleApp().run()
