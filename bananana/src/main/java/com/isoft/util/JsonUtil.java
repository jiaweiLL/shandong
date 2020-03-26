package com.isoft.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonUtil {
    public static String obj2JsonStr(Object obj) {
        ObjectMapper objectMapper = new ObjectMapper() ;
        try {
            return objectMapper.writeValueAsString(obj) ;
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return null ;
        }
    }
}
