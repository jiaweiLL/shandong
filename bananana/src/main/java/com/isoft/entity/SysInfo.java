package com.isoft.entity;

import java.io.Serializable;
import java.util.Date;

public class SysInfo implements Serializable {
    private Integer sysid ;
    private String sysphoto ;
    private Date addtime ;
    public SysInfo(){}

    public SysInfo(Integer sysid, String sysphoto, Date addtime) {
        this.sysid = sysid;
        this.sysphoto = sysphoto;
        this.addtime = addtime;
    }

    public Integer getSysid() {
        return sysid;
    }

    public void setSysid(Integer sysid) {
        this.sysid = sysid;
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
        return "SysInfo{" +
                "sysid=" + sysid +
                ", sysphoto='" + sysphoto + '\'' +
                ", addtime=" + addtime +
                '}';
    }
}
