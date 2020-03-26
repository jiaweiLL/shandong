
$(function(){
    var pageCount;
    $.post(
        "../sys?method=getpay" ,
        function(reqData){
            console.log(reqData) ;
            parsePage(reqData) ;
        }
    );

})


function parsePage(pageInfo) {
    var string=pageInfo.split(" ");
    var str="";
    var money=0;
    var i=0;
    while(i<string.length){
        str += "<tr>";
        str += "<td>数量" +string[i]+ "</td>" ;
        money=money+Number(string[i])*120;
        i=i+1;
        str += "<td><img src=http://localhost:8090/bananana/img/" +string[i]+ "></td>" ;
        str +="</tr>" ;
        // str+=string[i];
        i=i+1;
    }

    $("#money").html(money);
    $("#showtype").html(str) ;
}