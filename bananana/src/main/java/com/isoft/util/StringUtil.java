package com.isoft.util;

import java.text.SimpleDateFormat;
import java.util.Date;

public class StringUtil {
    public static boolean isEmpty(String str) {
        if(str == null || str.trim().length() == 0) {
            return true ;
        }
        return false ;
    }

    /**
     * 构造储户id：开户日期时间毫秒+四位随机数
     * @return
     */
    public static String chuhuId() {
        return new SimpleDateFormat("yyyyMMddHHmmssSSSS").format(new Date()) + ((int)(Math.random() * 9000 + 1000)) ;
    }
    public static Integer str2Int(String str) {
        Integer i = null ;
        try {
            i = Integer.parseInt(str) ;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return i ;
    }
}
