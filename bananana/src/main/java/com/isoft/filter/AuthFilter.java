package com.isoft.filter;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

/*
未登录用户不能请求manager目录下的所有动态资源，动态资源Servlet配置时以.do结尾
登录用户将在Session中存储loginuser属性
 */
@WebFilter(urlPatterns = { "/admin/*"})
public class AuthFilter implements Filter {
    String[] pages ;
    public void destroy() {
    }

    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain) throws ServletException, IOException {

        HttpServletRequest request = (HttpServletRequest) req ;
        HttpSession session = request.getSession();
        Object obj = session.getAttribute("loginuser") ;
        if(null == obj) {
            ((HttpServletResponse)resp).sendRedirect(request.getContextPath() + "/Login.html");
            return ;
        }
        chain.doFilter(req, resp);
    }

    public void init(FilterConfig config) throws ServletException {
    }

}
