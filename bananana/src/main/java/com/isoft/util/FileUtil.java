package com.isoft.util;

import com.isoft.bean.ServerResult;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class FileUtil {
    // 上传配置
    private static final int MAX_FILE_SIZE      = 1024 * 1024 * 4; // 4MB
    private static final int MAX_REQUEST_SIZE   = 1024 * 1024 * 10; // 10MB
    public static ServerResult fileUpload(HttpServletRequest request, HttpServletResponse response , String upPath , String[] params ) {
        boolean result = false ;
        String fileName = null ;
        // 客户端提交内容：文件域upphoto , 若干普通信息
        Map<String , String> value = new HashMap<>();
        // 构造文件上传要保存的路径，并检测路径是否存在，不存在创建该路径
        String uploadPath = request.getServletContext().getRealPath("/") + File.separator + upPath;
        // 如果目录不存在则创建
        File uploadDir = new File(uploadPath);
        if (!uploadDir.exists()) {
            uploadDir.mkdirs();
        }

        // 创建 上传参数设置相关的 对象
        DiskFileItemFactory factory = new DiskFileItemFactory();
        // 创建ServletFileUpload对象，设置上传相关参数
        ServletFileUpload upload = new ServletFileUpload(factory);
        // 设置最大文件上传值
        upload.setFileSizeMax(MAX_FILE_SIZE);
        // 设置最大请求值 (包含文件和表单数据)
        upload.setSizeMax(MAX_REQUEST_SIZE);
        // 中文处理
        upload.setHeaderEncoding("UTF-8");

        try {
            // 解析请求的内容提取文件数据 : 返回表单提交的所有数据
            List<FileItem> formItems = upload.parseRequest(request);

            if (formItems != null && formItems.size() > 0) {
                // 迭代表单数据，进行处理
                for (FileItem item : formItems) {
//                    System.out.println(item);
                    // FileItem.isFormField() : 如果是文件内容，返回false，如果是普通文本域，返回true
                    // FileItem.getName() 可以获取上传文件的文件名
                    if(item.isFormField()) {  // 处理普通文本域:id,name
                        value.put(item.getFieldName() , item.getString("utf-8")) ;
                    }
                    else {
                        // 构造用户上传文件的新名字
                        String oriFileName = item.getName() ;
                        String extName = oriFileName.substring(oriFileName.lastIndexOf(".")) ;
                        fileName = new SimpleDateFormat("yyyyMMddHHmmssSSSS").format(new Date()) +  extName ;
                        // 构造用户上传文件保存的绝对物理路径
                        String fullName = uploadPath + File.separator + fileName;
                        File storeFile = new File(fullName);
                        // 在控制台输出文件的上传路径
                        System.out.println(fullName);
                        // 保存文件到硬盘
                        item.write(storeFile);
                        System.out.println("上传文件成功！");
                        result = true ;
                    }
                }
                System.out.println(value);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        // 返回客户端表单提交后的结果 ：上传是否成功以及成功后文件浏览url
        String url = null ;
        if(result) {
            String protocol = request.getProtocol() ;
            protocol = protocol.substring(0 , protocol.indexOf("/")) ;
            url =  protocol + "://" +
                    request.getServerName() + ":" +
                    request.getServerPort() + "/" +
                    request.getContextPath() + "/" + upPath + "/" + fileName;
            System.out.println(url);
        }
        ServerResult obj = new ServerResult();
        obj.setErrorCode(result ? 0 : 1);
        obj.setErrorMsg(result ? "up seccese" : "up defest");
        Map<String , Object> map = new HashMap<>() ;
        map.put("url" , url ) ;
        map.put("params" , value ) ;
        obj.setResult(map);
        return obj;
    }
}
