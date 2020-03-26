package com.isoft.bean;

import java.io.Serializable;

public class ServerResult implements Serializable {
    private Integer errorCode ;
    private String errorMsg ;
    private Object result ;
    public ServerResult(){}

    public ServerResult(Integer errorCode, String errorMsg, Object result) {
        this.errorCode = errorCode;
        this.errorMsg = errorMsg;
        this.result = result;
    }

    public Integer getErrorCode() {
        return errorCode;
    }

    public void setErrorCode(Integer errorCode) {
        this.errorCode = errorCode;
    }

    public String getErrorMsg() {
        return errorMsg;
    }

    public void setErrorMsg(String errorMsg) {
        this.errorMsg = errorMsg;
    }

    public Object getResult() {
        return result;
    }

    public void setResult(Object result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "ServerResult{" +
                "errorCode=" + errorCode +
                ", errorMsg='" + errorMsg + '\'' +
                ", result=" + result +
                '}';
    }
}
