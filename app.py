from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from DigitalSignatures import RSASign, RSAVerify, RSA
from ReadFileDocx import read_docx
from random import randint
import os

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.title("Digital Signature")
        self.geometry("900x450")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.CreateNavigationBar()
        self.SignatureFrame()
        self.VerifyFrame()
        self.GetKeyPairFrame()
        self.SignFrameBtnEvent()

    def CreateNavigationBar(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=20)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Digital Signature",
                                            compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.sign_frame_button = ctk.CTkButton(self.navigation_frame, corner_radius=20, height=40, border_spacing=10, text="Signature",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.SignFrameBtnEvent)
        self.sign_frame_button.grid(row=1, column=0, sticky="ew")

        self.veri_frame_button = ctk.CTkButton(self.navigation_frame, corner_radius=20, height=40, border_spacing=10, text="Verify",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.VeriFrameBtnEvent)
        self.veri_frame_button.grid(row=2, column=0, sticky="ew")

        self.getK_frame_button = ctk.CTkButton(self.navigation_frame, corner_radius=20, height=40, border_spacing=10, text="Get key pair",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.GetFrameKBtnEvent)
        self.getK_frame_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        self.appearance_mode_menu.set("System")

    def SignatureFrame(self):
        self.sign_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.sign_frame.grid_columnconfigure(0, weight=1)

        self.sign_div1 = ctk.CTkFrame(self.sign_frame, fg_color="transparent")
        self.sign_div1.grid(row=0, column=0, pady=10)
        # Tạo Label
        self.sign_label1 = ctk.CTkLabel(self.sign_div1, text="Chọn file cần ký")
        self.sign_label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Tạo Entry để hiển thị đường dẫn file
        self.sign_entry1 = ctk.CTkEntry(self.sign_div1, width=300)
        self.sign_entry1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # Tạo Button để chọn file
        self.sign_select_file1 = ctk.CTkButton(self.sign_div1, text="Chọn file", command=lambda: self.select_file(self.sign_entry1))
        self.sign_select_file1.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.sign_div2 = ctk.CTkFrame(self.sign_frame, fg_color="transparent")
        self.sign_div2.grid(row=1, column=0, pady=10)
        # Tạo Label
        self.sign_label2 = ctk.CTkLabel(self.sign_div2, text="Chọn file private key")
        self.sign_label2.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Tạo Entry để hiển thị đường dẫn file
        self.sign_entry2 = ctk.CTkEntry(self.sign_div2, width=300)
        self.sign_entry2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # Tạo Button để chọn file
        self.sign_select_file2 = ctk.CTkButton(self.sign_div2, text="Chọn file", command=lambda: self.select_file(self.sign_entry2))
        self.sign_select_file2.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.sign_btn = ctk.CTkButton(self.sign_frame, text="Kí", width=100, command=self.SignBtnEvent)
        self.sign_btn.grid(row=2, column=0, pady=10)

    def VerifyFrame(self):
        self.veri_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.veri_frame.grid_columnconfigure(0, weight=1)

        self.veri_div1 = ctk.CTkFrame(self.veri_frame, fg_color="transparent")
        self.veri_div1.grid(row=0, column=0, pady=10)
        # Tạo Label
        self.veri_label1 = ctk.CTkLabel(self.veri_div1, text="Chọn file cần kiểm tra")
        self.veri_label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Tạo Entry để hiển thị đường dẫn file
        self.veri_entry1 = ctk.CTkEntry(self.veri_div1, width=300)
        self.veri_entry1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # Tạo Button để chọn file
        self.veri_select_file1 = ctk.CTkButton(self.veri_div1, text="Chọn file", command=lambda: self.select_file(self.veri_entry1))
        self.veri_select_file1.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.veri_div2 = ctk.CTkFrame(self.veri_frame, fg_color="transparent")
        self.veri_div2.grid(row=1, column=0, pady=10)
        # Tạo Label
        self.veri_label2 = ctk.CTkLabel(self.veri_div2, text="Chọn file public key")
        self.veri_label2.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Tạo Entry để hiển thị đường dẫn file
        self.veri_entry2 = ctk.CTkEntry(self.veri_div2, width=300)
        self.veri_entry2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # Tạo Button để chọn file
        self.veri_select_file2 = ctk.CTkButton(self.veri_div2, text="Chọn file", command=lambda: self.select_file(self.veri_entry2))
        self.veri_select_file2.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.veri_div3 = ctk.CTkFrame(self.veri_frame, fg_color="transparent")
        self.veri_div3.grid(row=2, column=0, pady=10)
        # Tạo Label
        self.veri_label3 = ctk.CTkLabel(self.veri_div3, text="Chọn file chữ kí")
        self.veri_label3.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Tạo Entry để hiển thị đường dẫn file
        self.veri_entry3 = ctk.CTkEntry(self.veri_div3, width=300)
        self.veri_entry3.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # Tạo Button để chọn file
        self.veri_select_file3 = ctk.CTkButton(self.veri_div3, text="Chọn file", command=lambda: self.select_file(self.veri_entry3))
        self.veri_select_file3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")


        self.veri_btn = ctk.CTkButton(self.veri_frame, text="Kiểm tra", width=100, command=self.VeriBtnEvent)
        self.veri_btn.grid(row=3, column=0, pady=10)

    def GetKeyPairFrame(self):
        self.getK_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.getK_btn = ctk.CTkButton(self.getK_frame, text="Get key", command=self.GetKBtnEvent)
        self.getK_btn.pack(expand=True)

    def select_file(self, entry: ctk.CTkEntry):
        file_path = tk.filedialog.askopenfilename(title="Chọn file", filetypes=[("All files", "*.*")])
        if file_path:
            entry.delete(0, ctk.END)
            entry.insert(0, file_path)
    
    def SignBtnEvent(self):
        root_url = self.sign_entry1.get()
        private_url = self.sign_entry2.get()
        try:
            if root_url.endswith(".docx"):
                data = read_docx(root_url)
            else:
                with open(root_url, encoding="utf-8") as f:
                    data = f.read()
            with open(private_url, "rb") as f:
                private_key = RSA.import_key(f.read())

            signature = RSASign(data, private_key)
            sign_file_name = os.path.basename(root_url) + "_sig.bin"
            with open(sign_file_name, "wb") as f:
                f.write(signature)
            messagebox.showinfo("Thành công", "Kí thành công")
        except TypeError:
            messagebox.showerror("Lỗi", f"Key được chọn phải là private key")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file")

    def VeriBtnEvent(self):
        check_url = self.veri_entry1.get()
        public_url = self.veri_entry2.get()
        sign_url = self.veri_entry3.get()
        try:
            if check_url.endswith(".docx"):
                data = read_docx(check_url)
            else:
                with open(check_url, encoding="utf-8") as f:
                    data = f.read()
            with open(public_url, "rb") as f:
                public_key = RSA.import_key(f.read())
            with open(sign_url, "rb") as f:
                signature = f.read()
            if public_key.has_private():
                messagebox.showerror("Lỗi", "Key được chọn phải là public key")
                return
            
            check = RSAVerify(data, signature, public_key)
            if check:
                messagebox.showinfo("Thành công", "Chữ ký hợp lệ\nVăn bản chính xác")
            else:
                messagebox.showerror("Thất bại", "Chữ ký không hợp lệ\nVăn bản đã bị chỉnh sửa")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không thể đọc file")

    def GetKBtnEvent(self):
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        index = randint(1000, 9999)
        with open(f"private_key{index}.pem", "wb") as f:
            f.write(private_key.export_key())
        with open(f"public_key{index}.pem", "wb") as f:
            f.write(public_key.export_key())
        messagebox.showinfo("Thành công", "Tạo khóa thành công")


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.sign_frame_button.configure(fg_color=("gray75", "gray25") if name == "Signature" else "transparent")
        self.veri_frame_button.configure(fg_color=("gray75", "gray25") if name == "Verify" else "transparent")
        self.getK_frame_button.configure(fg_color=("gray75", "gray25") if name == "Get key pair" else "transparent")
        # show selected frame
        if name == "Signature":
            self.sign_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sign_frame.grid_forget()
        if name == "Verify":
            self.veri_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.veri_frame.grid_forget()
        if name == "Get key pair":
            self.getK_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.getK_frame.grid_forget()

    def SignFrameBtnEvent(self):
        self.select_frame_by_name("Signature")

    def VeriFrameBtnEvent(self):
        self.select_frame_by_name("Verify")

    def GetFrameKBtnEvent(self):
        self.select_frame_by_name("Get key pair")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)