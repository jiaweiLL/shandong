package com.isoft.entity;

import java.io.Serializable;
import java.util.Date;

/**
 * 对应数据表 tb_news , 从表
 */
public class News implements Serializable {
    private Integer id ;
    private String title ;
    private String content ;
    private Date adddatetime ;
    private String from ;
    private NewsType newsType;
    public News(){}

    public News(Integer id, String title, String content, Date adddatetime, String from) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.adddatetime = adddatetime;
        this.from = from;
    }

    public News(Integer id, String title, String content, Date adddatetime, String from, NewsType newsType) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.adddatetime = adddatetime;
        this.from = from;
        this.newsType = newsType;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Date getAdddatetime() {
        return adddatetime;
    }

    public void setAdddatetime(Date adddatetime) {
        this.adddatetime = adddatetime;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public NewsType getNewsType() {
        return newsType;
    }

    public void setNewsType(NewsType newsType) {
        this.newsType = newsType;
    }

    @Override
    public String toString() {
        return "News{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", content='" + content + '\'' +
                ", adddatetime=" + adddatetime +
                ", from='" + from + '\'' +
                ", newsType=" + newsType +
                '}';
    }
}
