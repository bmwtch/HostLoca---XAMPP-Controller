# gui/app_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from modules import mysql, user_manager, apache
import webbrowser

class ControlPanelApp:
    def __init__(self, root, settings, save_settings):
        self.root = root
        self.settings = settings
        self.save_settings = save_settings

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        self.build_xampp_connector()
        self.build_htdocs_settings()
        self.build_db_control_board()
        self.build_user_management()

        self.build_footer_bar()

    def build_xampp_connector(self):
        section = tk.LabelFrame(self.frame, text="XAMPP Connector", padx=10, pady=10)
        section.pack(fill="x", pady=5)

        self.xampp_label = tk.Label(section, text=f"Selected: {self.settings.get('xampp_path', '')}")
        self.xampp_label.pack(anchor="w")

        tk.Button(section, text="Select XAMPP Folder", command=self.select_xampp_folder).pack(pady=5)

    def select_xampp_folder(self):
        folder = filedialog.askdirectory(title="Select XAMPP Installation Folder")
        if folder:
            self.settings["xampp_path"] = folder
            self.save_settings(self.settings)
            self.xampp_label.config(text=f"Selected: {folder}")
            messagebox.showinfo("XAMPP Connector", f"XAMPP folder set to {folder}")

    def build_htdocs_settings(self):
        section = tk.LabelFrame(self.frame, text="HTDOC Settings", padx=10, pady=10)
        section.pack(fill="x", pady=5)

        section.grid_columnconfigure(0, weight=1)
        section.grid_columnconfigure(1, weight=1)

        self.htdocs_label = tk.Label(section, text=f"Current HTDOC: {self.settings.get('htdocs_path', '')}")
        self.htdocs_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        tk.Button(section, text="Select Custom HTDOC Folder", command=self.select_htdocs_folder).grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )

    def select_htdocs_folder(self):
        folder = filedialog.askdirectory(title="Select HTDOC Folder")
        if folder:
            try:
                apache.set_htdocs(folder)
                self.settings["htdocs_path"] = folder
                self.save_settings(self.settings)
                self.htdocs_label.config(text=f"Current HTDOC: {folder}")
                messagebox.showinfo("HTDOC Settings", f"HTDOC folder set to {folder}")
            except Exception as e:
                messagebox.showerror("HTDOC Settings", f"Error: {e}")

    def build_db_control_board(self):
        section = tk.LabelFrame(
            self.frame,
            text="Database Control Board || Default DB User : `root`, DB Password: `` ",
            padx=10, pady=10
        )
        section.pack(fill="x", pady=5)

        for i in range(3):
            section.grid_columnconfigure(i, weight=1)

        self.sql_label = tk.Label(section, text=f"SQL Folder: {self.settings.get('sql_folder', '')}")
        self.sql_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        tk.Button(section, text="Select SQL Folder", command=self.select_sql_folder).grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )

        tk.Button(section, text="Load SQL Databases", command=self.load_sql_databases).grid(
            row=0, column=2, sticky="ew", padx=5, pady=5
        )

    def select_sql_folder(self):
        folder = filedialog.askdirectory(title="Select SQL Folder")
        if folder:
            self.settings["sql_folder"] = folder
            self.save_settings(self.settings)
            self.sql_label.config(text=f"SQL Folder: {folder}")

    def load_sql_databases(self):
        try:
            mysql.import_sql_folder(
                self.settings.get("sql_folder", ""),
                self.settings.get("db_user", "root"),
                self.settings.get("db_pass", "")
            )
            messagebox.showinfo("Database Control Board", "SQL databases loaded successfully!")
        except Exception as e:
            messagebox.showerror("Database Control Board", f"Error: {e}")

    def build_user_management(self):
        section = tk.LabelFrame(self.frame, text="User Management (Secure Setup)", padx=10, pady=10)
        section.pack(fill="x", pady=5)

        for i in range(5):
            section.grid_columnconfigure(i, weight=1)

        tk.Label(section, text="Username").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.user_entry = tk.Entry(section)
        self.user_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(section, text="Password").grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.pass_entry = tk.Entry(section, show="*")
        self.pass_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        tk.Button(section, text="Submit", command=self.setup_user).grid(
            row=0, column=4, sticky="ew", padx=5, pady=5
        )

    def setup_user(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("User Management", "Username and password cannot be empty.")
            return

        try:
            user_manager.setup_secure_user(username, password, root_pass=self.settings.get("db_pass", ""))
            self.settings["db_user"] = username
            self.settings["db_pass"] = password
            self.save_settings(self.settings)
            messagebox.showinfo("User Management", f"Secure user {username} set up successfully!")
        except Exception as e:
            messagebox.showerror("User Management", f"Error: {e}")

    def build_footer_bar(self):
        footer = tk.Frame(self.root, bg="#f0f0f0")
        footer.pack(side="bottom", fill="x")

        def open_donate():
            webbrowser.open("https://bmwtech.in/donateme.php")

        donate_btn = tk.Button(
            footer,
            text="Donate Me",
            command=open_donate,
            bg="orange",
            font=("Segoe UI", 12, "bold"),
            width=20,
            height=1
        )
        donate_btn.pack(side="top", pady=5)

        note_text = (
            "This is an open source project created to help.\n"
            "If you find it useful and wish to support, kindly consider donating."
        )
        note = tk.Label(
            self.root,
            text=note_text,
            justify="left",
            wraplength=980,
            fg="green",
            font=("Segoe UI", 10, "bold")
        )
        note.pack(side="bottom", pady=20)
