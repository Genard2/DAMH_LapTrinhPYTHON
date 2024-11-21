import tkinter as tk
from tkinter import messagebox

# Hàm xử lý nút bấm
def click_button(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(str(entry.get()))
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Lỗi", "Phép tính không hợp lệ!")
    elif text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Máy tính cơ bản")

# Tạo Entry (ô nhập liệu)
entry = tk.Entry(root, font="Arial 20", borderwidth=5, relief=tk.RIDGE, justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)

# Danh sách các nút bấm
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+"
]

# Tạo các nút bấm
row_val, col_val = 1, 0
for button in buttons:
    btn = tk.Button(root, text=button, font="Arial 18", width=5, height=2)
    btn.grid(row=row_val, column=col_val, padx=5, pady=5)
    btn.bind("<Button-1>", click_button)
    
    col_val += 1
    if col_val > 3:  # Chuyển sang dòng mới sau 4 cột
        col_val = 0
        row_val += 1

# Chạy ứng dụng
root.mainloop()
