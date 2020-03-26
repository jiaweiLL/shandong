var pageParam = 1 ;
var sizeParam = 5 ;
$(function(){
    var pageCount;
    $.post(
        "../news?method=showNews" ,
        {page : pageParam , size : sizeParam},
        function(reqData){
            console.log(reqData) ;
            parsePage(JSON.parse(reqData)) ;
            // pageCountnt=JSON.parse(reqData).result.pageCount;
        }
    );
    $("#aUp").click(function(){
        if(pageParam == 1) {
            return ;
        }
        pageParam -= 1;
        ajaxPage() ;
    });
    $("#aDown").click(function(){
        if(pageParam>pageCount){
            return;
        }
        pageParam += 1;
        ajaxPage();
    })
})

function ajaxPage() {
    $.post(
        "../news?method=showNews" ,
        {page : pageParam , size : sizeParam},
        function(reqData){
            // console.log(reqData) ;
            parsePage(JSON.parse(reqData)) ;
            // pageCount=JSON.parse(reqData).result.pageCount;
        }
    );
}

function parsePage(pageInfo) {
    if(0 != pageInfo.errorCode) {
        return ;
    }
    var page = pageInfo.result ;
    $("#showPage").text(page.page) ;
    $("#showPageCount").text(page.pageCount) ;
    $("#showRowCount").text(page.rowCount) ;
    $("#showSize").text(page.size) ;
    // 表格填充数据
    var str = "" ;
    var order = 0 ;
    $.each(page.data , function(index , item){
        order++ ;
        // console.log(item) ;
        str += "<tr align=center>" ;
        // str += "<td>" + order + "</td>" ;
        // str += "<td>" + item.id + "</td>" ;
        // var content = '' ;
        // var c = item.sysname ;
        // if(null != c && c.length > 0) {
        //     content = c.substr(0 , 10) + "..." ;
        // }
        // str += "<td>" + item.title+ "</td>" ;
        str += "<td>" + item.content + "</td>" ;
        // str+="<td>"+item.adddatetime+"</td>";
        str + "</tr>" ;
    }) ;
    $("#NewsBody").html(str) ;
}