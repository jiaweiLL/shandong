package com.isoft.entity;

import java.io.Serializable;
import java.util.Date;

public class SysAll implements Serializable {
    private Integer id ;
    private String sysname ;
    private String syspass;
    private String role ;
    private String sysphoto;
    private Date addtime ;

    public SysAll() {
    }

    public SysAll(Integer id, String sysname, String syspass, String role, String sysphoto, Date addtime) {
        this.id = id;
        this.sysname = sysname;
        this.syspass = syspass;
        this.role = role;
        this.sysphoto = sysphoto;
        this.addtime = addtime;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getSysname() {
        return sysname;
    }

    public void setSysname(String sysname) {
        this.sysname = sysname;
    }

    public String getSyspass() {
        return syspass;
    }

    public void setSyspass(String syspass) {
        this.syspass = syspass;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getSysphoto() {
        return sysphoto;
    }

    public void setSysphoto(String sysphoto) {
        this.sysphoto = sysphoto;
    }

    public Date getAdddatetime() {
        return addtime;
    }

    public void setAdddatetime(Date adddatetime) {
        this.addtime = addtime;
    }

    @Override
    public String toString() {
        return "SysAll{" +
                "id=" + id +
                ", sysname='" + sysname + '\'' +
                ", syspass='" + syspass + '\'' +
                ", role='" + role + '\'' +
                ", sysphoto='" + sysphoto + '\'' +
                ", adddatetime=" + addtime +
                '}';
    }
}
