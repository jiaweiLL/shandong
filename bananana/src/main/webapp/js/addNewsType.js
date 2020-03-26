$(function () {

    $("#addNewsTypeBtn").click(function () {
        $.post(
            "../news?method=addNewsType",
            $("#addNewstypeForm").serialize(),
            function (responseData) {
                console.log(responseData)
                var resultObj = JSON.parse(responseData);
                alert(resultObj.errorMsg);
                if (resultObj.errorCode == 0){
                    location.href = "admin/ManagerIndex.html";
                }

            }
        );

    });
})
