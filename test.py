from flask import Flask, render_template, request, jsonify
from markupsafe import Markup
from flask_socketio import SocketIO
from api import askclaude,reserMessages 
from DBlink import initDB,getArticleContent,getArticleList
import time
app = Flask(__name__)
initDB()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# 存储在线用户的字典
online_users = {}

@app.route('/chat/<param>')
def index(param):
    return render_template('chat.html',User_scenario=param)

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/info/<param>')
def info(param):
    try:
        data = getArticleContent(name=param)[0]
        return render_template('info.html',data=Markup(data))
    except Exception as e:
        print(e)
        return "404"

@app.route('/undergraduate')
def undergraduate():
    return render_template('undergraduate.html',
                announcement= getArticleList('under_notice',5,length_limit=False),
                art = getArticleList('under_art', 4),
                sport = getArticleList('under_sport', 4),
                CEA = getArticleList('under_CEA', 4),
                special = getArticleList('under_special',4)
                
                )
@app.route('/undergraduate/<param>')
def infoUndergraduateParam(param):
    try:
        return render_template('infoUnder.html', 
                type='under_'+param,
                announcement = getArticleList(article_type='under_' + param,length_limit=False)
                )
    except Exception as e:
        print(e)
        return "404"

@app.route('/reader/<param>')
def reader(param):
    try:
        data=list(getArticleContent(id = param))
        data[0] = Markup(data[0])
        return render_template('reader.html', data=data)
    except Exception as e:
        print(e)
        return "404"
@app.route('/postgraduate')
def postgraduate():
    return render_template('postgraduate.html',
                documents=getArticleList('post_documents', 5 , length_limit=False),
                notice = getArticleList("post_notice", 5 , length_limit=False),
                noexam = getArticleList("post_noexam", 5, length_limit=False)
                )
@app.route('/postgraduate/<param>')
def infoPostgraduateParam(param):
    try:
        return render_template('infoPost.html', 
                type='post_'+param,
                announcement = getArticleList(article_type='post_' + param,length_limit=False)
                )
    except Exception as e:
        print(e)
        return "404"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    reserMessages()
    print('Client disconnected')
#====================================
#
# 这个函数是用于处理客户端发送的消息的。当客户端发送消息时,会触发'message'事件,这个函数就会被调用。
#
# 函数的主要功能如下:
# 1. 打印接收到的消息,并显示消息的来源是'Undergraduate'
# 2. 获取当前客户端的会话ID(session ID)
# 3. 将接收到的消息转换为Python对象(使用eval()函数)
# 4. 发送'New_conversation'事件,通知客户端有新的对话开始
# 5. 发送'RecieveMessage'事件,将接收到的消息发送给当前客户端
# 6. 发送'New_conversation'事件,通知客户端对话已发送
# 7. 调用'askclaude'函数,传递接收到的消息、socketio对象、当前客户端的会话ID和消息的角色(role)
#
#====================================
@socketio.on('message')
def handle_under_message(data):
    print('Received message' + data)
    user_sid = request.sid 
    request_message = eval(data)
    print(request_message)  
    socketio.emit('New_conversation','user',room=user_sid)
    socketio.emit('RecieveMessage', request_message['message'],room=user_sid)  
    socketio.emit('New_conversation','sent',room=user_sid)
    res = askclaude(request_message['message'], socketio,user_sid,request_message['role'])
    print(res)
    
if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",allow_unsafe_werkzeug=True )
