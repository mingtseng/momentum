import difflib

d = difflib.HtmlDiff()
with open(r"D:\users\zengming\Desktop\python\demo.xml", "r", encoding="utf-8") as f:
    text1_lines = f.readlines()
with open(r"D:\Users\zengming\Desktop\awaw.xml", "r", encoding="utf-8") as f:
    text2_lines = f.readlines()

htmlContent = d.make_file(text2_lines, text1_lines)

with open("a.html", "w", encoding="utf-8") as f:
    f.write(htmlContent)

