import re

study = "csdjrk"
output_type = []
file_type = []
output_number = []
original_output_name = []
population = []
pattern = re.compile(r'[\d+.]+')
with open(file="D:\\Users\\zengming\\Desktop\\新建文本文档.txt", encoding="utf-8", mode="r") as f:
    for line in f:
        if line[0] in ("表", "列", "图"):
            a = re.findall(pattern, line)
            number = "-".join(a[0].split("."))
            output_number.append(number)
            if line[0] == "表":
                Type = "T"
                output_type.append(Type)
                file_type.append("rtf")
            if line[0] == "列":
                Type = "L"
                output_type.append(Type)
                file_type.append("rtf")
            if line[0] == "图":
                Type = "F"
                output_type.append(Type)
                file_type.append("pdf")
            original_output_name.append(study + "-" + Type.lower() + "-" + number)

            text1 = line.split(":")[1].split()[-4].strip()
            text2 = line.split(":")[1].split()[-2].strip()
            # print(text2)
            title = " - ".join([text1, text2])
            population.append(text2)
            print(title)

# print(population)
# for i in file_type:
#     print(i)
# print(len(file_type))
# print(len(output_number))
# print(len(original_output_name))

