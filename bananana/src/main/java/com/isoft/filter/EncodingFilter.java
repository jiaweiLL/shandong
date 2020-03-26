package com.isoft.filter;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.annotation.WebInitParam;
import java.io.IOException;

@WebFilter(filterName = "EncodingFilter" ,
           urlPatterns = "/*",
           initParams = {@WebInitParam(name="encode" , value = "utf-8")}
)
public class EncodingFilter implements Filter {
    private String encoding ;

    public void destroy() {
        System.out.println("call EncodingFilter.destroy()");
    }

    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain) throws ServletException, IOException {
        req.setCharacterEncoding(encoding);
        resp.setCharacterEncoding(encoding);
        chain.doFilter(req , resp);
        /*
        System.out.println("before chain.doFilter()  -- call EncodingFilter.doFilter!");
        chain.doFilter(req, resp);
        System.out.println("after chain.doFilter()  -- call EncodingFilter.doFilter!");
        */
    }

    public void init(FilterConfig config) throws ServletException {
        System.out.println("call EncodingFilter.init()");
        encoding = config.getInitParameter("encode") ;
        if(encoding == null || encoding.trim().length() == 0) {
            encoding = "UTF-8" ;
        }
    }

}
