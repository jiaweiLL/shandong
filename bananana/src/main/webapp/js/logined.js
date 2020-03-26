$(function() {
    var name = getCookie("name");
    if (name == null) {
        var login = "登录";
        var register = "注册";
        var href1="http://localhost:8090/bananana/Login.html";
        var href2="http://localhost:8090/bananana/register.html";
        var href3="http://localhost:8090/bananana/Login.html";
        changeContent(login,register,href1,href2,href3);
    } else {
        var login = "欢迎" + name;
        var register = "退出";
        var href1="http://localhost:8090/bananana/User/User.html";
        var href2="http://localhost:8090/bananana/sys?method=clearcheck";
        var href1="http://localhost:8090/bananana/User/pay.html";
        changeContent(login,register,href1,href2,href3);
        // changeContent(login);
    }
})

function changeContent(text1,text2,href1,href2,href3) {
    document.getElementById("login").innerHTML = text1;
    document.getElementById("register").innerHTML = text2;
    document.getElementById("login").href=href1;
    document.getElementById("register").href=href2;
    document.getElementById("carshop").href=href3;
}
function getCookie(name) {
    var cookies = document.cookie;
    var list = cookies.split("; ");          // 解析出名/值对列表

    for(var i = 0; i < list.length; i++) {
        var arr = list[i].split("=");          // 解析出名和值
        if(arr[0] == name)
            return decodeURIComponent(arr[1]);   // 对cookie值解码
    }
    return "";
}