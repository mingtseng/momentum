import time
from docx2pdf import convert
start = time.perf_counter()
convert('word/', 'pdf/')
end = time.perf_counter()
interval = end - start
print("Word文档转换成PDF的时间间隔是:{:.1f}s".format(interval))
