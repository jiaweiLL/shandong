package com.isoft.service;

import com.isoft.bean.Page;
import com.isoft.db.SqlSessionUtil;
import com.isoft.entity.News;
import com.isoft.entity.shop;
import com.isoft.util.MD5Util;
import com.isoft.util.StringUtil;
import com.isoft.dao.SysDao;
import com.isoft.entity.Sys;
import org.apache.ibatis.session.SqlSession;

import java.sql.SQLException;
import java.util.ArrayList;

public class SysService {
    private SysDao sysDao ;
    private SqlSession sqlSession;
    public SysService() {
        this.sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
        sysDao=sqlSession.getMapper(SysDao.class);
    }
    public Sys loginCheck(String name , String pass) {
        if(StringUtil.isEmpty(name) || StringUtil.isEmpty(pass)) {
            return null ;
        }
//        SqlSession sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
//        SysDao sysDao=sqlSession.getMapper(SysDao.class);
        Sys sys = sysDao.logincheck(name , pass) ;

        return sys ;
    }
    public int addCheck(String name,String pass){
        if(StringUtil.isEmpty(name) || StringUtil.isEmpty(pass)) {
            return -1 ;
        }
//        SqlSession sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
//        SysDao sysDao=sqlSession.getMapper(SysDao.class);
        int m=sysDao.selectSys(name);
        if(m>0){
            return -1;
        }
        int rs= sysDao.addSys(name,pass);
        if(rs>0){
            sqlSession.commit();
        }
        return rs;

    }
    public int changepassCheck(int id,String pass){
        if( StringUtil.isEmpty(pass)) {
            return -1 ;
        }
//        SqlSession sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
//        SysDao sysDao=sqlSession.getMapper(SysDao.class);
        int rs=sysDao.changePass(id,pass);
        if(rs>0){
            sqlSession.commit();
        }
        return rs;

    }
    public com.isoft.bean.Page<Sys> pageDate(String sysname, Integer typeId, Integer page, Integer size){
        if (null==sysname||sysname.trim().length()==0){
            sysname=null;
        }
        if (typeId==null||typeId<=0){
            typeId=null;
        }
        if (null==page||page<1){
            page=1;
        }
        if (null==size||size<1){
            size=5;
        }
//        SqlSession sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
//        SysDao sysDao=sqlSession.getMapper(SysDao.class);
        int rowCount=sysDao.getRowCount(sysname,typeId);
        ArrayList<Sys> list=sysDao.getPageData(sysname,typeId,(page-1)*size,size);
        int pageCount=(int)Math.ceil(rowCount*1.0)/size+1;
        return new Page<Sys>(page,size,pageCount,rowCount,list);

    }

    public int changeRole(Integer id){
//        if (null==role||role.trim().length()==0){
//            role=null;
//        }
        if (id==null||id<=0){
            id=null;
        }
        int rs;
        String m=sysDao.selectid(id);
        if(m.equals("系统管理员")){
            rs=sysDao.changerole("普通用户",id);
        }else {
            rs = sysDao.changerole("系统管理员", id);
        }
        if(rs>0){
            sqlSession.commit();
        }
        return rs;
    }
    public int register(String name,String pass){
        if(StringUtil.isEmpty(name) || StringUtil.isEmpty(pass)) {
            return -1 ;
        }
//        SqlSession sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
//        SysDao sysDao=sqlSession.getMapper(SysDao.class);
//        int m=sysDao.selectSys(name);
//        if(m>0){
//            return -1;
//        }
        int rs= sysDao.registerUser(name,pass);
        if(rs>0){
            sqlSession.commit();
        }
        return rs;

    }
    public int addshop(String name,String shop,int num){
        int rs= sysDao.addshop(name,shop,num);
        if(rs>0){
            sqlSession.commit();
        }
        return rs;

    }

    public ArrayList<shop> getpay(String name){
        ArrayList<shop> list=new ArrayList<>();
        list= sysDao.getpay(name);
        return list;
    }
}
