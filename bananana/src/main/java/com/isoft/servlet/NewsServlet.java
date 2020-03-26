package com.isoft.servlet;

import com.isoft.bean.Page;
import com.isoft.bean.ServerResult;
import com.isoft.entity.News;
import com.isoft.entity.NewsType;
import com.isoft.entity.Sys;
import com.isoft.service.NewsService;
import com.isoft.util.JsonUtil;
import com.isoft.util.StringUtil;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/news")
public class NewsServlet extends HttpServlet {
    private NewsService newsService;
    public NewsServlet(){
        this.newsService=new NewsService();
    }
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        doGet(request,response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String args=request.getParameter("method");
        switch (args){
            case "addNewsType":
                addNewsType(request,response);
                break;
            case "showNewsType":
                showNewsType(request,response);
                break;
            case "AddNews":
                AddNews(request,response);
                break;
            case "showNews" :
                showNews(request,response);
                break;
            default:
                break;
        }
    }
    public void addNewsType(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String typename=request.getParameter("typename");
        String desc=request.getParameter("desc");
        Integer rs=newsService.addNewsType(typename,desc);
        Map<String,Object> map=new HashMap<>();
        int errorCode;
        String errorMsg;
        if(rs==-1||rs==null){
            errorCode=1;
            errorMsg="add defeat";
        }else{
            errorCode = 0 ;
            errorMsg = "add seccess!" ;
        }
        map.put("errorCode" , errorCode) ;
        map.put("errorMsg" , errorMsg) ;
        System.out.println(1);
        response.getWriter().print(JsonUtil.obj2JsonStr(map));
    }
    public void showNewsType(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Page<NewsType> pageInfo=newsService.selectnewstype();
        Map<String , Object> map = new HashMap<>() ;
        int errorCode ;
        String errorMsg ;

        ServerResult serverResult=new ServerResult();
        serverResult.setErrorCode(0);
        serverResult.setErrorMsg("成功");
        serverResult.setResult(pageInfo);
        System.out.println(2);
        response.getWriter().print(JsonUtil.obj2JsonStr(serverResult));
    }
    public void showImg(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String str=request.getParameter("title");
        response.getWriter().print(str);
    }
    public void AddNews(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Integer typeid=Integer.parseInt(request.getParameter("id"));
        String title=request.getParameter("title");
        String content=request.getParameter("content");
        Date adddatetime=new Date();
        Integer rs=newsService.addnews(typeid,title,content,adddatetime);
        Map<String,Object> map=new HashMap<>();
        int errorCode;
        String errorMsg;
        if(rs==-1||rs==null){
            errorCode=1;
            errorMsg="add defeat";
        }else{
            errorCode = 0 ;
            errorMsg = "add seccess!" ;
        }
        map.put("errorCode" , errorCode) ;
        map.put("errorMsg" , errorMsg) ;
        System.out.println(3);
        response.getWriter().print(JsonUtil.obj2JsonStr(map));

    }
    protected void showNews(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String page=request.getParameter("page");
        String size=request.getParameter("size");
        String titleKey=request.getParameter("titleKey");
        String typeId=request.getParameter("typeId");
        Integer typeInt , pageInt , sizeInt ;
        typeInt = pageInt = sizeInt = null ;
        try{
            if (!StringUtil.isEmpty(typeId)) {
                typeInt = StringUtil.str2Int(typeId);
            }
            if (!StringUtil.isEmpty(page)) {
                pageInt = StringUtil.str2Int(page);
            }
            if (!StringUtil.isEmpty(size)){
                sizeInt= StringUtil.str2Int(size);
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        Page<News> pageInfo=newsService.Allnews(titleKey,typeInt,pageInt,sizeInt);
        ServerResult serverResult=new ServerResult();
        serverResult.setErrorCode(0);
        serverResult.setErrorMsg("成功");
        serverResult.setResult(pageInfo);
        response.getWriter().print(JsonUtil.obj2JsonStr(serverResult));
    }

}
