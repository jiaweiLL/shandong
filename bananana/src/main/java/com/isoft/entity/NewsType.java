package com.isoft.entity;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * 对应数据库中的tb_newstype表，是tb_news的主表
 */
public class NewsType implements Serializable {
    private Integer id ;
    private String typename ;
    private String desc;
    private ArrayList<News> news ;
    public NewsType(){}

    public NewsType(Integer id, String typename, String desc) {
        this.id = id;
        this.typename = typename;
        this.desc = desc;
    }

    public NewsType(Integer id, String typename, String desc, ArrayList<News> news) {
        this.id = id;
        this.typename = typename;
        this.desc = desc;
        this.news = news;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTypename() {
        return typename;
    }

    public void setTypename(String typename) {
        this.typename = typename;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    public ArrayList<News> getNews() {
        return news;
    }

    public void setNews(ArrayList<News> news) {
        this.news = news;
    }

    @Override
    public String toString() {
        return "NewsType{" +
                "id=" + id +
                ", typename='" + typename + '\'' +
                ", desc='" + desc + '\'' +
                ", news=" + news +
                '}';
    }
}
