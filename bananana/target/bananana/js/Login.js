$(function () {

    $("#loginBtn").click(function () {
            $.post(
                "sys/admin?method=logincheck",
                $("#loginForm").serialize(),
                function (responseData) {
                    console.log(responseData)
                    var resultObj = JSON.parse(responseData);
                    alert(resultObj.errorMsg);
                    if (resultObj.errorCode == 0){
                        if(!$('#rem').is(':checked')) {
                            localStorage.removeItem("sysname");
                            localStorage.removeItem("syspass");
                        }else{
                            var sysname = $("#sysname").val();
                            var syspass = $("#syspass").val();
                            localStorage.setItem("sysname",sysname);
                            localStorage.setItem("syspass",syspass);
                        }

                        sessionStorage.setItem("loginuser",JSON.stringify(resultObj.result));
                        location.href = "admin/ManagerIndex.html";
                    }

                }
            );

    });
})
