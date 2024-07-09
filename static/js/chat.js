
var socket = io.connect('http://' + document.domain + ':' + location.port);
var pointer_to_add;
var Generating = false;
    socket.on('New_conversation', function(role) 
    { // 添加事件名称和回调函数
        // 获取要添加内容的父元素
        if(role == "sent")
        {
            var submitButton = document.getElementById('sendButton');
            submitButton.disabled = true;
            Generating = true;
            var messagesDiv = document.getElementById("messages");

            // 创建新的 div 元素
            var newMessageDiv = document.createElement("div");
            newMessageDiv.className = "message d-flex mb-4";

            // 创建头像元素
            var avatarDiv = document.createElement("div");
            avatarDiv.className = "text-left pr-1";
            var avatarImg = document.createElement("img");
            avatarImg.src = "/static/logo.png";
            avatarImg.width = "30";
            avatarImg.className = "img1";
            avatarDiv.appendChild(avatarImg);
            newMessageDiv.appendChild(avatarDiv);

            // 创建消息内容元素
            var contentDiv = document.createElement("div");
            contentDiv.className = "pr-2 pl-1";
            var nameSpan = document.createElement("span");
            nameSpan.className = "name";
            nameSpan.textContent = role;
            pointer_to_add = document.createElement("p");
            pointer_to_add.className = "msg";
            pointer_to_add.textContent = "";
            contentDiv.appendChild(nameSpan);
            contentDiv.appendChild(pointer_to_add);
            newMessageDiv.appendChild(contentDiv);

            // 将新创建的元素添加到父元素中
            messagesDiv.appendChild(newMessageDiv);
        }
        else
        {
            var messagesDiv = document.getElementById("messages");

            // 创建新的 div 元素
            var newMessageDiv = document.createElement("div");
            newMessageDiv.className = "d-flex align-items-center text-right justify-content-end ";

            // 创建头像元素
            var avatarDiv = document.createElement("div");
            var avatarImg = document.createElement("img");
            avatarImg.src = "/static/user.png";
            avatarImg.width = "30";
            avatarImg.className = "img1";
            avatarDiv.appendChild(avatarImg);
            

            // 创建消息内容元素
            var contentDiv = document.createElement("div");
            contentDiv.className = "pr-2";
            var nameSpan = document.createElement("span");
            nameSpan.className = "name";
            nameSpan.textContent = role;
            pointer_to_add = document.createElement("p");
            pointer_to_add.className = "msg";
            pointer_to_add.textContent = "";
            contentDiv.appendChild(nameSpan);
            contentDiv.appendChild(pointer_to_add);
            newMessageDiv.appendChild(contentDiv);
            newMessageDiv.appendChild(avatarDiv);
            // 将新创建的元素添加到父元素中
            messagesDiv.appendChild(newMessageDiv);
            

        }

    });
    socket.on('RecieveMessage', function(data) {
        pointer_to_add.innerHTML += data;
        var element = document.getElementById('messages');
        element.scrollTop = element.scrollHeight;
});
    socket.on('endOfMessage', function(data){
        Generating = false;
        pointer_to_add.innerHTML = data;
        var element = document.getElementById('messages');
        element.scrollTop = element.scrollHeight;
    });

function sendMessage(role) {
   var message = document.getElementById("message_input").value;
   let dictionary = { role: role, message: message };
   let formattedJson = JSON.stringify(dictionary, null, 2);
   socket.emit('message', formattedJson);
   document.getElementById("message_input").value = '';
   var element = document.getElementById('messages');
   element.scrollTop = element.scrollHeight;
            
}
function checkInput() {
    var inputField = document.getElementById('message_input');
    var submitButton = document.getElementById('sendButton');
    
    if (inputField.value.trim() === '' || Generating) {
      submitButton.disabled = true;
    } else {
      submitButton.disabled = false;
    }
  }