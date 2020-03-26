package com.isoft.entity;

public class shop {

    public int getNum() {
        return num;
    }

    public void setNum(int num) {
        this.num = num;
    }

    private int num;
    private int id;

    @Override
    public String toString() {
        return "shop{" +
                "num=" + num +
                ", id=" + id +
                ", name='" + name + '\'' +
                ", shop='" + shop + '\'' +
                '}';
    }

    private String name;
    private String shop;
    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setShop(String shop) {
        this.shop = shop;
    }


    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getShop() {
        return shop;
    }


}
