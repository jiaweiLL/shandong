package com.isoft.servlet;



import com.isoft.bean.Page;
import com.isoft.bean.ServerResult;
import com.isoft.entity.News;
import com.isoft.entity.Sys;
import com.isoft.entity.shop;
import com.isoft.service.SysService;
import com.isoft.util.FileUtil;
import com.isoft.util.JsonUtil;
import com.isoft.util.StringUtil;

import javax.servlet.ServletException;
import javax.servlet.SessionCookieConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/sys")
public class SysServlet extends HttpServlet {
    private SysService sysService ;
    private static final String UPLOAD_DIRECTORY = "upload";
    public SysServlet() {
        this.sysService = new SysService() ;
    }
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        doGet(request , response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String args=request.getParameter("method");
        switch (args){
            case "logincheck":
                logincheck(request,response);
                break;
            case "clearcheck":
                clearcheck(request,response);
                break;
            case "addSys":
                addSys(request,response);
                break;
            case "ChangePass" :
                ChangePass(request,response);
                break;
            case "uploadSys":
                uploadSys(request,response);
                break;
            case "showSys":
                showSys(request,response);
                break;
            case "ChangeRole":
                ChangeRole(request,response);
                break;
            case "register":
                register(request,response);
                break;
            case "addshop":
                addshop(request,response);
                break;
            case "getpay":
                getpay(request,response);
        }
    }
    protected void logincheck(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name = request.getParameter("sysname") ;
        String pass = request.getParameter("syspass") ;

//        String remanber[]=request.getParameterValues("remanber");
//        System.out.println(remanber[0]);
        Sys sys = sysService.loginCheck(name , pass) ;
        Map<String , Object> map = new HashMap<>() ;
        int errorCode ;
        String errorMsg ;
        if(null == sys) {
            errorCode = 1;
            errorMsg = "login defeat！" ;
        } else {
            errorCode = 0 ;
            errorMsg = "login seccsess！" ;

            // 信息存入Session
            HttpSession session = request.getSession() ;
            String sid=""+sys.getId();
            Cookie cookie = new Cookie("sid", sid);
            Cookie cookie1 = new Cookie("name", name);
            response.addCookie(cookie);
            response.addCookie(cookie1);
            session.setAttribute("loginuser" , sys);
        }
        map.put("errorCode" , errorCode) ;
        map.put("errorMsg" , errorMsg) ;
        map.put("result" , sys) ;
        response.getWriter().print(JsonUtil.obj2JsonStr(map));
    }
    protected void clearcheck(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession() ;
        Cookie cookie[]=request.getCookies();
        if(cookie!=null){
            for(Cookie cookie1:cookie){
                if("name".equals(cookie1.getName())){
                    cookie1.setValue(null);
                    response.addCookie(cookie1);
                }
            }
        }
        session.invalidate();
        response.sendRedirect(request.getContextPath()+"/Login.html");
    }
    protected void addSys(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name = request.getParameter("addsysname") ;
        String pass = request.getParameter("addsyspass") ;
        int rs =sysService.addCheck(name,pass);
//        response.sendRedirect(request.getContextPath()+"/admin/ManagerIndex.html");
        Map<String , Object> map = new HashMap<>() ;
        int errorCode ;
        String errorMsg ;
        if(rs == -1) {
            errorCode = 1;
            errorMsg = " add defeat！" ;
        } else {
            errorCode = 0 ;
            errorMsg = "add seccess!" ;
            // 信息存入Session
        }
        map.put("errorCode" , errorCode) ;
        map.put("errorMsg" , errorMsg) ;
        response.getWriter().print(JsonUtil.obj2JsonStr(map));
    }
    protected void addshop(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name="";
        Cookie cookie[]=request.getCookies();
        if(cookie!=null){
            for(Cookie cookie1:cookie){
                if("name".equals(cookie1.getName())){
                    name=cookie1.getValue();
                }
            }
        }
        String shop = request.getParameter("img") ;
        HttpSession session = request.getSession();
//        int num=session.getAttribute("num");
        int num=Integer.parseInt(request.getParameter("num"));;
        int rs =sysService.addshop(name,shop,num);
//        response.sendRedirect(request.getContextPath()+"/admin/ManagerIndex.html");
        Map<String , Object> map = new HashMap<>() ;
        int errorCode ;
        String errorMsg ;
        if(rs == -1) {
            errorCode = 1;
            errorMsg = " add defeat！" ;
        } else {
            errorCode = 0 ;
            errorMsg = "add seccess!" ;
            // 信息存入Session
        }
        map.put("errorCode" , errorCode) ;
        map.put("errorMsg" , errorMsg) ;
        response.getWriter().print(JsonUtil.obj2JsonStr(map));
    }
    protected void ChangePass(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Cookie[] cookies=request.getCookies();
        int id=0;
        for(int i=0;i<cookies.length;i++){
            if("sid".equals(cookies[i].getName())){
                id=Integer.parseInt(cookies[i].getValue());
            }
        }
        String pass = request.getParameter("changesyspass") ;
//        pass= MD5Util.MD5(pass);
        int rs =sysService.changepassCheck(id,pass);

        response.sendRedirect(request.getContextPath()+"/admin/ManagerIndex.html");
    }
    protected void uploadSys(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ServerResult serverResult = FileUtil.fileUpload(request , response , UPLOAD_DIRECTORY , new String[]{"name" , "age"}) ;
        System.out.println(serverResult);
        response.getWriter().print(JsonUtil.obj2JsonStr(serverResult));
    }
    protected void showSys(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String page=request.getParameter("page");
        String size=request.getParameter("size");
        String sysname=request.getParameter("sysname");
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


        Page<Sys> pageInfo=sysService.pageDate(sysname,typeInt,pageInt,sizeInt);
        ServerResult serverResult=new ServerResult();
        serverResult.setErrorCode(0);
        serverResult.setErrorMsg("成功");
        serverResult.setResult(pageInfo);
        response.getWriter().print(JsonUtil.obj2JsonStr(serverResult));
    }

