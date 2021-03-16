//Query Parameter Changer.
const friends = document.getElementsByClassName("friend-list");
for(var i = 0; i < friends.length; i++){
    friends[i].addEventListener("click", function() {
        const x = this.getAttribute("data-friendname")
        console.log(x);
        value = 'http://'+ location.host + window.location.pathname + '?recipient='+x;
        this.setAttribute("href", value)
})}

//Loading SVG
person=`<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
  <path fill="white" d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
  <path fill="white" fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
</svg>`

//Socket Connection Establisher
const sender = JSON.parse(document.getElementById('sender').textContent);
const recipient = JSON.parse(document.getElementById('recipient').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
console.log('ws://' + window.location.host + '/apps/ws/chat/' + username + '/?recipient=' + recipient)
const chatSocket = new WebSocket('ws://' + window.location.host + '/apps/ws/chat/' + username + '/?recipient=' + recipient);


//Textbox Clear
document.querySelector('#send').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    if (message.trim()!=""){
        chatSocket.send(JSON.stringify({
        'message': message,
        'sender': sender,
        'recipient': recipient
        }));
    }else{return false}

    messageInputDom.value = '';
};

//On Message
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)

    console.log(data.sender, sender)
    if (data.sender==sender){
        $("#chat-messages").append(`<div class="chat-message-right mb-4">
                                       <div class='mt-2'>
                                          ${person}
                                          <div class="text-muted small text-nowrap mt-2">2:43 am</div>
                                       </div>
                                       <div class="chat-box flex-shrink-1 text-dark bg-success rounded py-2 px-3 mr-3  rounded">
                                          <div class="font-weight-bold text-right">@${data.sender}</div>
                                          <span id="your-text">${data.message}</span>
                                       </div>
                                    </div>`)
    }
    else{$("#chat-messages").append(`<div class="chat-message-left mb-4">
                                       <div class='mt-2'>
                                          ${person}
                                          <div class="text-muted small text-nowrap mt-2">2:43 am</div>
                                       </div>
                                       <div class="chat-box flex-shrink-1 text-dark bg-info rounded py-2 px-3 ml-3 rounded">
                                           <div class="font-weight-bold">@${data.sender}</div>
                                           <span id="friend-text" class="">${data.message}</span>
                                       </div>
                                   </div>`)
    }

    //Scroll to the bottom of the chatbox to display newest messages
    var elem = document.getElementById('chat-messages');
    elem.scrollTop = elem.scrollHeight;
    console.log("Worked")
}

//Preventing Default submit Behaviour
document.getElementById("send").addEventListener("click", function(event){
  event.preventDefault()
});
