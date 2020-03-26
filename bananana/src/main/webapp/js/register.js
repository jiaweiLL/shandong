$(function () {

    $("#loginBtn").click(function () {
        $.post(
            "sys?method=register",
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
                    location.href="Login.html" ;
                }
            }
        );

    });
})
