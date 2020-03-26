$(function(){
    $("#upBtn").click(function(){
        var formData = new FormData($("#upForm2")[0]);
        $.ajax({
            url:'../sys?method=uploadSys',
            dataType:'json',
            type:'POST',
            async: false,
            data : formData ,
            contentType : false,
            processData : false ,
            success : function(data) {
                alert(data.errorMsg) ;
                if(data.errorCode == 0) {
                    var url = data.result.url;
                    //location.href = url;
                    $("#showPhoto").attr("src", url) ;
                }
            } ,
            error : function(data) {
                // 请求失败，回调该函数
            }
        });
    });
})