    protected void ChangeRole(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Integer id=Integer.parseInt(request.getParameter("id"));
        System.out.println(id);
//        String str=""+id;
//        String role=request.getParameter(str);
        Integer rs =sysService.changeRole(id);
//        response.sendRedirect(request.getContextPath()+"/admin/ManagerIndex.html");
        Map<String , Object> map = new HashMap<>() ;
        int errorCode ;
        String errorMsg ;
        if(rs == -1||rs==null) {
            errorCode = 1;
            errorMsg = " add defeat！" ;
        } else {
            errorCode = 0 ;
            errorMsg = "add seccess!" ;
            // 信息存入Session
        }
        map.put("errorCode" , errorCode) ;
        map.put("errorMsg" , errorMsg) ;
        response.getWriter().print(JsonUtil.obj2JsonStr(map));
        response.sendRedirect("admin/AllSys.html");
    }
    protected void register(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name = request.getParameter("registername") ;
        String pass = request.getParameter("registerpass") ;
        int rs =sysService.register(name,pass);
//        response.sendRedirect(request.getContextPath()+"/admin/ManagerIndex.html");
        Map<String , Object> map = new HashMap<>() ;
        int errorCode ;
        String errorMsg ;
        if(rs == -1) {
            errorCode = 1;
            errorMsg = " register defeat！" ;
        } else {
            errorCode = 0 ;
            errorMsg = "register seccess!" ;
            // 信息存入Session
        }
        map.put("errorCode" , errorCode) ;
        map.put("errorMsg" , errorMsg) ;
        response.getWriter().print(JsonUtil.obj2JsonStr(map));
    }
    protected void getpay(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name="";
        Cookie[] cookies=request.getCookies();
        for(int i=0;i<cookies.length;i++){
            if("name".equals(cookies[i].getName())){
                name=cookies[i].getValue();
            }
        }
        ArrayList<shop> list=new ArrayList<>();
        list=sysService.getpay(name);
        String str="";
        System.out.println(list.size());
        for(int i=0;i<list.size();i++){
            str=str+list.get(i).getNum()+" "+list.get(i).getShop()+" ";
            System.out.println(str);
        }
        str=str.trim();
        response.getWriter().print(str);
    }
}
