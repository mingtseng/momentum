from bs4 import BeautifulSoup
import re
from urllib import request
import urllib
import xlwt

find_name = re.compile(r'<h2 class="champion_name">(.*?)</h2>')
find_title = re.compile(r'<h3 class="champion_title">(.*?)</h3>')
find_intro = re.compile(r'<p>(.*?)</p>')
find_tags = re.compile(r'<span class="champion_tooltip_tags">Tags:(.*?)</span>')

def main():
    url = 'http://lol.qq.com/web200912/hero_list.htm'
    html = get_html(url)
    data = parse_html(html)
    save_data(data)

def get_html(url):
    # header = {User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36}
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = ""
    html = response.read().decode('ANSI')
    return html

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find(name='div', class_="cm_bg")
    data = []
    name = re.findall(find_name, str(info))
    for each_name in name:
        data.append(each_name)
    title = re.findall(find_title, str(info))
    for each_title in title:
        data.append(each_title)
    intro = re.findall(find_intro, str(info))
    for each_intro in intro:
        data.append(each_intro)
    tags = re.findall(find_tags, str(info))
    for each_tags in tags:
        data.append(each_tags)

    return data

def save_data(data):
    workbook = xlwt.Workbook(encoding='UTF-8')
    worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    index = ["英雄名", "英雄称号", "英雄介绍", "英雄属性"]
    count = 0
    for i in range(0, 4):
        worksheet.write(0, i, index[i])
    for j in range(0, 4):
        for k in range(1, 41):
            worksheet.write(k, j, data[count])
            count += 1
    workbook.save("英雄概括.xls")


if __name__ == '__main__':
    main()


