package com.isoft.entity;


import java.io.Serializable;

public class Sys implements Serializable {
    private int id;
    private String sysname;
    private String syspass;
    private String role;
    public Sys(){

    }

    public Sys(int id, String sysname, String syspass, String role) {
        this.id = id;
        this.sysname = sysname;
        this.syspass = syspass;
        this.role = role;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
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

    @Override
    public String toString() {
        return "Sys{" +
                "id=" + id +
                ", sysname='" + sysname + '\'' +
                ", syspass='" + syspass + '\'' +
                ", role='" + role + '\'' +
                '}';
    }
}
