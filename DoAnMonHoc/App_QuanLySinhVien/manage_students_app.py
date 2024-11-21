import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import psycopg2

# Kết nối cơ sở dữ liệu PostgreSQL
conn = None

class Tab1:
    def __init__(self, tab_control):
        self.default_color = "#f5f5f5"  
        self.highlight_color = "#007acc"  
        self.button_color = "#4CAF50"  
        self.text_color = "#333333"  

        self.tab = tk.Frame(tab_control, bg=self.default_color)
        tab_control.add(self.tab, text="Connect SQL")

        # Frame for content
        self.content_frame = tk.Frame(self.tab, padx=20, pady=20, bg=self.default_color)
        self.content_frame.pack(expand=True, anchor='center')

        # Logo setup
        self.setup_logo()

        # Welcome message and fields for SQL connection info
        self.welcome_label = tk.Label(self.content_frame, text="Enter SQL Connection Info", 
                                      font=("Helvetica", 18, "bold"), fg=self.highlight_color, bg=self.default_color)
        self.welcome_label.pack(pady=10)

        # Khung cho các trường nhập
        self.entry_frame = tk.Frame(self.content_frame, bg=self.default_color, padx=10, pady=10)
        self.entry_frame.pack(pady=10, fill="x")

        # Các trường nhập cho thông tin kết nối SQL
        self.create_sql_fields()

        # Connect button
        self.connect_button = tk.Button(self.content_frame, text="Connect", font=("Helvetica", 12, "bold"),
                                        bg=self.button_color, fg="white", width=20, relief="flat", command=self.connect_to_db)
        self.connect_button.pack(pady=20)

    def create_sql_fields(self):
        field_style = {"font": ("Arial", 12), "bg": self.default_color, "fg": self.text_color}

        # Host
        tk.Label(self.entry_frame, text="Host:", **field_style).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.host_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=30, relief="groove")
        self.host_entry.grid(row=0, column=1, pady=5, sticky="w")
        self.host_entry.insert(0, "localhost")  # Default value

        # Database
        tk.Label(self.entry_frame, text="Database:", **field_style).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.db_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=30, relief="groove")
        self.db_entry.grid(row=1, column=1, pady=5, sticky="w")
        self.db_entry.insert(0, "postgres")  # Default value

        # User
        tk.Label(self.entry_frame, text="User:", **field_style).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.user_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=30, relief="groove")
        self.user_entry.grid(row=2, column=1, pady=5, sticky="w")
        self.user_entry.insert(0, "postgres")  # Default value

        # Password
        tk.Label(self.entry_frame, text="Password:", **field_style).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(self.entry_frame, font=("Arial", 12), show="*", width=30, relief="groove")
        self.password_entry.grid(row=3, column=1, pady=5, sticky="w")

    def setup_logo(self):
        logo_path = r'D:\LTPTNC\KTGK\Images\logo1.png'
        try:
            img = Image.open(logo_path)
            logo = ImageTk.PhotoImage(img)
            logo_label = tk.Label(self.content_frame, image=logo, bg=self.default_color)
            logo_label.image = logo  # Keep reference
            logo_label.pack(pady=10)
        except Exception as e:
            print("Error loading logo:", e)
            tk.Label(self.content_frame, text="Logo not found", bg=self.default_color).pack(pady=10)

    def connect_to_db(self):
        global conn
        if conn:
            messagebox.showinfo("Connection Status", "Already connected to the database.")
            return
        try:
            # Get the values from the input fields
            host = self.host_entry.get()
            database = self.db_entry.get()
            user = self.user_entry.get()
            password = self.password_entry.get()

            # Thực hiện kết nối với cơ sở dữ liệu
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            messagebox.showinfo("Connection Status", "Successfully connected to the database.")
            self.content_frame.config(bg="#dff0d8")  # Change color to greenish on successful connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to the database: {e}")


