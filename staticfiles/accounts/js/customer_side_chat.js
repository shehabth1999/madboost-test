// ######################################### Toggle Function #########################################
const buttons = {
    AdminsChat: document.querySelector('#AdminsChatButton'),
    BoosterChat: document.querySelector('#BoosterChatButton'),
};
const contents = {
    AdminsChat: document.querySelector('#AdminsChatContent'),
    BoosterChat: document.querySelector('#BoosterChatContent'),
};

function toggleContent(content) {
    for (const key in contents) {
        contents[key].style.display = key === content ? contents[key].style.display = 'block' : contents[key].style.display = 'none'
    }
}

// Toggle click event
function setupButtonClickEvent(button, content) {
    button.addEventListener('click', function () {
        toggleContent(content);
        scrollToBottom();
        admins_scrollToBottom();

        for (const key in buttons) {
            buttons[key].classList.remove('clicked_button');
        }
        button.classList.add('clicked_button');
        console.log('click')
    });
}

// Setup click events for each button
for (const key in buttons) {
    setupButtonClickEvent(buttons[key], key);
}


// ######################################### Chats #########################################
const user = JSON.parse(document.getElementById('user').textContent);
const admin_room = JSON.parse(document.getElementById('admin_room').textContent);
const booster_room_name = JSON.parse(document.getElementById('booster_room_name').textContent)

// ################ Admins Chat 
const admins_chatbox = document.querySelector("#chat-admin-container");
// Function to scroll to the bottom of the admins_chatbox
function admins_scrollToBottom() {
    admins_chatbox.scrollTop = admins_chatbox.scrollHeight;
}
admins_scrollToBottom();

const admins_roomName = JSON.parse(document.getElementById('admins_chat_slug').textContent);
const adminsChatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + admins_roomName + "/");

adminsChatSocket.onopen = function (e) {
    console.log("The connection was setup successfully adminsChatSocket!");
};
adminsChatSocket.onclose = function (e) {
    console.log("Something unexpected happened adminsChatSocket!");
};

document.querySelector("#admins_my_input").focus();
document.querySelector("#admin_chat_form").addEventListener("submit", function (e) {
    e.preventDefault();
});
document.querySelector("#admins_my_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        document.querySelector("#admins_submit_button").click();
    }
};
document.querySelector("#admins_submit_button").onclick = function (e) {
    var admins_messageInput = document.querySelector(
        "#admins_my_input"
    ).value;

    if (admins_messageInput.length == 0) {
        alert("Add some Input First Or Press Send Button! adminsChatSocket")
    }
    else {
        adminsChatSocket.send(JSON.stringify({ message: admins_messageInput, username: user, room_name: admin_room }));
    }

};

adminsChatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    $('.noMessageAdmin').html('');
    var div = document.createElement("div");
    console.log(e.data);
    div.innerHTML = `
    <div class="message p-3 rounded-3 ">
        <p class="content mb-1">${data.message}</p>
        <p class="text-end mb-1" style="font-size: 10px; color:#ffffffbf">Just Now</p>
    </div>
    `
    // Add class based on user authentication
    if (data.username === user) {
        div.classList.add("admins_chat_message", "userMessage");
    } else {
        div.classList.add("admins_chat_message", "otherMessage");
    }

    document.querySelector("#admins_my_input").value = "";
    document.querySelector("#admins_chatbox").appendChild(div);
    admins_scrollToBottom();
};

// ################ Booster Chat 
const chatbox = document.querySelector(".chat-customer-container");
// Function to scroll to the bottom of the chatbox
function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
}
scrollToBottom();


const roomName = JSON.parse(document.getElementById('room_slug').textContent);
const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomName + "/");
// const chatSocket = new WebSocket("ws://127.0.0.1:8000/ws/"+ roomName +"/");
// alert(chatSocket);
chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
};
chatSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
};

document.querySelector("#my_input").focus();
document.querySelector("#booster_chat_form").addEventListener("submit", function (e) {
    e.preventDefault();
});
document.querySelector("#my_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        document.querySelector("#submit_button").click();
    }
};
document.querySelector("#submit_button").onclick = function (e) {
    var messageInput = document.querySelector(
        "#my_input"
    ).value;

    if (messageInput.length == 0) {
        alert("Add some Input First Or Press Send Button!")
    }
    else {
        chatSocket.send(JSON.stringify({ message: messageInput, username: user, room_name: booster_room_name }));
    }

};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    $('.noMessageBooster').html('')
    var div = document.createElement("div");
    
    if(data.username === user){
        div.innerHTML = `
        <div class="message p-3 rounded-3 ">
            <p class="content mb-1">${data.message}</p>
            <p class="text-end mb-1" style="font-size: 10px; color:#ffffffbf">Just Now</p>
        </div>
        `
    }
    else{
        const booster_first_name = JSON.parse(document.getElementById('booster_first_name').textContent);
        const booster_last_name = JSON.parse(document.getElementById('booster_last_name').textContent);
        const booster_image = JSON.parse(document.getElementById('booster_image').textContent);

        if (booster_image){
            console.log('booster image')
            div.innerHTML = `
            <div class="image">
                <img src="${booster_image}" alt="" width="40" height="40">
            </div>
            <div class="message p-3 rounded-3 ">
                <p class="username mb-1">
                ${booster_first_name} ${booster_last_name}
                </p>
                <p class="content mb-1">${data.message}</p>
                <p class="text-end mb-1" style="font-size: 10px; color:#ffffffbf">Just Now</p>
            </div>
            `
        }
        else{
            console.log('no booster image')
            div.innerHTML = `
            <div class="image">
                <img src="${staticUrl}" alt="" width="40" height="40">
            </div>
            <div class="message p-3 rounded-3 ">
                <p class="username mb-1">
                ${booster_first_name} ${booster_last_name}
                </p>
                <p class="content mb-1">${data.message}</p>
                <p class="text-end mb-1" style="font-size: 10px; color:#ffffffbf">Just Now</p>
            </div>
            `
        }
    }

    // Add class based on user authentication
    if (data.username === user) {
        if (data.message.msg_type == 2) {
            div.classList.add("tip-message");
        } else {
            div.classList.add("chat-message", "userMessage");
        }
    } else {
        div.classList.add("chat-message", "otherMessage");
    }
    

    document.querySelector("#my_input").value = "";
    document.querySelector("#chatbox").appendChild(div);
    scrollToBottom();
};