package com.isoft.db;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.IOException;

public class SqlSessionUtil {
    private static SqlSessionUtil ourInstance ;
    private static SqlSession sqlSession ;
    private static String configFile = null ;

    /**
     *
     * @param configFile  如果为null，则MyBatis配置文件使用文件名mybatis-config.xml
     * @return
     */

    public synchronized static SqlSessionUtil getInstance(String configFile) {
        if(configFile != null && configFile.trim().length() > 0) {
            SqlSessionUtil.configFile = configFile;
        } else {
            SqlSessionUtil.configFile = "mybatis-config.xml" ;
        }
        ourInstance = new SqlSessionUtil() ;
        return ourInstance;
    }

    private SqlSessionUtil() {
        if(null == sqlSession) {
            try {
                sqlSession = new SqlSessionFactoryBuilder().build(Resources.getResourceAsReader(configFile)).openSession();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    public SqlSession getSqlSession() {
        return sqlSession ;
    }
    public void closeConn() {
        if(null != sqlSession) {
            sqlSession.close();
            sqlSession = null ;
        }
    }
}
