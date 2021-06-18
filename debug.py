import re

fmt = '''
SAE情况{SAE1OUT}@__
     1=死亡
     2=住院或住院时间延长
     3=永久或显著的伤残/功能障碍危及生命
     4=先天性异常/出生缺陷
     5=其他，请详述
SAE发生日期{SAESTDAT}@________(YYYY/MM/DD)
SAE严重程度{SAESEV}@__
     1=轻度      2=中度     3=重度
对试验采取的措施{SAEACN}@__
     1=继续试验   2=观察后继续试验   3=停止试验
SAE转归{SAEOUT}@__
     1=症状消失
     2=症状持续
     3=死亡    
SAE与试验器械的关系{SAEREL}@__
     1=无关
     2=可能无关
     3=可能相关
     4=肯定相关
     5=待评价
     6=无法判定
'''
# pattern = re.compile(r'([^@]+@_+)\s*((?:\d+=[\u4e00-\u9fa5]+\s+)*)', re.S)

pattern = re.compile(r'([^@\s]+)@_+\s*((?:\d+=\S+\s+)+)', re.S)
items = re.findall(pattern, fmt)
fmt = ""
for item in items:
    a = item[1].replace(" ", "")
    v = item[0].split("}")[0].split("{")[1]
    b = re.sub('(\d+)=([\u4e00-\u9fa5 \uff08\uff09\uff0c\u3001]+)',
               lambda x: f'        "{x.group(1)}" = "{x.group(2)}"\n', a)
    c = b.replace("\n\n", "\n")
    k = "    value $ " + v + "_\n" + c + "        ;\n"
    ptn = re.compile("{[A-Z]+}@_+")
    j = ptn.sub("", k).replace("\n\n", "\n")
    fmt += j

print("proc format;\n" + fmt + "run;")





