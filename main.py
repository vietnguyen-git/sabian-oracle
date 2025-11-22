# -*- coding: utf-8 -*-
import random
import re
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


def get_sabian_symbol(dice1, dice2):
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "1158872025.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        symbol_key = f"{dice1}-{dice2}"
        pattern = rf"{symbol_key}\:.*?(\n\d+\-\d+\:|\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            symbol_text = match.group(0)
            symbol_text = re.sub(r"\n\d+\-\d+\:.*$", "", symbol_text, flags=re.DOTALL)
            return symbol_text.strip()
        else:
            return f"❌ Không tìm thấy Sabian Symbol cho {symbol_key}"
    except FileNotFoundError:
        return "⚠️ Lỗi: Không tìm thấy file '1158872025.txt'."
    except UnicodeDecodeError:
        return "⚠️ Lỗi: Không thể đọc file, hãy lưu file ở dạng UTF-8."
    except Exception as e:
        return f"⚠️ Lỗi: {str(e)}"


class SabianLayout(BoxLayout):
    def roll_dice(self):
        dice1 = random.randint(1, 12)
        dice2 = random.randint(1, 30)
        result_text = f"🎲 Kết quả xúc xắc: {dice1}-{dice2}\n\n🔮 Dự đoán Sabian:\n\n"
        result_text += get_sabian_symbol(dice1, dice2)
        self.ids.output_box.text = result_text


class SabianOracleApp(App):
    def build(self):
        self.title = "Sabian Oracle 🎲🔮"
        return SabianLayout()


if __name__ == "__main__":
    SabianOracleApp().run()
