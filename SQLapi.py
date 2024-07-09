import anthropic,json,os
from config import api, SQL_config,SQL_PM_config,SQL_AM_config
sys = SQL_config()
sys_PM = SQL_PM_config()
sys_AM = SQL_AM_config()
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=api,
)
def giveSysByRole(role):
    if role == "under": return sys
    elif role == "postPM" :return sys_PM
    elif role == "postAM" : return sys_AM
    else : return " "
#====================================

# 该函数用于生成SQL查询语句。它接受两个参数:
# 1. question: 用户提出的问题
# 2. role: 用户的角色
#
# 函数首先使用Anthropic的Claude-3-haiku-20240307模型创建一个消息对象,并设置以下参数:
# - max_tokens: 生成的最大token数量
# - temperature: 生成文本的随机性程度
# - system: 根据用户的角色设置系统消息
# - messages: 包含用户提出的问题
#
# 最后,函数将模型生成的JSON响应解析为Python字典,并返回其中的"content"字段,即生成的SQL查询语句。
#
#====================================
def getSQL(question, role):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        temperature=1,
        system=giveSysByRole(role),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )
    return json.loads(message.model_dump_json())['content'][0]['text']