
$(function(){
    var pageCount;
    $.post(
        "../news?method=showNewsType" ,
        function(reqData){
            console.log(reqData) ;
            parsePage(JSON.parse(reqData)) ;
            // pageCountnt=JSON.parse(reqData).result.pageCount;
        }
    );

})

// function ajaxPage() {
//     $.post(
//         "../sys?method=showSys" ,
//         {page : pageParam , size : sizeParam},
//         function(reqData){
//             // console.log(reqData) ;
//             parsePage(JSON.parse(reqData)) ;
//             // pageCount=JSON.parse(reqData).result.pageCount;
//         }
//     );
// }

function parsePage(pageInfo) {
    if(0 != pageInfo.errorCode) {
        return ;
    }
    var page = pageInfo.result ;
    console.log(page.data)
    var str = "" ;
    $.each(page.data , function(index , item){
        console.log(item.typename)
        str += '<option value="'+item.id+'">' +item.typename  + '</option>';
    }) ;
    $("#showtype").html(str) ;
}