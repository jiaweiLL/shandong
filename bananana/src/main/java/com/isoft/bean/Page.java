package com.isoft.bean;

import java.io.Serializable;
import java.util.ArrayList;

public class Page<T> implements Serializable {

    private int page;
    private int size;
    private int pageCount;
    private int rowCount;
    ArrayList<T> data;
    public Page(){

    }

    public Page(int page, int size, int pageCount, int rowCount, ArrayList<T> data) {
        this.page = page;
        this.size = size;
        this.pageCount = pageCount;
        this.rowCount = rowCount;
        this.data = data;
    }

    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public int getPageCount() {
        return pageCount;
    }

    public void setPageCount(int pageCount) {
        this.pageCount = pageCount;
    }

    public int getRowCount() {
        return rowCount;
    }

    public void setRowCount(int rowCount) {
        this.rowCount = rowCount;
    }

    public ArrayList<T> getData() {
        return data;
    }

    public void setData(ArrayList<T> data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "Page{" +
                "page=" + page +
                ", size=" + size +
                ", pageCount=" + pageCount +
                ", rowCount=" + rowCount +
                ", data=" + data +
                '}';
    }
}
