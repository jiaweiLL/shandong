var code ; //在全局定义验证码
//产生验证码
window.onload = function createCode(){
    code = "";
    var codeLength = 4;//验证码的长度
    var checkCode = document.getElementById("checkCode");
    var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
        'S','T','U','V','W','X','Y','Z');//随机数
    for(var i = 0; i < codeLength; i++) {//循环操作
        var charIndex = Math.floor(Math.random()*36);//取得随机数的索引
        code += random[charIndex];//根据索引取得随机数加到code上
    }
    checkCode.value = code;//把code值赋给验证码
}
//校验验证码
function validate(){
    var inputCode = document.getElementById("input").value.toUpperCase(); //取得输入的验证码并转化为大写
    if(inputCode.length <= 0) { //若输入的验证码长度为0
        alert("请输入验证码！"); //则弹出请输入验证码
    }
    else if(inputCode != code ) { //若输入的验证码与产生的验证码不一致时
        alert("验证码输入错误！"); //则弹出验证码输入错误
        // createCode();//刷新验证码
    }
    else { //输入正确时
        $(function(){
            $.post(
                "sys?method=logincheck",
                $("#loginForm").serialize() ,
                function(responseData) {
                    console.log(responseData) ;
                    // 转换为js对象
                    var resultObj = JSON.parse(responseData) ;
                    var str="";
                    $("[name='rem']").each(function(){
                        str+=$(this).val();
                    })
                    // $("#dd").val(str)
                    if(null!=str){
                        if(resultObj.result!=null) {
                            localStorage.setItem("username", resultObj.result.sysname);
                            localStorage.setItem("userpass", resultObj.result.syspass);
                        }
                    }
                    alert(resultObj.errorMsg) ;
                    if(resultObj.errorCode == 0) {

                        var sys = "系统管理员";
                        var user="普通用户";
                        var role=resultObj.result.role;
                        // console.log(role==user);
                        // 将登录管理员信息保存到SessionStorage或者Cookie
                        sessionStorage.setItem("loginuser" , JSON.stringify(resultObj.result)) ;
                        if(role==sys){
                            location.href="admin/ManagerIndex.html" ;
                        }else{
                            location.href="User/Main.html" ;
                        }

                    }
                }
            );
        })
        // alert("^-^"); //弹出^-^
    }
}