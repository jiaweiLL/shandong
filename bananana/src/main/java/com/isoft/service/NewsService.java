package com.isoft.service;

import com.isoft.bean.Page;
import com.isoft.dao.NewsDao;
import com.isoft.dao.SysDao;
import com.isoft.db.SqlSessionUtil;
import com.isoft.entity.News;
import com.isoft.entity.NewsType;
import com.isoft.entity.Sys;
import com.isoft.util.StringUtil;
import org.apache.ibatis.session.SqlSession;

import java.util.ArrayList;
import java.util.Date;

public class NewsService {
    private NewsDao newsDao;
    private SqlSession sqlSession;
    public NewsService() {
        this.sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
        newsDao=sqlSession.getMapper(NewsDao.class);
    }
    public int addNewsType(String typename,String desc){
        if(StringUtil.isEmpty(typename) ) {
            return -1;
        }
        Integer rs=newsDao.addnewstype(typename,desc);
        if(rs>0||rs!=null){
            sqlSession.commit();
        }
        return rs;
    }
    public com.isoft.bean.Page<NewsType> selectnewstype(){

        ArrayList<NewsType> list=newsDao.selectnews();
        return new Page<NewsType>(0,0,0,0,list);
    }
    public int addnews(Integer typeid, String title, String content, Date adddatetime){
        Integer rs=newsDao.Addnews(typeid,title,content,adddatetime);
        if(StringUtil.isEmpty(title) ) {
            return -1;
        }
        if(rs>0||rs!=null){
            sqlSession.commit();
        }
        return rs;
    }
    public com.isoft.bean.Page<News> Allnews(String titleKey, Integer typeId, Integer page, Integer size){
        if (null==titleKey||titleKey.trim().length()==0){
            titleKey=null;
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
        int rowCount=newsDao.getRowCount(titleKey,typeId);
        ArrayList<News> list=newsDao.getPageData(titleKey,typeId,(page-1)*size,size);
        int pageCount=(int)Math.ceil(rowCount*1.0)/size+1;
        return new Page<News>(page,size,pageCount,rowCount,list);

    }

}
