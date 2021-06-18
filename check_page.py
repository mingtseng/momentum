

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
        self.root.geometry("430x560")
        self.root.title("check_pages")
        self.pack()
        self.ProjectName = tk.StringVar()
        self.study_list = os.listdir("Z:\studies")
        self.role_list = ["SCP", "QCP"]
        self.role = tk.StringVar()
        self.folder_path = os.path.join(self.get_desktop_path(), "TempCheck")
        self.createPage()
        self.ProjectName.trace("w", self.default_output_path)
        self.role.trace("w", self.default_output_path)
        self.default_output_path()

    def createPage(self):
        ttk.Label(self).grid(row=0, columnspan=2)

        frame = ttk.LabelFrame(self, text="Study and Role")
        frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(frame, text="Study", width=5).grid(row=1, column=0, pady=10, padx=10)
        self.combobox_study = ttk.Combobox(frame, textvariable=self.ProjectName, font=("Arial", 10),
                                           value=self.study_list, width=12)
        self.combobox_study.grid(row=1, column=1, stick=tk.W, padx=10, pady=10)
        self.combobox_study.current(0)

        ttk.Label(frame, text="Role").grid(row=1, column=2, padx=10, pady=10)
        self.combobox = ttk.Combobox(frame, textvariable=self.role, font=("Arial", 10), value=self.role_list, width=6)
        self.combobox.grid(row=1, column=3, padx=10, pady=10)
        self.combobox.current(0)

        filepath_frame = ttk.LabelFrame(self, text="OUTPUT Folder")
        filepath_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.entry = ttk.Entry(filepath_frame, font=("Arial", 10), textvariable=None, width=38)
        self.entry.grid(row=0, column=0, padx=5, pady=10)
        ttk.Button(filepath_frame, text='...', width=2, command=self.file_path).grid(row=0, column=1, padx=5, pady=10)

        ttk.Button(self, text='Copy', command=self.copy_method).grid(row=4, column=0, stick=tk.W, pady=10)
        ttk.Button(self, text='Check', command=self.check_method).grid(row=4, column=1, stick=tk.E, pady=10)

        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="determinate", maximum=100,
                                           length=250, variable=None)
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
                if re.match(r'^[a-z]+-[l|t|f]-[a-z0-9-]+.rtf$', file):
                    shutil.copy(os.path.join(output_path, file), raw_path)
        messagebox.showinfo('tips', 'Copy Successful')

    def default_output_path(self, *args):
        if self.role.get() == "QCP":
            self.output_path = os.path.join(r"Z:\studies", self.ProjectName.get(), r"STAT\testdir\qc\output")
        else:
            self.output_path = os.path.join(r"Z:\studies", self.ProjectName.get(), r"STAT\testdir\output")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.output_path)

    def file_path(self):
        path_two = filedialog.askdirectory()
        if path_two:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, path_two)

    def get_desktop_path(self):
        # 利用注册表信息查询到系统桌面路径
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    def clean_folder(self):
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)
            messagebox.showinfo('tips', 'Clean Successful')
        else:
            pass

    def kill_exe(self, exe_name):
        cmd = 'taskkill /F /IM ' + exe_name
        os.system(cmd)

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
                self.kill_exe("WINWORD.EXE")
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
                        pages = word.ActiveDocument.ComputeStatistics(2)
                        if times == pages:
                            print(f"pass {file}")
                        else:
                            appointed = []
                            for each_table in word.ActiveDocument.Tables:
                                # 指定范围的单元格数量
                                cellCount = each_table.Range.Cells.Count
                                # 表格中第一个单元格所属页码数
                                firstCharPage = each_table.Range.Cells(1).Range.Characters.First.Information(3)
                                # 表格中最后一个单元格所属页码数
                                lastCharPage = each_table.Range.Cells(cellCount).Range.Characters.First.Information(3)
                                if firstCharPage != lastCharPage:
                                    appointed.append(firstCharPage)
                                    break
                            if appointed == []:
                                appointed.append("only due to footnotes")
                            self.text.insert(tk.END, file + " " + str(appointed) + "\n")
                            self.text.focus_force()
                            self.text.see(tk.END)
                            self.text.update()
                        word.DisplayAlerts = 0
                        rtf.Close()
                        self.progressbar["value"] = int((i + 1) / len(files) * self.progressbar["maximum"])
                        self.txt['text'] = self.progressbar['value'], '%'
                        self.update_idletasks()
            finally:
                    word.Quit()
                    del word


if __name__ == '__main__':
    mygui = tk.Tk()
    mygui.resizable(0, 0)
    myroot = MainPage(mygui)
    mygui.mainloop()
    # pyinstaller -w -F -i xml.ico -n Checka_page check_page.py
