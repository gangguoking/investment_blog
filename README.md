# investment_blog

## 项目背景
#### Python 小任务 采集目标站：(选择其一即可)
#### Bloomberg:  https://www.bloomberg.com/markets
#### Insider:  https://www.insider.com     
#### 采集内容关键词：investments advisor, investment planning, investment plan 
#### 注：需将内容中的图片、视频进行本地化并上传到S3，并更新内容中原有资源为S3资源


## 安装依赖包

- python版本：python3.8

- pip命令行 
    > pip3 install -r requirement.txt


## 参数配置

### 请配置settings.py里的参数 FILES_STORE (当前存储的是本地的文件目录)
- 本地目录示例（如果你想存在本地）
> FILES_STORE = "/Users/huhao/WorkFiles/python_program/investment_blog/investment_blog/download_file/"
- s3目录示例（如果你想存在s3）
> FILES_STORE = "s3://bucket/s3_images"


## 运行程序
- 本地测试直接pycharm直接运行程序（图形界面直接点击 spiders目录 下 bloomberg_blog.py 的运行按钮即可）

- scrapy命令行启动
    > scrapy crawl bloomberg_blog
