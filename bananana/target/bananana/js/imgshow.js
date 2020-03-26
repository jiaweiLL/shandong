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
    var strImg = "" ;
    var order = 0 ;
    strImg+= "<tr >" ;
    $.each(page.data , function(index , item){
        order++ ;
        str += "<tr>" ;

        str += "<td bgcolor='aqua'>" + "公告</td>" ;
        var ss=item.content;

        if(ss.length>11){
            ss=ss.substr(0,11);
            str += "<td>" + ss+ "</td>" ;
        }else{

            str += "<td>" + item.content + "...</td>" ;
        }
        if(order>4){
            // strImg += "<td align='center'><img src=http://localhost:8090/bananana/img/" + item.title + "><br>商品"+order+"</td>" ;
            // strImg+= "</tr>" ;
        }else{
            strImg += "<td align='center' ><a href='http://localhost:8090/bananana/User/shop.html?title="+item.title+"'><img src=http://localhost:8090/bananana/img/" + item.title + "><br>商品"+order+"</a></td>" ;
        }

        str + "</tr>" ;
    }) ;

    strImg+= "</tr>" ;
    $("#NewsBody").html(str) ;
    $("#NewsBody1").html(strImg) ;
}