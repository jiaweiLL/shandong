$(function () {


    $("#add").click(function () {
        var num = sessionStorage.getItem("num");
        var img= sessionStorage.getItem("img");
        $.post(

            "../sys?method=addshop&num="+num+"&img="+img,
            $("#addshopForm").serialize(),
            function (responseData) {
                console.log(responseData)
                var resultObj = JSON.parse(responseData);
                alert(resultObj.errorMsg);


            }
        );

    });
})