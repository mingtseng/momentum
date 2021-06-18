
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from lxml import html
import time
import json

class MainPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.root.geometry("400x440")
        self.pack()

        self.study_name = self.get_name()
        self.ProjectName = tk.StringVar()

        self.FolderName = tk.StringVar()

        self.path1 = tk.StringVar()
        self.path2 = tk.StringVar()
        self.createPage()
        self.default()


    def createPage(self):
        ttk.Label(self).grid(row=0, column=0)
        self.frame_pro = ttk.LabelFrame(self, text="Project Name")
        self.frame_pro.grid(row=1, column=0, sticky=tk.W, pady=15)
        self.combobox = ttk.Combobox(self.frame_pro, textvariable=self.ProjectName, value=tuple(self.study_name), width=8)
        self.combobox.grid(pady=10)
        self.combobox.bind("<<ComboboxSelected>>", self.default)
        self.combobox.current(0)
        self.frame_fold = ttk.LabelFrame(self, text="Folder Name")
        self.frame_fold.grid(row=1, column=1, sticky=tk.E, pady=15)
        self.folder_names = self.get_folder_name()
        self.combobox2 = ttk.Combobox(self.frame_fold, textvariable=self.FolderName, value=tuple(self.folder_names), width=8)
        self.combobox2.grid(pady=10)
        self.combobox2.bind("<<ComboboxSelected>>", self.default_s)
        self.combobox2.current(0)

        # adam相关组块
        filepath_frame_adam = ttk.LabelFrame(self, text="Destination Folder(ADaM)")
        filepath_frame_adam.grid(row=3, column=0, columnspan=2)
        self.entry1 = ttk.Entry(filepath_frame_adam, textvariable=self.path1, width=40)
        self.entry1.grid(row=0, column=0, padx=5, pady=10)
        ttk.Button(filepath_frame_adam, text='...', width=2, command=self.filepath1).grid(row=0, column=1, padx=5, pady=10)

        ttk.Button(self, text='ADaM', command=self.get_adam).grid(row=4, column=0, stick=tk.W, pady=30)
        ttk.Button(self, text='bat[compare]', command=self.get_adam_bat).grid(row=4, column=1, stick=tk.E, pady=30)

        # tfls相关组块
        filepath_frame_tfl = ttk.LabelFrame(self, text="Destination Folder(tfls)")
        filepath_frame_tfl.grid(row=5, column=0, columnspan=2)
        self.entry2 = ttk.Entry(filepath_frame_tfl, textvariable=self.path2, width=40)
        self.entry2.grid(row=0, column=0, padx=5, pady=10)
        ttk.Button(filepath_frame_tfl, text='...', width=2, command=self.filepath2).grid(row=0, column=1, padx=5, pady=10)

        ttk.Button(self, text='TFLs', command=self.get_tfl).grid(row=6, column=0, stick=tk.W, pady=30)
        ttk.Button(self, text='bat[compare]', command=self.get_tfl_bat).grid(row=6, column=1, stick=tk.E, pady=30)

    def get_folder_name(self):
        url_folder = "http://10.20.2.73:8082/system/project/ajax_list"
        response_folder = self.re_session.get(url_folder, headers=dict(referer=url_folder)).text
        self.items_folder = json.loads(response_folder)['data']
        analysis_types = []
        for item in self.items_folder:
            if item['parent_id'] != 0:
                if item['study_name'] == self.ProjectName.get():
                    analysis_types.append(item['analysis_type'])
        return analysis_types

    def get_parent_path(self):
        path = ""
        for item in self.items_folder:
            if item['parent_id'] != 0:
                if item['study_name'] == self.ProjectName.get() and item['analysis_type'] == self.FolderName.get():
                    path = item['parent_path']
        return path

    # 从Tracker中获取tfls相关信息
    def get_data(self, key):
        url_goal3 = "http://10.20.2.73:8082/system/tfls/ajax_list?study_number=" + self.ProjectName.get() + "-" + self.FolderName.get() + "&page=1&limit=100"
        url_goal4 = "http://10.20.2.73:8082/system/tfls/ajax_list?study_number=" + self.ProjectName.get() + "-" + self.FolderName.get() + "&page=2&limit=100"
        response3 = self.re_session.get(url_goal3, headers=dict(referer=url_goal3)).text
        response4 = self.re_session.get(url_goal4, headers=dict(referer=url_goal4)).text
        items = json.loads(response3)['data'] + json.loads(response4)['data']
        data = []
        if self.role == "QCP":
            self.actor = "qcer"
        elif self.role == "SCP":
            self.actor = "source_programer"
        else:
            pass
        for item in items:
            if item[self.actor] == self.username:
                data.append(item[key])
        return data

    # 从Tracker中获取adam数据集信息
    def get_adam_data(self, key):
        url_goal = "http://10.20.2.73:8082/system/dataset/ajax_list?study_number=" + self.ProjectName.get() + "-" + self.FolderName.get() + "&page=1&limit=15"
        response = self.re_session.get(url_goal, headers=dict(referer=url_goal)).text
        items = json.loads(response)['data']

        if self.role == "QCP":
            self.actor = "qcer"
        elif self.role == "SCP":
            self.actor = "source_programer"
        else:
            pass

        data = []
        for item in items:
            if item[self.actor] == self.username:
                data.append(item[key])
        return data


    def get_adam_bat(self):
        # 产生bat_username.bat文件
        text1 = '"C:\\Program Files\\SASHome\\SASFoundation\\9.4\\sas.exe"  -sysin '
        if self.role == "SCP":
            text2 = '"' + self.parent_path + "\\program\\adam\\"
        elif self.role == "QCP":
            text2 = '"' + self.parent_path + "\\qc\\program\\adam\\"
        else:
            text2 = None
        text3 = '" -nologo -icon -rsasuser'
        if not os.path.isfile(self.path1.get() + "/" + "bat_" + self.username + ".bat"):
            with open(self.path1.get() + "\\bat_" + self.username + ".bat", 'a', encoding='utf-8') as f:
                f.write("goto whisper\n")
                for each in self.get_adam_data(key='dataset_name'):
                    f.write(text1 + text2 + each.lower() + ".sas" + text3 + "\n")
                f.write(":whisper")
        else:
            pass

        # 产生compare_username.sas文件
        if self.role == "QCP":
            if not os.path.isfile(self.path1.get() + "/" + "compare_" + self.username + ".sas"):
                with open("adam_compare.sas", 'r', encoding='utf-8') as f1, \
                     open(self.path1.get() + "/compare_" + self.username + ".sas", 'a', encoding='utf-8') as f2:
                    old_filename = "File name:"
                    old_project = "Study:"
                    old_dateS = "Date started:"
                    old_dateC = "Date completed:"
                    old_prname = "1.0"
                    new_filename = "compare_" + self.username + ".sas"
                    new_project = self.ProjectName.get()
                    new_date = self.get_date()
                    new_name = self.name_format(self.username)
                    blank_name = (16 - len(new_name)) * " "

                    for line in f1:
                        if old_filename in line:
                            line = line.replace(old_filename, old_filename + "      " + new_filename)
                        if old_project in line:
                            line = line.replace(old_project, old_project + "          " + new_project)
                        if old_dateS in line:
                            line = line.replace(old_dateS, old_dateS + "   " + new_date)
                        if old_dateC in line:
                            line = line.replace(old_dateC, old_dateC + " " + new_date)
                        if old_prname in line:
                            line = line.replace(old_prname,
                                                old_prname + "     " + new_date + "       " + new_name + blank_name + "Create")
                        f2.write(line)

                    for each in self.get_adam_data(key='dataset_name'):
                        f2.write("%qc_m_compare(\n" + "    type=adam,\n" + "    base=adam." + each.lower() + ",\n" + "    compare=adam_qc." + each.lower() + "\n);\n\n")
        else:
            pass

    def get_tfl_bat(self):
        # 产生bat_username.bat文件
        text1 = '"C:\\Program Files\\SASHome\\SASFoundation\\9.4\\sas.exe"  -sysin '
        if self.role == "SCP":
            text2 = '"' + self.parent_path + "\\program\\tfl\\"
        elif self.role == "QCP":
            text2 = '"' + self.parent_path + "\\qc\\program\\tfl\\"
        else:
            text2 = None
        text3 = '" -nologo -icon -rsasuser'
        if not os.path.isfile(self.path2.get() + "/" + "bat_" + self.username + ".bat"):
            with open(self.path2.get() + "\\bat_" + self.username + ".bat", 'a', encoding='utf-8') as f:
                f.write("goto whisper\n")
                for each in self.get_data(key='source_program_name'):
                    f.write(text1 + text2 + each + text3 + "\n")
                f.write(":whisper")
        else:
            pass

        # 产生compare_username.sas文件
        if self.role == "QCP":
            if not os.path.isfile(self.path2.get() + "/" + "compare_" + self.username + ".sas"):
                with open("tfls_compare.sas", 'r', encoding='utf-8') as f1, \
                     open(self.path2.get() + "/compare_" + self.username + ".sas", 'a', encoding='utf-8') as f2:
                    old_filename = "File name:"
                    old_project = "Study:"
                    old_dateS = "Date started:"
                    old_dateC = "Date completed:"
                    old_prname = "1.0"
                    new_filename = "compare_" + self.username + ".sas"
                    new_project = self.ProjectName.get()
                    new_date = self.get_date()
                    new_name = self.name_format(self.username)
                    blank_name = (16 - len(new_name)) * " "

                    for line in f1:
                        if old_filename in line:
                            line = line.replace(old_filename, old_filename + "      " + new_filename)
                        if old_project in line:
                            line = line.replace(old_project, old_project + "          " + new_project)
                        if old_dateS in line:
                            line = line.replace(old_dateS, old_dateS + "   " + new_date)
                        if old_dateC in line:
                            line = line.replace(old_dateC, old_dateC + " " + new_date)
                        if old_prname in line:
                            line = line.replace(old_prname,
                                                old_prname + "     " + new_date + "       " + new_name + blank_name + "Create")
                        f2.write(line)

                    for each in self.get_data(key='original_output_name'):
                        f2.write("%ds_comp(ds=" + each + ", dv=7);" + "\n")
        else:
            pass


    def filepath1(self):
        path_one = filedialog.askdirectory()
        if path_one:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, path_one)

    def filepath2(self):
        path_two = filedialog.askdirectory()
        if path_two:
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, path_two)

    def default(self, event=None):
        self.combobox2.destroy()
        self.folder_names = self.get_folder_name()
        self.combobox2 = ttk.Combobox(self.frame_fold, textvariable=self.FolderName, value=tuple(self.folder_names), width=6)
        self.combobox2.grid(row=0, column=0)
        self.combobox2.bind("<<ComboboxSelected>>", self.default_s)
        self.combobox2.current(0)

        self.parent_path = self.get_parent_path()

        self.default_path1 = ""
        self.default_path2 = ""
        self.get_role()
        if self.role == "QCP":
            self.default_path1 = self.parent_path + "\\qc\\program\\adam"
            self.default_path2 = self.parent_path + "\\qc\\program\\tfl"
        elif self.role == "SCP":
            self.default_path1 = self.parent_path + '\\program\\adam'
            self.default_path2 = self.parent_path + '\\program\\tfl'

        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry1.insert(0, self.default_path1)
        self.entry2.insert(0, self.default_path2)

    def default_s(self, event=None):
        self.get_role()
        self.default_path1 = ""
        self.default_path2 = ""
        self.parent_path = self.get_parent_path()
        if self.role == "QCP":
            self.default_path1 = self.parent_path + "\\qc\\program\\adam"
            self.default_path2 = self.parent_path + "\\qc\\program\\tfl"
        elif self.role == "SCP":
            self.default_path1 = self.parent_path + '\\program\\adam'
            self.default_path2 = self.parent_path + '\\program\\tfl'

        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry1.insert(0, self.default_path1)
        self.entry2.insert(0, self.default_path2)

    def get_name(self):
        url_goal1 = "http://10.20.2.73:8082/system/project/ajax_list"
        response1 = self.re_session.get(url_goal1, headers=dict(referer=url_goal1)).text
        study_list = []
        for each_study in json.loads(response1)["data"]:
            study_list.append(each_study["study_name"])
        study_name = list(set(study_list))
        study_name.sort(key=study_list.index)
        return study_name

    def get_role(self):
        study_name = self.ProjectName.get()
        url_goal2 = "http://10.20.2.73:8082/system/tfls/list/?study_number=" + study_name + "-" + self.FolderName.get()
        response2 = self.re_session.get(url_goal2, headers=dict(referer=url_goal2)).text
        tree2 = html.fromstring(response2)
        SCP_list = tree2.xpath("//select[@name='source_programer']/option/@value")[1:]
        QCP_list = tree2.xpath("//select[@name='qcer']/option/@value")[1:]
        if SCP_list and QCP_list:
            if self.username in SCP_list:
                self.role = "SCP"
            elif self.username in QCP_list:
                self.role = "QCP"
        else:
            tk.messagebox.showinfo(title="提示", message="该项目尚未在项目管理中指定编程角色")
            self.role = None

    def name_format(self, name):
        surname_dict = ["zhao", "qian", "sun", "li", "zhou", "wu", "zheng", "wang", "feng", "chen", "chu", "wei", "jiang",
                        "shen", "han", "yang", "zhu", "qin", "you", "xu", "he", "lv", "shi", "zhang", "kong", "cao", "yan",
                        "hua", "jin", "wei", "tao", "jiang", "qi", "xie", "zou", "yu", "bai", "shui", "dou", "zhang", "yun",
                        "su", "pan", "ge", "xi", "fan", "peng", "lang", "lu", "wei", "chang", "ma", "miao", "feng", "hua",
                        "fang", "yu", "ren", "yuan", "liu", "feng", "bao", "shi", "tang", "fei", "lian", "cen", "xue",
                        "lei", "he", "ni", "tang", "teng", "yin", "luo", "bi", "hao", "wu", "an", "chang", "le", "yu",
                        "shi", "fu", "pi", "bian", "qi", "kang", "wu", "yu", "yuan", "bo", "gu", "meng", "ping", "huang",
                        "he", "mu", "xiao", "yin", "yao", "shao", "zhan", "wang", "qi", "mao", "yu", "di", "mi", "bei",
                        "ming", "zang", "ji", "fu", "cheng", "dai", "tan", "song", "mao", "pang", "xiong", "ji", "shu",
                        "qu", "xiang", "zhu", "dong", "liang", "du", "ruan", "lan", "min", "xi", "ji", "ma", "qiang", "jia",
                        "lu", "lou", "wei", "jiang", "tong", "yan", "guo", "mei", "sheng", "lin", "diao", "zhong", "xu",
                        "qiu", "luo", "gao", "xia", "cai", "tian", "fan", "hu", "ling", "huo", "yu", "wan", "zhi", "ke",
                        "zan", "guan", "lu", "mo", "jing", "fang", "qiu", "miu", "gan", "jie", "ying", "zong", "ding",
                        "xuan", "ben", "deng", "yu", "dan", "hang", "hong", "bao", "zhu", "zuo", "shi", "cui", "ji", "niu",
                        "gong", "cheng", "ji", "xing", "hua", "pei", "lu", "rong", "weng", "xun", "yang", "yu", "hui",
                        "zhen", "qu", "jia", "feng", "rui", "yi", "chu", "jin", "ji", "bing", "mi", "song", "jing", "duan",
                        "fu", "wu", "wu", "jiao", "ba", "gong", "mu", "wei", "shan", "gu", "che", "hou", "mi", "peng",
                        "quan", "xi", "ban", "yang", "qiu", "zhong", "yi", "gong", "ning", "chou", "luan", "bao", "gan",
                        "dou", "li", "rong", "zu", "wu", "fu", "liu", "jing", "zhan", "shu", "long", "ye", "xing", "si",
                        "shao", "gao", "li", "ji", "bo", "yin", "su", "bai", "huai", "pu", "tai", "cong", "e", "suo",
                        "xian", "ji", "lai", "zhuo", "lin", "tu", "meng", "chi", "qiao", "yin", "yu", "xu", "neng", "cang",
                        "shuang", "wen", "xin", "dang", "zhai", "tan", "gong", "lao", "pang", "ji", "shen", "fu", "du",
                        "ran", "zai", "li", "yong", "que", "qu", "sang", "gui", "pu", "niu", "shou", "tong", "bian", "hu",
                        "yan", "ji", "jia", "pu", "shang", "nong", "wen", "bie", "zhuang", "yan", "chai", "ju", "yan",
                        "chong", "mu", "lian", "ru", "xi", "huan", "ai", "yu", "rong", "xiang", "gu", "yi", "shen", "ge",
                        "liao", "yu", "zhong", "ji", "ju", "heng", "bu", "dou", "geng", "man", "hong", "kuang", "guo",
                        "wen", "kou", "guang", "lu", "que", "dong", "ou", "shu", "wo", "li", "wei", "yue", "kui", "long",
                        "shi", "gong", "she", "nie", "chao", "gou", "ao", "rong", "leng", "zi", "xin", "kan", "na", "jian",
                        "rao", "kong", "zeng", "wu", "sha", "mie", "yang", "ju", "xu", "feng", "chao", "guan", "kuai",
                        "xiang", "cha", "hou", "jing", "hong", "you", "zhu", "quan", "lu", "gai", "yi", "huan", "gong",
                        "shang", "mou", "she", "er", "bo", "shang", "mo", "ha", "qiao", "da", "nian", "ai", "tu", "qin",
                        "gui", "hai", "yue", "shuai", "gou", "kang", "kuang", "hou", "you", "qin", "yang", "tong", "diwu",
                        "yan", "fu", "zhang", "du", "jin", "chu", "yan", "fa", "ru", "yan", "moqi", "sima", "shangguan",
                        "ouyang", "xiahou", "zhuge", "wenren", "dongfang", "helian", "huangfu", "weichi", "gongyang",
                        "dantai", "gongye", "zongzheng", "puyang", "chunyu", "danyu", "taishu", "shentu", "gongsun",
                        "zhongsun", "xuanyuan", "linghu", "zhongli", "yuwen", "changsun", "murong", "xianyu", "lvqiu",
                        "situ", "sikong", "jiguan", "sikou", "ziche", "zhuansun", "duanmu", "wuma", "gongxi", "qidiao",
                        "lezheng", "rangsi", "gongliang", "yangshe", "weisheng", "tuoba", "jiagu", "zaifu", "guliang",
                        "duangan", "baili", "dongguo", "nanmen", "huyan", "liangqiu", "zuoqiu", "dongmen", "ximen",
                        "nangong", "liufu"]

        surname_set = list(set(surname_dict))
        name_split = []
        for num_letter in range(8, 1, -1):
            name_split.append(name[:num_letter])

        for each_split in name_split:
            flag = 0
            for each_surname in surname_set:
                if each_split == each_surname:
                    surname = each_surname
                    flag = 1
                    break
            if flag == 1:
                break
        firstname = name[len(surname):]
        format1 = [firstname.capitalize(), surname.capitalize()]
        format2 = ".".join(format1)
        return format2

    def get_date(self):
        t = time.gmtime()
        date = time.strftime("%d%b%Y", t).upper()
        return date

    def get_adam(self):
        self.get_role()

        def alter_A1(adam_template_sas, adam_template_sas_temp,
                     old_project, old_dateS, old_dateC, old_prname, new_project, new_date, new_name):
            with open(adam_template_sas, 'r', encoding='utf-8') as f1, \
                 open(adam_template_sas_temp, 'w', encoding='utf-8') as f2:
                blank_name = (16 - len(new_name)) * " "
                for line in f1:
                    if old_project in line:
                        line = line.replace(old_project, old_project + "          " + new_project)
                    if old_dateS in line:
                        line = line.replace(old_dateS, old_dateS + "   " + new_date)
                    if old_dateC in line:
                        line = line.replace(old_dateC, old_dateC + " " + new_date)
                    if old_prname in line:
                        line = line.replace(old_prname,
                                            old_prname + "     " + new_date + "       " + new_name + blank_name + "Create")
                    f2.write(line)

        def alter_A2(adam_template_sas_temp, adam_sas, old_str1, old_str2, a_new):
            with open(adam_template_sas_temp, 'r', encoding='utf-8') as f1, \
                 open(adam_sas + "/" + a_new.lower() + ".sas", 'w', encoding='utf-8') as f2:
                for line in f1:
                    if old_str1 in line:
                        line = line.replace(old_str1, old_str1 + "      " + a_new + ".sas")
                    if old_str2 in line:
                        line = line.replace(old_str2, old_str2 + "        " + "create " + a_new + " dataset")
                    f2.write(line)

        alter_A1(
            adam_template_sas="adam_template.sas",
            adam_template_sas_temp="ADaM_Template_temp.sas",
            old_project="Study:",
            old_dateS="Date started:",
            old_dateC="Date completed:",
            old_prname="1.0",
            new_project=self.ProjectName.get(),
            new_date=self.get_date(),
            new_name=self.name_format(self.username)
        )


        for a in self.get_adam_data(key='dataset_name'):
            if not os.path.isfile(self.path1.get() + "/" + a + ".sas"):
                alter_A2(
                    adam_template_sas_temp="ADaM_Template_temp.sas",
                    adam_sas=self.path1.get(),
                    old_str1="File name:",
                    old_str2="Purpose:",
                    a_new=a,
                )
            else:
                pass
        os.remove("ADaM_Template_temp.sas")

    def get_tfl(self):
        self.get_role()

        def alter_1(file_1, file_2, old_project, old_dateS, old_dateC, old_prname, new_project, new_date, new_name):
            with open(file_1, 'r', encoding='utf-8') as f1, \
                 open(file_2, 'w', encoding='utf-8') as f2:
                blank_name = (16 - len(new_name)) * " "
                for line in f1:
                    if old_project in line:
                        line = line.replace(old_project, old_project + "          " + new_project)
                    if old_dateS in line:
                        line = line.replace(old_dateS, old_dateS + "   " + new_date)
                    if old_dateC in line:
                        line = line.replace(old_dateC, old_dateC + " " + new_date)
                    if old_prname in line:
                        line = line.replace(old_prname,
                                            old_prname + "     " + new_date + "       " + new_name + blank_name + "Create")
                    f2.write(line)


        def alter_2(file_2, file_3, old_str1, old_str2, a_new, b_new):
            with open(file_2, 'r', encoding='utf-8') as f1, \
                 open(file_3 + "/" + a_new, 'w', encoding='utf-8') as f2:
                for line in f1:
                    if old_str1 in line:
                        line = line.replace(old_str1, old_str1 + "      " + a_new)
                    if old_str2 in line:
                        line = line.replace(old_str2, old_str2 + "        " + b_new)
                    f2.write(line)

        alter_1(
            file_1="tfls_template.sas",
            file_2="Template_transition.sas",
            old_project="Study:",
            old_dateS="Date started:",
            old_dateC="Date completed:",
            old_prname="1.0",
            new_project=self.ProjectName.get(),
            new_date=self.get_date(),
            new_name=self.name_format(self.username)
        )

        for a, b in zip(self.get_data(key='source_program_name'), self.get_data(key='title')):
            if not os.path.isfile(self.path2.get() + "/" + a):
                alter_2(
                    file_2="Template_transition.sas",
                    file_3=self.path2.get(),
                    old_str1="File name:",
                    old_str2="Purpose:",
                    a_new=a,
                    b_new=b
                )
            else:
                pass
        os.remove("Template_transition.sas")





