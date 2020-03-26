package com.isoft.dao;

import com.isoft.entity.News;
import com.isoft.entity.NewsType;
import com.isoft.entity.Sys;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Param;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public interface NewsDao {
    ArrayList<News> getPageData(@Param("titleKey") String titleKey, @Param("typeid") Integer typeid, @Param("offset") Integer offset, @Param("rows") Integer rows);
    int getRowCount(@Param("titleKey") String titleKey, @Param("typeid") Integer typeid);
    ArrayList<News> selectAllNews();
    /**
     * 增加新闻
     * @param title
     * @param content
     * @return
     */
    int Addnews(@Param("typeid") Integer typeid, @Param("title") String title, @Param("content") String content, @Param("adddatetime") Date adddatetime);
    /**
     * 增加新闻类型
     * @param typename
     * @param desc
     * @return
     */
//    @Insert("insert into tb_newstype values(null , #{typename} , #{desc} )")
    int addnewstype(@Param("typename") String typename,@Param("desc") String desc);

    /**
     * 所有新闻类型
     * @return
     */
    ArrayList<NewsType> selectnews();
    /**
     * 根据新闻标题关键字查询新闻信息（不包括新闻所属类型）
     * @param titleKey  新闻标题关键字，如果传参为null，则查询所有新闻
     * @return
     */
//    List<News> getBytitleKey(@Param("titleKey") String titleKey) ;

    /**
     * 条件检索查询新闻
     * @param titleKey
     * @param contentKey
     * @param addDate   格式为 yyyy-MM-dd
     * @param newstypeId
     * @return
     */
//    List<News> searchNews(@Param("titleKey") String titleKey, @Param("contentKey") String contentKey,
//                          @Param("addDate") String addDate, @Param("id") Integer newstypeId) ;
//
//    int updateNews(News news) ;
//    List<News> searchNews2(@Param("titleKey") String titleKey, @Param("contentKey") String contentKey,
//                           @Param("addDate") String addDate, @Param("id") Integer newstypeId) ;
//
//    int updateNews2(News news) ;
//
//    int addNews(List<News> list) ;
//
//    int deleteByIds(Integer[] ids) ;

    /**
     * 获取id值区间内的新闻，开区间
     * @param idLower  下限，可以为null
     * @param idUpper  上限，可以为null
     * @return
     */
//    List<News> getNews(@Param("idLower") Integer idLower, @Param("idUpper") Integer idUpper) ;
}

