##版本说明：
- 5.2.5: add ua list
- 5.2.6: add table create function
- 5.2.7: add ua list again
- 5.2.8: 添加获取百度cookie的方法
- 5.2.9: 修改百度cookie存储位置
- 5.2.10: add *.txt file
- 5.2.11: baidu cookie storage use sorted set
- 5.2.12: add baidu mb cookie
- 5.2.13: 修复本地中文乱码
- 5.2.14: downloader fail
- 5.2.15: downloader fail
- 5.2.16: pymysql版本写法问题
- 5.2.17: v1.0.0及以上请使用from pymysql.converters import escape_string

#### 新下载中心参数，参考 newDownloadReadme.md 文件

使用方法：
config={"param": {"et":13,'cu',url}}
request = SpiderRequest(headers=headers, urls=urls,config = config)
