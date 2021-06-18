

import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import winreg
import shutil
import re
import win32com.client

class MainPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.root.geometry("430x500")
        self.root.title("check_pages")
        self.pack()
        self.ProjectName = tk.StringVar()
        self.folder_path = os.path.join(self.get_desktop_path(), "TempCheck")
        self.createPage()

    def createPage(self):
        ttk.Label(self).grid(row=0, columnspan=2)

        filepath_frame = ttk.LabelFrame(self, text="OUTPUT Folder")
        filepath_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.entry = ttk.Entry(filepath_frame, font=("Arial", 10), textvariable=None, width=38)
        self.entry.grid(row=0, column=0, padx=5, pady=10)
        ttk.Button(filepath_frame, text='...', width=2, command=self.file_path).grid(row=0, column=1, padx=5, pady=10)

        ttk.Button(self, text='Copy', command=self.copy_method).grid(row=4, column=0, stick=tk.W, pady=10)
        ttk.Button(self, text='Check', command=self.check_method).grid(row=4, column=1, stick=tk.E, pady=10)

        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="determinate", maximum=100, length=250, variable=None)
        self.progressbar.grid(row=5, columnspan=2, pady=15, sticky=(tk.E, tk.W))
        self.txt = ttk.Label(self, text='0 %')
        self.txt.grid(row=6, columnspan=2, pady=5, sticky=(tk.E, tk.W))



        self.text = scrolledtext.ScrolledText(self, font="Arial", width=30, height=8, wrap=tk.WORD)
        self.text.grid(row=7, columnspan=2, pady=10)

        ttk.Button(self, text='Clean', command=self.clean_folder).grid(row=8, column=1, stick=tk.E, pady=20)

    def copy_method(self):
        # 在桌面新建一个名为"TempCheck"的文件夹, 再将项目文件夹中的output文件复制过来, 对其进行筛选并重命名为"raw"
        # 最后将其复制到同一文件夹下并命名为"check"
        self.progressbar["value"] = 0
        self.text.delete(1.0, tk.END)
        path = self.folder_path
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass

        output_path = self.entry.get()
        raw_path = os.path.join(path, "Temp")
        if not os.path.exists(raw_path):
            os.mkdir(raw_path)
        else:
            pass
        for root, dirs, files in os.walk(output_path):
            for file in files:
                if re.match(r'^[^merge|~].*?.rtf$', file):
                    shutil.copy(os.path.join(output_path, file), raw_path)
        messagebox.showinfo('tips', 'Copy Successful')

    def file_path(self):
        path_two = filedialog.askdirectory()
        if path_two:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, path_two)

    def get_desktop_path(self):
        # 利用注册表信息查询到系统桌面路径
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    def clean_folder(self):
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)
            messagebox.showinfo('tips', 'Clean Successful')
        else:
            pass

    def check_method(self):
        '''
        open打开rtf文本
        获取rtf码中的原始页码数m
        word打开rtf
        获取分页后的页码数n
        比较m与n是否相等
        如果有差异则将rtf文件名输出到entry
        text.insert("insert", filename)
        '''
        input_dir = self.get_desktop_path() + "\\TempCheck\\Temp"
        rtf_count = 0
        # 计算rtf文件个数, 清理临时文件
        for subdir, dirs, files in os.walk(input_dir):
            for file in files:
                if "~" in file:
                    in_file = os.path.join(subdir, file)
                    os.remove(in_file)
                else:
                    rtf_count += 1
        # print(f"目的文件夹内一共存在 {rtf_count} 个文件：{files}", end="\n\n")
        self.text.delete(1.0, tk.END)
        # 计算rtf码内的NUMPAGE频数
        for subdir, dirs, files in os.walk(input_dir):
            try:
                word = win32com.client.DispatchEx("Word.Application")
                word.Visible = 0
                word.DisplayAlerts = 0

                for i, file in enumerate(files):
                    file_path = os.path.join(subdir, file)
                    if "~?" in file:
                        os.remove(file_path)
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = f.readlines()
                            times = 0
                            for line in data:
                                if "NUMPAGE" in line:
                                    times += 1

                        word.Visible = 0
                        word.DisplayAlerts = 0
                        rtf = word.Documents.Open(file_path)
                        # word.ActiveDocument.Repaginate()
                        pages = word.ActiveDocument.ComputeStatistics(2)
                        # print(f"的实际页码数：{pages}", end=" ")
                        rtf.Close()
                        self.progressbar["value"] = int((i + 1) / len(files) * self.progressbar["maximum"])
                        self.txt['text'] = self.progressbar['value'], '%'
                        self.update_idletasks()
                        if times == pages:
                            print(f"pass {file}")
                        else:
                            self.text.insert(tk.END, file + "\n")
                            self.text.focus_force()
                            self.text.see(tk.END)
                            self.text.update()
                            # print(f"Report的NUMPAGES个数：{times}")
                            # print(f"但{file}的实际页码数：{pages}", end="\n\n")
            finally:
                    word.Quit()
                    del word


if __name__ == '__main__':
    mygui = tk.Tk()
    mygui.resizable(0, 0)
    myroot = MainPage(mygui)
    mygui.iconphoto(False, tk.PhotoImage(file="creeper.png"))
    mygui.mainloop()
    # pyinstaller -w -D -i 48.ico -n inspect_pages inspect_pages.py
