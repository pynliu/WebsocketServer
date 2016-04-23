window.onbeforeunload = function () {
    try {
        socket.send('quit');
        socket.close();
        socket = null;
        }
    catch (ex) {
        log(ex);
        }
};

function init() {
    var form1 = document.getElementById("form1");
    var log1 = document.getElementById("log1");
    var p1 = document.getElementById("p1");
    var start1 = document.getElementById("start1");
    var close1 = document.getElementById("close1");
    var flush1 = document.getElementById("flush1");

    flush1.style.display = 'none';
    p1.innerHTML = '';

    var host = "ws://192.168.1.11:88/";
    try {
        socket = new WebSocket(host);
        socket.onopen = function (msg) {
            start1.innerHTML='开始';
            close1.innerHTML = '关闭'
            ;
        };
        socket.onmessage = function (msg) {
            log(msg.data);
            if(msg.data=="SUCCESS!"){start1.innerHTML='开始'}
        };
        socket.onclose = function (msg) {
            log("Lose Connection!");
            offline_server();
        };
    }
    catch (ex) {
        log(ex);
    }
}

function begin(obj){
    if (socket==null){init() ; close1.style.display='inline';return};
    app_name = form1.app.value
    selecct_option = form1.option.value
    if (!app_name) {
        alert("Message can not be empty");
        return 1;
    }
    else{obj.innerHTML='Running';log1.innerHTML = '' ;
        flush1.style.display = 'inline'
        p1.innerHTML= selecct_option + ':' + app_name
        p1.style.color="blue"
        send()}
}

function mymessage() {
    alert("加载完成。");
}

function send() {
    msg = app_name + ' ' + selecct_option
    try {
        socket.send(msg);
    } catch (ex) {
        log(ex);
    }
}

function log(msg) {
    log1.innerHTML += "<br>" + msg;
}

function close_websocket() {
    close1.innerHTML = '正在关闭'
    socket.send('quit');
    socket.close();
    socket = null;
}

function offline_server(){
    start1.innerHTML = '连接服务器';
    p1.innerHTML = '连接已经断开！ 点击<连接服务器>重新建立连接'
    disply_switch(flush1)
    disply_switch(close1)
}

function disply_switch(st){
    st.style.display='none'
}

function clear_log(){
            flush1.innerHTML = "刷新成功"
            log1.innerHTML = ''
            setTimeout("flush1.innerHTML = '刷新'", 2000)
        }
