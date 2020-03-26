import com.isoft.dao.NewsDao;
import com.isoft.dao.SysDao;
import com.isoft.db.SqlSessionUtil;
import com.isoft.service.NewsService;
import com.isoft.service.SysService;
import org.apache.ibatis.session.SqlSession;
import org.junit.Test;

import java.util.Date;

public class test {
    @Test
    public void test(){
        SqlSession sqlSession= SqlSessionUtil.getInstance(null).getSqlSession();
        NewsDao newsDao=sqlSession.getMapper(NewsDao.class);
        SysDao sysDao=sqlSession.getMapper(SysDao.class);
        SysService sysService=new SysService();
        String str="asdasdsdg";
        System.out.println(str.charAt(2)=='s');
//        System.out.println(sysService.getpay("sdust"));
//        System.out.println(newsDao.getPageData(null,1,1,3));
//        System.out.println(newsDao.Addnews(1,"asf","asf",new Date()));
//        NewsService newsService=newsDao.addnewstype("自然","动植物)
//        System.out.println(newsDao.addnewstype("自然","动植物"));
//        System.out.println(sysDao.addSys("jiawei","123"));
//        System.out.println(sysDao.logincheck("admin",MD5Util.getMD5("123")));
//        SysService sysService=new SysService();
//        PageeDao pageDao = sqlSession.getMapperer(PageDao.class) ;
//        System.out.println(sysDao.getPageData(null , null , 3 , 3));
//        TestDao testDao = sqlSession.getMapper(TestDao.class) ;
//        System.out.println(testDao.getAll());
//        System.out.println(sysService.loginCheck("admin","123"));
//        Page<Sys> page = sysService.pageData(null , null , 2 , 5) ;
//        Page<Sys> page=
//        ArrayList<Sys> list ` = sysDao.getPageData(null , null ,1 ,2) ;
//        System.out.println(list);
//        System.out.println(sysService.changepassCheck(6, MD5Util.getMD5("1234")));
//        System.out.println(sysService.addCheck("jj","123"));

//        NewsDao newsDao=sqlSession.getMapper(NewsDao.class);
//        System.out.println(newsDao.getBytitleKey("个"));
//        System.out.println(newsDao.searchNews("庆" , null , null , null));
//        News news=new News(4,"星宇年","坑",null,"qq");
//        int r=newsDao.updateNews(news);
//        if(r>0){
//            sqlSession.commit();
//        }
//        List<News> list = new ArrayList<News>() ;
//        list.add(new News(null , "t1" , "c1" , null , "f1" , new NewsType(2,null,null)));
//        list.add(new News(null , "t2" , "c2" , null , "f1" , new NewsType(3,null,null)));
//        list.add(new News(null , "t3" , "c3" , null , "f1" , new NewsType(4,null,null)));
//        int r = newsDao.addNews(list) ;
//        System.out.println(newsDao.getNews(2 , 5));
//        sqlSession.commit();
    }
}
