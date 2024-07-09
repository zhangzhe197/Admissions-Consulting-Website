import requests
from bs4 import BeautifulSoup
import os

# 定义要下载PDF文件的页面链接
url = 'https://gs.upc.edu.cn/2022/0922/c15226a384890/page.psp'

# 发送HTTP请求并获取页面内容
response = requests.get(url)
print(response.text)
soup = BeautifulSoup(response.content, 'html.parser')

# 在页面中查找所有的链接标签<a>，并提取其中的href属性值
pdf_links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href is not None and href.endswith('.pdf'):
        pdf_links.append("https://gs.upc.edu.cn/" + href)

# 创建一个目录用于保存下载的PDF文件
if not os.path.exists('downloaded_pdfs'):
    os.makedirs('downloaded_pdfs')

# 下载所有的PDF文件
for pdf_link in pdf_links:
    pdf_filename = pdf_link.split('/')[-1]  # 从链接中提取文件名
    pdf_path = os.path.join('downloaded_pdfs', pdf_filename)
    pdf_response = requests.get(pdf_link)
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(pdf_response.content)
        print(f'{pdf_filename} 下载完成')

print('所有PDF文件下载完成')
