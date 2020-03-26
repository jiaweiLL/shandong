package com.isoft.dao;



import com.isoft.entity.News;
import com.isoft.entity.shop;
import com.isoft.entity.Sys;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.ArrayList;
import java.util.List;

public interface SysDao {
    /**
     * 获得所有购物车商品
     * @param name
     * @return
     */
    ArrayList<shop> getpay(@Param("name") String name);


    int changerole(@Param("role") String role,@Param("id") Integer id);
    String selectid(@Param("id") Integer id);

    /**
     * 增加商品
     * @param name
     * @param shop
     * @return
     */



    @Insert("insert into tb_shop values(null,#{name} , #{shop},#{num})")
    int addshop(@Param("name") String name, @Param("shop") String shop,  @Param("num") int num);
    /**
     * 注册用户
     * @param name
     * @param pass
     * @return
     */
    @Insert("insert into tb_sys values(null,#{name} , #{pass},'普通用户')")
    int registerUser(@Param("name") String name,@Param("pass") String pass);

    /**
     * 查询所有用户
     * @return
     */
//    @Select("select * from tb_sys")
    ArrayList<Sys> getPageData(@Param("sysname") String sysname, @Param("typeId") Integer typeId, @Param("offset") Integer offset, @Param("rows") Integer rows);
    int getRowCount(@Param("sysname") String sysname, @Param("typeId") Integer typeId);
    /**
     * 查询表中单个用户
     * @param name
     * @return
     */
    @Select("select * from tb_sys where sysname=#{name}")
    int selectSys(String name);
    /**
     * 登录验证
     * @param name
     * @param pass
     * @return
     */
    @Select("select * from tb_sys where sysname=#{name} and syspass=#{pass}")
    Sys logincheck(@Param("name") String name,@Param("pass") String pass);

    /**
     * 增加管理员
     * @param name
     * @param pass
     * @return
     */
    @Insert("insert into tb_sys values(null,#{name} , #{pass},'系统管理员')")
    int addSys(@Param("name") String name,@Param("pass") String pass);

    /**
     * 修改管理员密码
     * @param id
     * @param pass
     * @return
     */
    @Update("update tb_sys set syspass=#{pass} where id=#{id}")
    int changePass(@Param("id") int id ,@Param("pass") String pass);

}
