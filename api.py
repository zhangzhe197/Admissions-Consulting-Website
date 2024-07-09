import asyncio,os,json,time
from config import init_config, api
from anthropic import AsyncAnthropic
from DBlink import getInfoFromDB
#=========================================================
# 代理, 否则无法访问Claude
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
#=========================================================
AM_sys_world,PM_sys_word ,sys_word = init_config()
messages = []
user_ask = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": ""
        }
    ]
}
additional_info = ""
assistant_reply =  {
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": ""
        }
    ]
}

client = AsyncAnthropic(api_key=api)

#====================================
# stepSysWord函数
# 根据不同角色返回系统词汇或信息
# 参数: role - 角色类型，可以是'under', 'postAM', 'postPM'之一
# 返回值: 根据角色类型返回相应的系统词汇或信息
#====================================
def stepSysWord(role):
    if role == 'under':
        return ("Here are some detailed information about China University of Petroleum (East China) majors" +
            additional_info
             if additional_info.strip() else "") + sys_word 
    elif role == 'postAM':
        return AM_sys_world
    elif role == 'postPM':
        return PM_sys_word
    else :
        return ""
#====================================
# 清除对话记录
#====================================
def reserMessages():
    messages.clear()

#=====================================================================================
# 这是一个异步函数 main，它接受四个参数:
# - user_question: 用户提出的问题
# - socketio: 用于发送消息到客户端的 SocketIO 实例
# - user_id: 用户的唯一标识符
# - role: 指定 AI 助手的角色或个性
# 函数的主要作用是与 Claude AI 模型进行交互,并将响应发送回客户端。
# 1. 首先,它将用户的问题添加到 messages 列表中,该列表用于存储对话历史。
# 2. 然后,它使用 client.messages.stream 异步上下文管理器与 Claude AI 模型进行交互。在这个过程中,它会实时输出 AI 的响应,并通过 SocketIO 将响应发送到客户端。
# 3. 在上下文管理器结束后,它获取 AI 的最终响应,并将其添加到 messages 列表中。
# 4. 最后,它通过 SocketIO 将 AI 的最终响应发送到客户端。
# 该函数使用了异步编程,可以实时地与 AI 模型交互并将响应发送到客户端,提供了良好的用户体验。
#====================================================================================
async def main(user_question,socketio,user_id,role) -> None:
    user_ask["content"][0]["text"] = user_question
    messages.append(user_ask)
    point2 = None
    async with client.messages.stream(
        max_tokens=1024,
        system= stepSysWord(role),
        messages=messages,
        model="claude-3-sonnet-20240229",
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
            if point2 is None: point2 = time.time()
            socketio.emit('RecieveMessage', text.replace("\n","<br>"), room=user_id)
        print()
    # you can still get the accumulated final message outside of
    # the context manager, as long as the entire stream was consumed
    # inside of the context manager
    accumulated = await stream.get_final_message()
    assistant_reply["content"][0]["text"] = json.loads(accumulated.model_dump_json(indent=2))["content"][0]["text"]
    messages.append(assistant_reply)
    socketio.emit('endOfMessage',assistant_reply["content"][0]["text"].replace("\n","<br>") , room=user_id)
    return point2
#====================================
# 调用main函数之前, 使用getInfoFromDB获得数据库中内容, 扩充提示词内容
#====================================
def askclaude(question,socketio,user_id,role):
    
    global additional_info
    try:
        start = time.time()
        data_DB, res = getInfoFromDB(question,role) 
        additional_info += data_DB
        point2 = asyncio.run(main(user_question=question, socketio=socketio,user_id= user_id,role=role))
        return res[0] - start , res[1] - start , point2 - start
    except Exception as e:
        print(e)
        socketio.emit('message',"抱歉, 出现错误, 请您稍后再试, 或者刷新一下页面", room=user_id)

