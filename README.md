#### lip师兄投资规则自动化     

1. 安装chrome和chromedriver(注意版本对应)    
  https://cuiqingcai.com/31043.html

2. 将代码移植到服务端 (scp)

3. 启动代码

   ```python
   nohup python main.py 1>log.log 2>&1 &
   ```

   

运行结果如下:
```angular2html
2023-02-02 10:23:36,001 - INFO: 中证800 PE-TTM: 13.5
2023-02-02 10:23:41,940 - INFO: 中国十年期国债收益率: 2.9101
2023-02-02 10:23:58,024 - INFO: 可转债中位数价格: 124.887
2023-02-02 10:23:58,035 - INFO: 股市吸引力指数: 2.545, 黄金机会
2023-02-02 10:23:58,035 - INFO: 可转债吸引力指数: 124.887, 泡沫期
2023-02-02 10:24:11,051 - INFO: the email was sent successfully !!!
```







