var pageParam = 1 ;
var sizeParam = 5 ;
$(function(){
    var pageCount;
    $.post(
        "../sys?method=showSys" ,
        {page : pageParam , size : sizeParam},
        function(reqData){
            // console.log(reqData) ;
            parsePage(JSON.parse(reqData)) ;

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
        "../sys?method=showSys" ,
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
        str += "<td>" + order + "</td>" ;
        str += "<td>" + item.id + "</td>" ;
        // var content = '' ;
        // var c = item.sysname ;
        // if(null != c && c.length > 0) {
        //     content = c.substr(0 , 10) + "..." ;
        // }
        str += "<td>" + item.sysname + "</td>" ;
        str += "<td>" + item.syspass + "</td>" ;
        // str+="<td>"+item.role+"</td>";
        if(item.role=="系统管理员"){
            str+="<td><select id='role'><option value='系统管理员' selected>系统管理员</option><option value='普通用户'>普通用户</option> </select> </td>";
        }else{
            str+="<td><select id='role'><option value='系统管理员'>系统管理员</option><option value='普通用户' selected>普通用户</option> </select> </td>";
        }
        str += "<td><a href='../sys?method=ChangeRole&id="+item.id+"'>确认</a> </td>" ;
        // str+="<td><select name='education' id='education1'><option value='系统管理员'>系统管理员</option><option value='普通用户'>普通用户</option> </select> </td>";
        str + "</tr>" ;
    }) ;
    $("#SysBody").html(str) ;

}