
import os
import time
import xlwings as xw
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QMouseEvent, QFont
import qtawesome as qs

class MainUi(QtWidgets.QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    def __init__(self):
        super().__init__()
        self.init_ui()

    # Rewriting the move event.
    def mouseMoveEvent(self, e: QMouseEvent):
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def init_ui(self):
        # main window
        self.setFixedSize(380, 180)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # quit button
        self.quit_button = QtWidgets.QPushButton(qs.icon('fa.close', color='black'), "")
        self.quit_button.clicked.connect(self.quit)

        # import path widget
        self.import_widget = QtWidgets.QWidget()
        self.import_layout = QtWidgets.QGridLayout()
        self.import_widget.setLayout(self.import_layout)
        self.import_path = QtWidgets.QLineEdit()
        self.import_path.setPlaceholderText("Excel file path")
        self.import_path.setFont(QFont("Arial", 10))
        self.import_button = QtWidgets.QPushButton("•••")
        self.import_button.setFont(QFont("Arial", 10))
        self.import_button.clicked.connect(self.import_path_method)
        self.import_button.setMaximumWidth(30)
        self.import_layout.addWidget(self.import_path, 0, 0, 1, 1)
        self.import_layout.addWidget(self.import_button, 0, 1, 1, 1)

        # export path widget
        self.export_widget = QtWidgets.QWidget()
        self.export_layout = QtWidgets.QGridLayout()
        self.export_widget.setLayout(self.export_layout)
        self.export_path = QtWidgets.QLineEdit()
        self.export_path.setPlaceholderText("SAS export path")
        self.export_path.setFont(QFont("Arial", 10))
        self.export_button = QtWidgets.QPushButton("•••")
        self.export_button.setFont(QFont("Arial", 10))
        self.export_button.clicked.connect(self.export_path_method)
        self.export_button.setMaximumWidth(30)
        self.export_layout.addWidget(self.export_path, 0, 0, 1, 1)
        self.export_layout.addWidget(self.export_button, 0, 1, 1, 1)

        # input widget
        self.inputdata_widget = QtWidgets.QWidget()
        self.inputdata_layout = QtWidgets.QGridLayout()
        self.inputdata_widget.setLayout(self.inputdata_layout)
        self.username_line = QtWidgets.QLineEdit()
        self.username_line.setPlaceholderText("username")
        self.username_line.setFont(QFont("Arial", 10))
        # self.role_box = QtWidgets.QComboBox()
        # items = ["SCP", "QCP"]
        # self.role_box.addItems(items)
        # self.role_box.setCurrentIndex(0)
        # self.role_box.setPlaceholderText("role")
        # self.role_box.setFont(QFont("Arial", 10))
        self.inputdata_layout.addWidget(self.username_line, 0, 0, 1, 1)
        # self.inputdata_layout.addWidget(self.role_box, 0, 1, 1, 1)

        # boot widget
        self.boot_widget = QtWidgets.QWidget()
        self.boot_layout = QtWidgets.QGridLayout()
        self.boot_widget.setLayout(self.boot_layout)
        self.ADaM_button = QtWidgets.QPushButton(qs.icon('fa.github-alt', color='black'), "ADaM")
        self.ADaM_button.setFont(QFont("Arial", 10))
        self.ADaM_button.clicked.connect(self.generate)
        self.ADaM_button.setMaximumWidth(80)
        self.tfl_button = QtWidgets.QPushButton(qs.icon('fa.github-alt', color='black'), "Hooray！")
        self.tfl_button.setFont(QFont("Arial", 10))
        self.tfl_button.clicked.connect(self.generate)
        self.tfl_button.setMaximumWidth(80)
        # self.boot_layout.addWidget(self.ADaM_button, 0, 2, 1, 1)
        self.boot_layout.addWidget(self.tfl_button, 0, 4, 1, 1)

        # put up
        self.main_layout.addWidget(self.quit_button, 0, 5, 1, 5)
        self.main_layout.addWidget(self.import_widget, 1, 0, 1, 5)
        self.main_layout.addWidget(self.export_widget, 2, 0, 1, 5)
        self.main_layout.addWidget(self.inputdata_widget, 3, 0, 1, 5)
        self.main_layout.addWidget(self.boot_widget, 4, 0, 1, 5)

        # self.range = QtWidgets.QLineEdit()
        # self.range.setFont(QtGui.QFont("Arial", 10))
        # self.range.setMaximumWidth(80)
        # self.range.setAlignment(QtCore.Qt.AlignCenter)
        # self.range.setReadOnly(False)
        # self.range.setPlaceholderText("Range")

        self.quit_button.setStyleSheet(
            '''QPushButton{
                            background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')
        self.import_path.setFixedSize(300, 25)
        self.import_path.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')

        self.import_button.setFixedSize(20, 20)
        self.import_button.setStyleSheet(
            '''QPushButton{
                            background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')

        self.export_path.setFixedSize(300, 25)
        self.export_path.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')

        self.export_button.setFixedSize(20, 20)
        self.export_button.setStyleSheet(
            '''QPushButton{background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')

        self.username_line.setFixedSize(120, 25)
        self.username_line.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')

        # self.role_box.setFixedSize(80, 25)
        # self.role_box.setStyleSheet(
        #     '''QLineEdit{
        #             border:1px solid gray;
        #             width:300px;
        #             border-radius:10px;
        #             padding:2px 4px;
        #     }''')

        self.tfl_button.setFixedSize(80, 20)
        self.tfl_button.setStyleSheet(
            '''QPushButton{
                            background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')

        self.ADaM_button.setFixedSize(80, 20)
        self.ADaM_button.setStyleSheet(
            '''QPushButton{background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')

        self.setWindowOpacity(1)  # Set window transparency
        self.setAttribute(Qt.WA_TranslucentBackground)  # Set transparent window background
        self.setWindowFlag(Qt.FramelessWindowHint)  # Hide borders
        self.main_widget.setStyleSheet('''
                QWidget{
                    background:#fabfb0;
                    border-top:1px solid #fabfb0;
                    border-bottom:1px solid #fabfb0;
                    border-left:1px solid #fabfb0;
                    border-right:1px solid #fabfb0;
                    border-top-left-radius:8px;
                    border-bottom-left-radius:8px;
                    border-top-right-radius:8px;
                    border-bottom-right-radius:8px;
                }
                ''')
        self.main_layout.setSpacing(0)

    def quit(self):
        self.close()

    def import_path_method(self):
        self.import_path_dig = QtWidgets.QFileDialog().getOpenFileName(self, 'Open File', '.', 'EXCEL file(*.xlsx *.xls)')
        self.import_path.setText(self.import_path_dig[0])

    def export_path_method(self):
        self.export_path_dig = QtWidgets.QFileDialog().getExistingDirectory(self, 'Open File Folder', '.')
        self.export_path.setText(self.export_path_dig)

    def information(self):
        self.reply = QtWidgets.QMessageBox.information(self, 'tips', self.program_type + " generated successfully")

    # Use the generation date of the SAS program as the programming date of the program header.
    def get_date(self):
        t = time.gmtime()
        date = time.strftime("%d%b%Y", t).upper()
        return date

    # Convert username to a standard format. for example: ZengMing ----> Ming.Zeng
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

    # Get the user's role of statistical programming
    def get_role(self):
        self.get_excel_data()
        self.sourcer_list = []
        self.qcer_list = []
        self.get_program_type()
        if self.program_type == "SDTM":
            self.column_count = 7
        elif self.program_type == "ADaM":
            self.column_count = 7
        elif self.program_type == "TFLS":
            self.column_count = 15

        for each in self.AK:
            if each[self.column_count] is not None and each[self.column_count] not in self.sourcer_list:
                self.sourcer_list.append(each[self.column_count])
            if each[self.column_count + 1] is not None and each[self.column_count + 1] not in self.qcer_list:
                self.qcer_list.append(each[self.column_count + 1])

        if self.username in self.sourcer_list:
            self.role = "SCP"
            self.seq = self.column_count
        elif self.username in self.qcer_list:
            self.role = "QCP"
            self.seq = self.column_count + 1


    # Judge the type of Excel data directly according to the name of Excel File.(SDTM or AdaM or TFLS);
    def get_program_type(self):
        if "SDTM" in self.import_path.text():
            self.program_type = "SDTM"
        elif "ADaM" in self.import_path.text():
            self.program_type = "ADaM"
        elif "TFLS" in self.import_path.text():
            self.program_type = "TFLS"

        return self.program_type

    def get_excel_data(self):
        self.app = xw.App(visible=False, add_book=False)
        self.wb = self.app.books.open(self.import_path.text())
        self.sheet0_docs = self.wb.sheets[0]
        self.AK = self.sheet0_docs.range("A2:X200").value
        self.Project_Name = self.AK[0][1].split("-")[0]
        self.username = self.username_line.text()

    def get_data(self, key):
        data = []
        for item in self.AK:
            if item[self.seq] == self.username:
                data.append(item[key])
        return data

    def generate(self):
        self.get_role()
        if self.program_type == "SDTM":
            self.get_sdtm()
        elif self.program_type == "ADaM":
            self.get_adam()
        elif self.program_type == "TFLS":
            self.get_tfl()
        self.information()

    def get_tfl(self):
        def alter_1(file_1, file_2, old_project, old_dateS, old_dateC, old_prname, new_project, new_date, new_name):
            with open(file_1, 'r', encoding='utf-8', errors='ignore') as f1, \
                    open(file_2, 'w', encoding='utf-8', errors='ignore') as f2:
                blank_name = (16 - len(new_name)) * " "
                for line in f1:
                    if old_project in line:
                        line = line.replace(old_project, old_project + 10 * " " + new_project)
                    if old_dateS in line:
                        line = line.replace(old_dateS, old_dateS + 3 * " " + new_date)
                    if old_dateC in line:
                        line = line.replace(old_dateC, old_dateC + " " + new_date)
                    if old_prname in line:
                        line = line.replace(old_prname,
                                            old_prname + 5 * " " + new_date + 7 * " " + new_name + blank_name + "Create")
                    f2.write(line)

        def alter_2(file_2, file_3, old_str1, old_str2, a_new, b_new, type):
            with open(file_2, 'r', encoding='utf-8', errors='ignore') as f1, \
                    open(file_3 + "/" + a_new, 'w', encoding='utf-8', errors='ignore') as f2:
                for line in f1:
                    if type == "pdf":
                        if "%RTFtemp" in line:
                            line = line.replace("%RTFtemp", "%PDFtemp")
                    if old_str1 in line:
                        line = line.replace(old_str1, old_str1 + 6 * " " + a_new)
                    if old_str2 in line:
                        line = line.replace(old_str2, old_str2 + 8 * " " + b_new)
                    f2.write(line)

        self.get_role()

        alter_1(
            file_1="tfls_template.txt",
            file_2="Template_transition.txt",
            old_project="Study:",
            old_dateS="Date started:",
            old_dateC="Date completed:",
            old_prname="1.0",
            new_project=self.Project_Name,
            new_date=self.get_date(),
            new_name=self.name_format(self.username)
        )

        for a, b, t in zip(self.get_data(key=4), self.get_data(key=6),
                           self.get_data(key=3)):
            if not os.path.isfile(self.export_path.text() + "/" + a + ".sas"):
                alter_2(
                    file_2="Template_transition.txt",
                    file_3=self.export_path.text(),
                    old_str1="File name:",
                    old_str2="Purpose:",
                    a_new=a + ".sas",
                    b_new=b,
                    type=t
                )
            else:
                pass
        os.remove("Template_transition.txt")
        # messagebox.showinfo('tips', 'TFLs generated successfully')
        self.get_tfl_bat()
        self.wb.close()

    def get_sdtm(self):
        def alter_1(file_1, file_2, old_project, old_dateS, old_dateC, old_prname, new_project, new_date, new_name):
            with open(file_1, 'r', encoding='utf-8', errors='ignore') as f1, \
                    open(file_2, 'w', encoding='utf-8', errors='ignore') as f2:
                blank_name = (16 - len(new_name)) * " "
                for line in f1:
                    if old_project in line:
                        line = line.replace(old_project, old_project + 10 * " " + new_project)
                    if old_dateS in line:
                        line = line.replace(old_dateS, old_dateS + 3 * " " + new_date)
                    if old_dateC in line:
                        line = line.replace(old_dateC, old_dateC + " " + new_date)
                    if old_prname in line:
                        line = line.replace(old_prname,
                                            old_prname + 5 * " " + new_date + 7 * " " + new_name + blank_name + "Create")
                    f2.write(line)

        def alter_2(file_2, file_3, old_str1, old_str2, a_new, b_new):
            with open(file_2, 'r', encoding='utf-8', errors='ignore') as f1, \
                    open(file_3 + "/" + a_new, 'w', encoding='utf-8', errors='ignore') as f2:
                for line in f1:
                    if old_str1 in line:
                        line = line.replace(old_str1, old_str1 + 6 * " " + a_new)
                    if old_str2 in line:
                        line = line.replace(old_str2, old_str2 + 8 * " " + b_new)
                    f2.write(line)

        self.get_role()

        alter_1(
            file_1="sdtm_template.txt",
            file_2="Template_transition.txt",
            old_project="Study:",
            old_dateS="Date started:",
            old_dateC="Date completed:",
            old_prname="1.0",
            new_project=self.Project_Name,
            new_date=self.get_date(),
            new_name=self.name_format(self.username)
        )

        for a, b in zip(self.get_data(key=4), self.get_data(key=5)):
            if not os.path.isfile(self.export_path.text() + "/" + a.lower() + ".sas"):
                alter_2(
                    file_2="Template_transition.txt",
                    file_3=self.export_path.text(),
                    old_str1="File name:",
                    old_str2="Purpose:",
                    a_new=a.lower() + ".sas",
                    b_new=b,
                )
            else:
                pass
        os.remove("Template_transition.txt")
        # messagebox.showinfo('tips', 'TFLs generated successfully')
        self.get_sdtm_bat()
        self.wb.close()

    def get_adam(self):
        def alter_A1(adam_template_sas, adam_template_sas_temp,
                     old_project, old_dateS, old_dateC, old_prname, new_project, new_date, new_name):
            with open(adam_template_sas, 'r', encoding='utf-8', errors='ignore') as f1, \
                 open(adam_template_sas_temp, 'w', encoding='utf-8', errors='ignore') as f2:
                blank_name = (16 - len(new_name)) * " "
                for line in f1:
                    if old_project in line:
                        line = line.replace(old_project, old_project + 10 * " " + new_project)
                    if old_dateS in line:
                        line = line.replace(old_dateS, old_dateS + 3 * " " + new_date)
                    if old_dateC in line:
                        line = line.replace(old_dateC, old_dateC + " " + new_date)
                    if old_prname in line:
                        line = line.replace(old_prname,
                                            old_prname + 5 * " " + new_date + 7 * " " + new_name + blank_name + "Create")
                    f2.write(line)

        def alter_A2(adam_template_sas_temp, adam_sas, old_str1, old_str2, a_new):
            with open(adam_template_sas_temp, 'r', encoding='utf-8', errors='ignore') as f1, \
                 open(adam_sas + "/" + a_new.lower() + ".sas", 'w', encoding='utf-8', errors='ignore') as f2:
                for line in f1:
                    if old_str1 in line:
                        line = line.replace(old_str1, old_str1 + 6 * " " + a_new + ".sas")
                    if old_str2 in line:
                        line = line.replace(old_str2, old_str2 + 8 * " " + "create " + a_new + " dataset")
                    f2.write(line)


        alter_A1(
            adam_template_sas="adam_template.txt",
            adam_template_sas_temp="Template_transition.txt",
            old_project="Study:",
            old_dateS="Date started:",
            old_dateC="Date completed:",
            old_prname="1.0",
            new_project=self.Project_Name,
            new_date=self.get_date(),
            new_name=self.name_format(self.username)
        )

        for a in self.get_data(key=4):
            if not os.path.isfile(self.export_path.text() + "/" + a.lower() + ".sas"):
                alter_A2(
                    adam_template_sas_temp="Template_transition.txt",
                    adam_sas=self.export_path.text(),
                    old_str1="File name:",
                    old_str2="Purpose:",
                    a_new=a.lower(),
                )
            else:
                pass
        os.remove("Template_transition.txt")
        self.get_adam_bat()
        self.wb.close()


    def get_tfl_bat(self):
        # generate bat_username.bat
        self.parent_path = "Z:\\studies\\" + self.Project_Name + "\\STAT\\testdir"
        text1 = '"C:\\Program Files\\SASHome\\SASFoundation\\9.4\\sas.exe"  -sysin '
        if self.role == "SCP":
            text2 = '"' + self.parent_path + "\\program\\tfl\\"
        elif self.role == "QCP":
            text2 = '"' + self.parent_path + "\\qc\\program\\tfl\\"
        else:
            text2 = None
        text3 = '" -nologo -icon -rsasuser'
        if not os.path.isfile(self.export_path.text() + "/" + "bat_" + self.username + ".bat"):
            with open(self.export_path.text() + "\\bat_" + self.username + ".bat", 'a', encoding='utf-8', errors='ignore') as f:
                f.write("goto whisper\n")
                for each in self.get_data(key=4):
                    f.write(text1 + text2 + each + ".sas" + text3 + "\n")
                f.write(":whisper")
            # messagebox.showinfo('tips', 'bat[compare] generated successfully')
        else:
            pass

        # generate compare_username.sas
        if self.role == "QCP":
            if not os.path.isfile(self.export_path.text() + "/" + "compare_" + self.username + ".sas"):
                with open("tfls_compare.txt", 'r', encoding='utf-8', errors='ignore') as f1, \
                     open(self.export_path.text() + "/compare_" + self.username + ".sas", 'a', encoding='utf-8', errors='ignore') as f2:
                    old_filename = "File name:"
                    old_project = "Study:"
                    old_dateS = "Date started:"
                    old_dateC = "Date completed:"
                    old_prname = "1.0"
                    new_filename = "compare_" + self.username + ".sas"
                    new_project = self.Project_Name
                    new_date = self.get_date()
                    new_name = self.name_format(self.username)
                    blank_name = (16 - len(new_name)) * " "

                    for line in f1:
                        if old_filename in line:
                            line = line.replace(old_filename, old_filename + 6 * " " + new_filename)
                        if old_project in line:
                            line = line.replace(old_project, old_project + 10 * " " + new_project)
                        if old_dateS in line:
                            line = line.replace(old_dateS, old_dateS + 3 * " " + new_date)
                        if old_dateC in line:
                            line = line.replace(old_dateC, old_dateC + " " + new_date)
                        if old_prname in line:
                            line = line.replace(old_prname,
                                                old_prname + 5 * " " + new_date + 7 * " " + new_name + blank_name + "Create")
                        f2.write(line)

                    for each in self.get_data(key=4):
                        f2.write("%ds_comp(ds=" + each + ", dv=7);" + "\n")

        else:
            pass


    def get_sdtm_bat(self):
        # generate bat_username.bat
        self.parent_path = "Z:\\studies\\" + self.Project_Name + "\\STAT\\testdir"
        text1 = '"C:\\Program Files\\SASHome\\SASFoundation\\9.4\\sas.exe"  -sysin '
        if self.role == "SCP":
            text2 = '"' + self.parent_path + "\\program\\sdtm\\"
        elif self.role == "QCP":
            text2 = '"' + self.parent_path + "\\qc\\program\\sdtm\\"
        else:
            text2 = None
        text3 = '" -nologo -icon -rsasuser'
        if not os.path.isfile(self.export_path.text() + "/" + "bat_" + self.username + ".bat"):
            with open(self.export_path.text() + "\\bat_" + self.username + ".bat", 'a', encoding='utf-8', errors='ignore') as f:
                f.write("goto whisper\n")
                for each in self.get_data(key=4):
                    f.write(text1 + text2 + each.lower() + ".sas" + text3 + "\n")
                f.write(":whisper")
            # messagebox.showinfo('tips', 'bat[compare] generated successfully')
        else:
            pass

        # generate compare_username.sas
        if self.role == "QCP":
            if not os.path.isfile(self.export_path.text() + "/" + "compare_" + self.username + ".sas"):
                with open("sdtm_compare.txt", 'r', encoding='utf-8', errors='ignore') as f1, \
                     open(self.export_path.text() + "/compare_" + self.username + ".sas", 'a', encoding='utf-8', errors='ignore') as f2:
                    old_filename = "File name:"
                    old_project = "Study:"
                    old_dateS = "Date started:"
                    old_dateC = "Date completed:"
                    old_prname = "1.0"
                    new_filename = "compare_" + self.username + ".sas"
                    new_project = self.Project_Name
                    new_date = self.get_date()
                    new_name = self.name_format(self.username)
                    blank_name = (16 - len(new_name)) * " "

                    for line in f1:
                        if old_filename in line:
                            line = line.replace(old_filename, old_filename + 6 * " " + new_filename)
                        if old_project in line:
                            line = line.replace(old_project, old_project + 10 * " " + new_project)
                        if old_dateS in line:
                            line = line.replace(old_dateS, old_dateS + 3 * " " + new_date)
                        if old_dateC in line:
                            line = line.replace(old_dateC, old_dateC + " " + new_date)
                        if old_prname in line:
                            line = line.replace(old_prname,
                                                old_prname + 5 * " " + new_date + 7 * " " + new_name + blank_name + "Create")
                        f2.write(line)

                    for each in self.get_data(key=4):
                        f2.write("%qc_m_compare(\n" + "  type     =sdtm\n" + "  ,base    =sdtm." + each.lower() + "\n  ,compare =sdtm_qc." + each.lower() + "\n);\n\n")

        else:
            pass

    def get_adam_bat(self):
        # generate bat_username.bat
        self.parent_path = "Z:\\studies\\" + self.Project_Name + "\\STAT\\testdir"
        text1 = '"C:\\Program Files\\SASHome\\SASFoundation\\9.4\\sas.exe"  -sysin '
        if self.role == "SCP":
            text2 = '"' + self.parent_path + "\\program\\adam\\"
        elif self.role == "QCP":
            text2 = '"' + self.parent_path + "\\qc\\program\\adam\\"
        else:
            text2 = None
        text3 = '" -nologo -icon -rsasuser'
        if not os.path.isfile(self.export_path.text() + "/" + "bat_" + self.username + ".bat"):
            with open(self.export_path.text() + "\\bat_" + self.username + ".bat", 'a', encoding='utf-8', errors='ignore') as f:
                f.write("goto whisper\n")
                for each in self.get_data(key=4):
                    f.write(text1 + text2 + each.lower() + ".sas" + text3 + "\n")
                f.write(":whisper")
            # messagebox.showinfo('tips', 'bat[compare] generated successfully')
        else:
            pass


        # generate compare_username.sas
        if self.role == "QCP":
            if not os.path.isfile(self.export_path.text() + "/" + "compare_" + self.username + ".sas"):
                with open("adam_compare.txt", 'r', encoding='utf-8', errors='ignore') as f1, \
                        open(self.export_path.text() + "/compare_" + self.username + ".sas", 'a', encoding='utf-8', errors='ignore') as f2:
                    old_filename = "File name:"
                    old_project = "Study:"
                    old_dateS = "Date started:"
                    old_dateC = "Date completed:"
                    old_prname = "1.0"
                    new_filename = "compare_" + self.username + ".sas"
                    new_project = self.Project_Name
                    new_date = self.get_date()
                    new_name = self.name_format(self.username)
                    blank_name = (16 - len(new_name)) * " "

                    for line in f1:
                        if old_filename in line:
                            line = line.replace(old_filename, old_filename + 6 * " " + new_filename)
                        if old_project in line:
                            line = line.replace(old_project, old_project + 10 * " " + new_project)
                        if old_dateS in line:
                            line = line.replace(old_dateS, old_dateS + 3 * " " + new_date)
                        if old_dateC in line:
                            line = line.replace(old_dateC, old_dateC + " " + new_date)
                        if old_prname in line:
                            line = line.replace(old_prname,
                                                old_prname + 5 * " " + new_date + 7 * " " + new_name + blank_name + "Create")
                        f2.write(line)

                    for each in self.get_data(key=4):
                        f2.write(
                            "%qc_m_compare(\n" + "    type=adam,\n" + "    base=adam." + each.lower() + ",\n" + "    compare=adam_qc." + each.lower() + "\n);\n\n")
        else:
            pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
# pyinstaller -w -F -i clt_ico.ico -n demo demo.py



