from pathlib import Path
from openai import OpenAI
import re,json,os
import pandas as pd
from io import StringIO
from tqdm import tqdm
import time
client = OpenAI(
    api_key="PUT YOUR API HERE",
    base_url="https://api.moonshot.cn/v1"
)
df = pd.DataFrame(columns=['专业类别名称','专业介绍'])
detail_df = pd.DataFrame(columns=['培养方向名称','特色与优势','专业类别名称'])
def summary_pdf(PDFfile, cnt):
    global df,detail_df
    print("uploading files " + PDFfile)
    file = client.files.create(file=Path(PDFfile),purpose="file-extract")
    file_content = client.files.content(file_id=file.id).text
    return file_content
    print("end uploading")
    content = eval(file_content)["content"]
    message1 = [
        {
            "role" : "system",
            "content" : content
        },
        {
            "role" : "user",
            "content" : '''
            总结文件.  使用csv格式, 总结文件的专业介绍部分. 尽量详细使用原文的表达
            文件格式如下:
            专业类别名称,专业介绍

        
    '''
        }
    ]

    message2 = [
        {
            "role" : "system",
            "content" : content
        },
        {
            "role" : "user",
            "content" : '''
            总结文件.  使用csv格式, 总结文件的培养方向部分. 尽量详细使用原文的表达
            文件格式如下:
            培养方向名称, 特色与优势, 专业类别名称

            补充: 专业类别名称是整个文件的正文第一行

        
    '''
        }
    ]
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=message1,
        temperature=0.1
    )
    detail_AM =json.loads(completion.model_dump_json())['choices'][0]['message']['content']
    new_df = pd.read_csv(StringIO(detail_AM))
    new_df.to_csv(f"./csvs/data_PM{cnt}.csv")
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=message2,
        temperature=0.1
    )
    detail_AM1 =json.loads(completion.model_dump_json())['choices'][0]['message']['content']
    new_df = pd.read_csv(StringIO(detail_AM1))
    new_df.to_csv(f"./csvs/data_PM_DE{cnt}.csv")


# folder_path = "./downloaded_pdfs"

# files = os.listdir(folder_path)
# failed = []
# print(files)
# for i, name in enumerate(tqdm(files[6:])):
#     try:
#         summary_pdf(name,i + 6)
#         time.sleep(25)
#     except Exception as e :
#         print(e)
#         failed.append(name)
# for line in failed:
#     print(line)
file = open("res.txt", 'w')
file.write(summary_pdf("./第一张.pdf",0))
file.close()