class Tab2:
    def __init__(self, tab_control):
        self.default_color = "#f5f5f5"  # Màu nền sáng
        self.highlight_color = "#007acc"  # Màu nhấn
        self.button_color = "#4CAF50"  # Màu nút bấm
        self.text_color = "#333333"  # Màu chữ tối

        self.tab = tk.Frame(tab_control, bg=self.default_color)
        tab_control.add(self.tab, text="Student Management")

        # Frame for form input
        self.form_frame = tk.Frame(self.tab, padx=20, pady=20, bg=self.default_color)
        self.form_frame.pack()
        # Tiêu đề cho Tab2
        self.title_label = tk.Label(self.form_frame, text="Student Management", font=("Helvetica", 18, "bold"), fg=self.highlight_color, bg=self.default_color)
        self.title_label.grid(row=0, columnspan=2, pady=10)
        tk.Label(self.form_frame, text="Tên:", bg=self.default_color, font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_name = tk.Entry(self.form_frame, font=("Arial", 12), width=40, relief="groove")
        self.entry_name.grid(row=1, column=1, pady=5)

        tk.Label(self.form_frame, text="Tuổi:", bg=self.default_color, font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_age = tk.Entry(self.form_frame, font=("Arial", 12), width=40, relief="groove")
        self.entry_age.grid(row=2, column=1, pady=5)

        tk.Label(self.form_frame, text="Giới tính:", bg=self.default_color, font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_gender = tk.Entry(self.form_frame, font=("Arial", 12), width=40, relief="groove")
        self.entry_gender.grid(row=3, column=1, pady=5)

        tk.Label(self.form_frame, text="Ngành học:", bg=self.default_color, font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.entry_major = tk.Entry(self.form_frame, font=("Arial", 12), width=40, relief="groove")
        self.entry_major.grid(row=4, column=1, pady=5)

        # Frame for buttons
        self.button_frame = tk.Frame(self.tab, padx=20, pady=20, bg=self.default_color)
        self.button_frame.pack()

        button_style = {"font": ("Arial", 12, "bold"), "bg": self.button_color, "fg": "white", "width": 15, "padx": 10, "pady": 10}

        # Buttons with new style and spacing
        tk.Button(self.button_frame, text="Thêm sinh viên", **button_style, command=self.add_student).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.button_frame, text="Cập nhật thông tin", **button_style, command=self.update_student).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.button_frame, text="Xóa sinh viên", **button_style, command=self.delete_student).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.button_frame, text="Tải lại danh sách", **button_style, command=self.load_students).grid(row=0, column=3, padx=5, pady=5)

        # Treeview for displaying student list with improved style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background=self.button_color, foreground="blue")
        style.configure("Treeview", font=("Arial", 11), rowheight=20, background="#f9f9f9", fieldbackground="#f9f9f9")
        style.map('Treeview', background=[('selected', '#007acc')])

        # Add Scrollbar
        self.tree_frame = tk.Frame(self.tab)
        self.tree_frame.pack(pady=20, fill='both', expand=True)

        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Tên", "Tuổi", "Giới tính", "Ngành"), show='headings', height=10, yscrollcommand=self.tree_scroll.set)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Tuổi", text="Tuổi")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.heading("Ngành", text="Ngành")

        # Cân chỉnh lại chiều rộng cột và căn giữa
        self.tree.column("ID", width=20, anchor="center")
        self.tree.column("Tên", width=100, anchor="center")
        self.tree.column("Tuổi", width=30, anchor="center")
        self.tree.column("Giới tính", width=50, anchor="center")
        self.tree.column("Ngành", width=50, anchor="center")

        

        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.config(command=self.tree.yview)

        # Load initial data
        self.load_students()

    def load_students(self):
        global conn
        if not conn:
            messagebox.showwarning("Database Connection", "Vui lòng kết nối cơ sở dữ liệu!")
            return
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        # Clear current data in Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data
        for row in rows:
            self.tree.insert('', 'end', values=row)

        # Thông báo tải lại danh sách thành công
        messagebox.showinfo("Reload", "Tải lại danh sách thành công!")

    def add_student(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        major = self.entry_major.get()

        if name and age and gender and major:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)", (name, age, gender, major))
            conn.commit()
            self.load_students()

            # Thông báo thêm thành công
            messagebox.showinfo("Add Student", "Thêm sinh viên thành công!")
        else:
            messagebox.showwarning("Input Error", "Vui lòng điền đầy đủ thông tin!")

    def update_student(self):
        selected = self.tree.focus()
        if selected:
            student_id = self.tree.item(selected)['values'][0]
            name = self.entry_name.get()
            age = self.entry_age.get()
            gender = self.entry_gender.get()
            major = self.entry_major.get()

            if name and age and gender and major:
                cursor = conn.cursor()
                cursor.execute("UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s",
                               (name, age, gender, major, student_id))
                conn.commit()
                self.load_students()

                # Thông báo cập nhật thành công
                messagebox.showinfo("Update Student", "Cập nhật thông tin thành công!")
            else:
                messagebox.showwarning("Input Error", "Vui lòng điền đầy đủ thông tin!")
        else:
            messagebox.showwarning("Selection Error", "Vui lòng chọn sinh viên để cập nhật!")

    def delete_student(self):
        selected = self.tree.focus()
        if selected:
            student_id = self.tree.item(selected)['values'][0]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
            conn.commit()
            self.load_students()

            # Thông báo xóa thành công
            messagebox.showinfo("Delete Student", "Xóa sinh viên thành công!")
        else:
            messagebox.showwarning("Selection Error", "Vui lòng chọn sinh viên để xóa!")


def main():
    root = tk.Tk()
    root.title("Student Management App")
    root.geometry("900x700")

    # Tạo thanh menu
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Student Management App v1.0"))
    menubar.add_cascade(label="Help", menu=about_menu)
    root.config(menu=menubar)

    tab_control = ttk.Notebook(root)

    # Tạo tab mới với giao diện nhập kết nối SQL
    tab1 = Tab1(tab_control)

    # Tạo tab quản lý sinh viên
    tab2 = Tab2(tab_control)

    tab_control.pack(expand=True, fill='both')

    root.mainloop()

if __name__ == "__main__":
    main()
