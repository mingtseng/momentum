from xml.dom.minidom import parse
import xlwings as xw
import re
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

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
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
        self.setFixedSize(380, 180)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.quit_button = QtWidgets.QPushButton(qs.icon('fa.close', color='black'), "")
        self.quit_button.clicked.connect(self.quit)

        self.proto_xml_widget = QtWidgets.QWidget()
        self.proto_xml_layout = QtWidgets.QGridLayout()
        self.proto_xml_widget.setLayout(self.proto_xml_layout)
        self.path1 = QtWidgets.QLineEdit()
        self.path1.setPlaceholderText("Prototype define.xml file path")
        self.path1.setFont(QFont("Arial", 10))
        self.button1 = QtWidgets.QPushButton("•••")
        self.button1.setFont(QFont("Arial", 10))
        self.button1.clicked.connect(self.path1_method)
        self.button1.setMaximumWidth(30)
        self.proto_xml_layout.addWidget(self.path1, 0, 0, 1, 1)
        self.proto_xml_layout.addWidget(self.button1, 0, 1, 1, 1)

        self.inputdata_widget = QtWidgets.QWidget()
        self.inputdata_layout = QtWidgets.QGridLayout()
        self.inputdata_widget.setLayout(self.inputdata_layout)
        self.path2 = QtWidgets.QLineEdit()
        self.path2.setPlaceholderText("ARM data Excel file path")
        self.path2.setFont(QFont("Arial", 10))
        self.button2 = QtWidgets.QPushButton("•••")
        self.button2.setFont(QFont("Arial", 10))
        self.button2.clicked.connect(self.path2_method)
        self.button2.setMaximumWidth(30)

        # self.range = QtWidgets.QLineEdit()
        # self.range.setFont(QtGui.QFont("Arial", 10))
        # self.range.setMaximumWidth(80)
        # self.range.setAlignment(QtCore.Qt.AlignCenter)
        # self.range.setReadOnly(False)
        # self.range.setPlaceholderText("Range")
        self.button3 = QtWidgets.QPushButton(qs.icon('fa.github-alt', color='black'), "APPEND")
        self.button3.clicked.connect(self.APPEND)
        self.button3.setFont(QFont("Arial", 10))
        self.button3.setMaximumWidth(80)

        self.inputdata_layout.addWidget(self.path2, 0, 0, 1, 1)
        self.inputdata_layout.addWidget(self.button2, 0, 1, 1, 1)
        # self.inputdata_layout.addWidget(self.range, 1, 0, 1, 1)

        self.main_layout.addWidget(self.quit_button, 0, 5, 1, 5)
        self.main_layout.addWidget(self.proto_xml_widget, 1, 0, 1, 5)
        self.main_layout.addWidget(self.inputdata_widget, 2, 0, 1, 5)
        self.main_layout.addWidget(self.button3, 3, 2, 1, 1)

        self.path1.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')
        self.path2.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')
        # self.range.setStyleSheet(
        #     '''QLineEdit{
        #             border:1px solid gray;
        #             width:300px;
        #             border-radius:10px;
        #             padding:2px 4px;
        #     }''')
        # 控制按钮
        self.button1.setFixedSize(20, 20)
        self.button2.setFixedSize(20, 20)
        self.button3.setFixedSize(80, 20)
        self.button1.setStyleSheet(
            '''QPushButton{
                            background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')
        self.button2.setStyleSheet(
            '''QPushButton{background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')
        self.button3.setStyleSheet(
            '''QPushButton{
                            background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')
        self.quit_button.setStyleSheet(
            '''QPushButton{
                            background:#E6CEAC;
                            border-top-left-radius:8px;
                            border-top-right-radius:8px;
                            border-bottom-left-radius:8px;
                            border-bottom-right-radius:8px;}
               QPushButton:hover{background:#F4606C;}''')

        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        self.main_widget.setStyleSheet('''
                QWidget{
                    background:#FDE6E0;
                    border-top:1px solid #FDE6E0;
                    border-bottom:1px solid #FDE6E0;
                    border-left:1px solid #FDE6E0;
                    border-right:1px solid #FDE6E0;
                    border-top-left-radius:8px;
                    border-bottom-left-radius:8px;
                    border-top-right-radius:8px;
                    border-bottom-right-radius:8px;
                }
                ''')
        self.main_layout.setSpacing(0)

    def quit(self):
        self.close()

    def path1_method(self):
        self.dig1 = QtWidgets.QFileDialog().getOpenFileName(self, 'Open File', '.', 'XML Files(*.xml)')
        self.path1.setText(self.dig1[0])

    def path2_method(self):
        self.dig2 = QtWidgets.QFileDialog().getOpenFileName(self, 'Open File', '.', 'EXCEL Files(*.xlsx *.xls)')
        self.path2.setText(self.dig2[0])

    def information(self):
        reply = QtWidgets.QMessageBox.about(self, 'tips', 'Building demo.xml from define.xml compelted successfully')

    def APPEND(self):
        app = xw.App(visible=False, add_book=False)
        wb = app.books.open(self.path2.text())

        sheet0_docs = wb.sheets[0]
        AK = sheet0_docs.range("A2:V100").value
        wb.save()
        wb.close()

        docs0 = []
        for i in AK:
            if i[0] is not None:
                docs0.append(i)
        domTree = parse(self.path1.text())
        rootNode = domTree.documentElement
        rootNode.setAttribute("xmlns:arm", "http://www.cdisc.org/ns/arm/v1.0")
        Wizard_MetaDataVersion = rootNode.getElementsByTagName("MetaDataVersion")[0]
        temp_ID = []
        sub_list = []
        total_list = []
        for row in docs0:
            if len(temp_ID) == 0:
                temp_ID.append(row[0])
                sub_list.append(row)
            else:
                if temp_ID[0] == row[0]:
                    sub_list.append(row)
                    if docs0.index(row) == len(docs0) - 1:
                        total_list.append(sub_list)
                else:
                    total_list.append(sub_list)
                    temp_ID.pop()
                    temp_ID.append(row[0])
                    sub_list = []
                    sub_list.append(row)
                    if docs0.index(row) == len(docs0) - 1:
                        total_list.append(sub_list)

        for sub_list in total_list:
            common = sub_list[0]
            ID_a = common[0].replace(" ", "_")
            common_ID = "LF." + ID_a
            common_Title = common[0]
            common_Href = common[2]
            Node1_leaf = domTree.createElement("def:leaf")
            Node1_leaf.setAttribute("ID", common_ID)
            Node1_leaf.setAttribute("xlink:href", common_Href)
            Node2_title = domTree.createElement("def:title")
            Node2_title_text = domTree.createTextNode(common_Title)
            Node2_title.appendChild(Node2_title_text)
            Node1_leaf.appendChild(Node2_title)
            Wizard_MetaDataVersion.appendChild(Node1_leaf)
            for each_table in sub_list:
                doc_ID = []
                doc_Title = []
                doc_Href = []

                sas_title = each_table[16].split("txt")[0] + "sas"
                doc_ID.append("LF.SAP-SEC-" + each_table[11].split()[2].strip())
                doc_ID.append("LF." + sas_title)
                doc_Title.append(each_table[11])
                doc_Title.append(sas_title)
                doc_Href.append(each_table[12])
                doc_Href.append(each_table[16])

                for ID, Title, Href in zip(doc_ID, doc_Title, doc_Href):
                    Node1_leaf = domTree.createElement("def:leaf")
                    Node1_leaf.setAttribute("ID", ID)
                    Node1_leaf.setAttribute("xlink:href", Href)
                    Node2_title = domTree.createElement("def:title")
                    Node2_title_text = domTree.createTextNode(Title)
                    Node2_title.appendChild(Node2_title_text)
                    Node1_leaf.appendChild(Node2_title)
                    Wizard_MetaDataVersion.appendChild(Node1_leaf)

        pattern = re.compile(r'[^\s()]+')
        for sub_list in total_list:
            for each_data in sub_list:
                ID = each_data[0].replace(" ", "_") + "." + each_data[3]
                where_str = []
                dss = []
                if "JOIN" in each_data[9]:
                    for ds in each_data[9].split("JOIN"):
                        dss.append(ds.strip().split()[0])
                        where_str.append(ds.strip().split("[")[1].split("]")[0].strip())
                else:
                    dss.append(each_data[9].strip().split()[0])
                    where_str.append(each_data[9].strip().split("[")[1].split("]")[0].strip())

                for adam, each_where in zip(dss, where_str):
                    Node1_WhereClauseDef = domTree.createElement("def:WhereClauseDef")
                    Node1_WhereClauseDef.setAttribute("OID", "WC." + ID + "." + adam)
                    Wizard_MetaDataVersion.appendChild(Node1_WhereClauseDef)

                    sub_str = each_where.split("and")
                    for pie in sub_str:
                        if pie.split()[1].strip().upper() == "IN":
                            Node2_RangeCheck = domTree.createElement("RangeCheck")
                            Node1_WhereClauseDef.appendChild(Node2_RangeCheck)
                            Node2_RangeCheck.setAttribute("Comparator", "IN")
                            Node2_RangeCheck.setAttribute("SoftHard", "Soft")
                            Node2_RangeCheck.setAttribute("def:ItemOID", "IT." + adam + "." + pie.split()[0].strip())
                            value = list(map(lambda x: x.replace('"', ''),
                                             re.findall(pattern, pie.split(pie.split()[1])[1].strip())))
                            for each_value in value:
                                Node3_CheckValue = domTree.createElement("CheckValue")
                                Node2_RangeCheck.appendChild(Node3_CheckValue)
                                Node4_CheckValue_text = domTree.createTextNode(each_value)
                                Node3_CheckValue.appendChild(Node4_CheckValue_text)
                        elif pie.split()[1].strip().upper() in ("EQ", "="):
                            Node2_RangeCheck = domTree.createElement("RangeCheck")
                            Node1_WhereClauseDef.appendChild(Node2_RangeCheck)
                            Node2_RangeCheck.setAttribute("Comparator", "EQ")
                            Node2_RangeCheck.setAttribute("SoftHard", "Soft")
                            Node2_RangeCheck.setAttribute("def:ItemOID", "IT." + adam + "." + pie.split()[0].strip())
                            Node3_CheckValue = domTree.createElement("CheckValue")
                            Node2_RangeCheck.appendChild(Node3_CheckValue)
                            Node4_CheckValue_text = domTree.createTextNode(
                                pie.split(pie.split()[1])[1].strip().replace('"', ''))
                            Node3_CheckValue.appendChild(Node4_CheckValue_text)

        Node1_AnalysisResultDisplays = domTree.createElement("arm:AnalysisResultDisplays")
        Wizard_MetaDataVersion.appendChild(Node1_AnalysisResultDisplays)
        for sub_list in total_list:
            common = sub_list[0]
            ID = common[0].replace(" ", "_")
            Node2_ResultDisplay = domTree.createElement("arm:ResultDisplay")
            Node2_ResultDisplay.setAttribute("Name", common[0])
            Node2_ResultDisplay.setAttribute("OID", "RD." + ID)

            Node3_Description = domTree.createElement("Description")
            Node4_TranslatedText = domTree.createElement("TranslatedText")
            Node4_TranslatedText.setAttribute("xml:lang", "en")
            Node5_Text = domTree.createTextNode(common[1])
            Node4_TranslatedText.appendChild(Node5_Text)
            Node3_Description.appendChild(Node4_TranslatedText)

            Node3_DocumentRef = domTree.createElement("def:DocumentRef")
            Node3_DocumentRef.setAttribute("leafID", "LF." + ID)
            Node4_PDFPageRef = domTree.createElement("def:PDFPageRef")
            Node4_PDFPageRef.setAttribute("PageRefs", "1")
            Node4_PDFPageRef.setAttribute("Type", "PhysicalRef")
            Node3_DocumentRef.appendChild(Node4_PDFPageRef)

            Node1_AnalysisResultDisplays.appendChild(Node2_ResultDisplay)
            Node2_ResultDisplay.appendChild(Node3_Description)
            Node2_ResultDisplay.appendChild(Node3_DocumentRef)

            for each_data in sub_list:
                Node3_AnalysisResult = domTree.createElement("arm:AnalysisResult")
                Node3_AnalysisResult.setAttribute("OID", "AR." + ID + "." + each_data[3])
                Node3_AnalysisResult.setAttribute("ParameterOID", "IT." + each_data[5])
                Node3_AnalysisResult.setAttribute("AnalysisReason", each_data[7])
                Node3_AnalysisResult.setAttribute("AnalysisPurpose", each_data[8])

                Node4_Description = domTree.createElement("Description")
                Node5_TranslatedText = domTree.createElement("TranslatedText")
                Node5_TranslatedText.setAttribute("xml:lang", "en")
                Node6_Text = domTree.createTextNode(each_data[4])
                Node5_TranslatedText.appendChild(Node6_Text)
                Node4_Description.appendChild(Node5_TranslatedText)

                Node4_AnalysisDatasets = domTree.createElement("arm:AnalysisDatasets")
                dss = []
                if "JOIN" in each_data[9]:
                    join = ""
                    for ds in each_data[9].split("JOIN"):
                        join += "-" + ds.strip().split()[0]
                        dss.append(ds.strip().split()[0])
                    Node4_AnalysisDatasets.setAttribute("def:CommentOID", "COM.JOIN" + join)
                else:
                    dss.append(each_data[9].strip().split()[0])
                for dataset in dss:
                    Node5_AnalysisDataset = domTree.createElement("arm:AnalysisDataset")
                    Node5_AnalysisDataset.setAttribute("ItemGroupOID", "IG." + dataset)
                    Node6_WhereClauseRef = domTree.createElement("def:WhereClauseRef")
                    Node6_WhereClauseRef.setAttribute("WhereClauseOID", "WC." + ID + "." + each_data[3] + "." + dataset)
                    Node5_AnalysisDataset.appendChild(Node6_WhereClauseRef)
                    Node4_AnalysisDatasets.appendChild(Node5_AnalysisDataset)

                    for avb in each_data[6].split():
                        if dataset == avb.split(".")[0]:
                            Node6_AnalysisVariable = domTree.createElement("arm:AnalysisVariable")
                            Node6_AnalysisVariable.setAttribute("ItemOID", "IT." + avb)
                            Node5_AnalysisDataset.appendChild(Node6_AnalysisVariable)

                Node4_Doc_SAP = domTree.createElement("arm:Documentation")
                Node5_Description = domTree.createElement("Description")
                Node6_TranslatedText = domTree.createElement("TranslatedText")
                Node6_TranslatedText.setAttribute("xml:lang", "en")
                Node7_Text = domTree.createTextNode(each_data[10])
                Node6_TranslatedText.appendChild(Node7_Text)
                Node5_Description.appendChild(Node6_TranslatedText)
                Node4_Doc_SAP.appendChild(Node5_Description)

                Node5_DocumentRef = domTree.createElement("def:DocumentRef")
                Node5_DocumentRef.setAttribute("leafID", "LF.SAP-SEC-" + each_data[11].split()[2].strip())
                Node6_PDFPageRef = domTree.createElement("def:PDFPageRef")
                Node6_PDFPageRef.setAttribute("PageRefs", str(int(each_data[13])))
                Node6_PDFPageRef.setAttribute("Type", "PhysicalRef")
                Node5_DocumentRef.appendChild(Node6_PDFPageRef)
                Node4_Doc_SAP.appendChild(Node5_DocumentRef)

                Node4_ProgrammingCode = domTree.createElement("arm:ProgrammingCode")
                Node4_ProgrammingCode.setAttribute("Context", each_data[14])
                Node5_Code = domTree.createElement("arm:Code")
                Node6_CodeText = domTree.createTextNode(each_data[15])
                Node5_Code.appendChild(Node6_CodeText)
                Node4_ProgrammingCode.appendChild(Node5_Code)
                Node5_DocumentRef_txt = domTree.createElement("def:DocumentRef")
                Node5_DocumentRef_txt.setAttribute("leafID", "LF." + each_data[16].split("txt")[0] + "sas")
                Node6_txtPageRef = domTree.createElement("def:PDFPageRef")
                Node6_txtPageRef.setAttribute("PageRefs", "1")
                Node6_txtPageRef.setAttribute("Type", "PhysicalRef")
                Node5_DocumentRef_txt.appendChild(Node6_txtPageRef)
                Node4_ProgrammingCode.appendChild(Node5_DocumentRef_txt)

                Node3_AnalysisResult.appendChild(Node4_Description)
                Node3_AnalysisResult.appendChild(Node4_AnalysisDatasets)
                Node3_AnalysisResult.appendChild(Node4_Doc_SAP)
                Node3_AnalysisResult.appendChild(Node4_ProgrammingCode)
                Node2_ResultDisplay.appendChild(Node3_AnalysisResult)

        total_len = len(self.path1.text())
        filename_len = len(self.path1.text().split("/")[-1])
        result_xml = self.path1.text()[0:total_len - filename_len]

        with open(result_xml + 'demo.xml', "w", encoding="UTF-8") as f:
            domTree.writexml(f, encoding="UTF-8")
        self.information()

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
# pyinstaller -w -F -i xml.ico -n ARM_Append AK.py