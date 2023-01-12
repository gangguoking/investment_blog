# investment_blog

## 项目背景
#### Python 小任务 采集目标站：(选择其一即可)
#### Bloomberg:  https://www.bloomberg.com/markets
#### Insider:  https://www.insider.com     
#### 采集内容关键词：investments advisor, investment planning, investment plan 
#### 注：需将内容中的图片、视频进行本地化并上传到S3，并更新内容中原有资源为S3资源


## 项目介绍
### 项目使用 scrapy 框架做了一个简易的爬虫程序
### 可以自行配置下载到的内容存储在本地还是s3


## 项目依赖

- python版本：python3.8

- 安装依赖包，pip命令行 
    > pip3 install -r requirement.txt


## 参数配置

### 请配置settings.py里的参数 FILES_STORE (当前存储的是本地的文件目录)
#### 文件存储配置请参考 https://www.osgeo.cn/scrapy/topics/media-pipeline.html
- 本地目录示例（如果你想存在本地）
> FILES_STORE = "/Users/huhao/WorkFiles/python_program/investment_blog/investment_blog/download_file/"
- s3目录示例（如果你想存在s3），需要挂载s3到本地，可参考：https://www.cnblogs.com/faberbeta/p/15953850.html
> FILES_STORE = "s3://bucket/s3_images"


## 运行程序
- 本地测试直接pycharm直接运行程序（图形界面直接点击 spiders目录 下 bloomberg_blog.py 的运行按钮即可）

- scrapy命令行启动
    > scrapy crawl bloomberg_blog


## 文件保存位置
- 图片文件存储在 bloomberg_jpg 目录
- audio文件存储在 bloomberg_audio 目录
- video文件存储在 bloomberg_video 目录
- 内容清单存储在 Bloomberg_query.csv 文件下，您可以调用 utils 目录下的 df_file.py 进行去重或者生成excel文件


