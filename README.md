# wechat_pyspider
利用pyspider与搜狗搜索引擎抓取微信公众号文章并提取信息存入数据库
## 关于cookies与headers ##
crawl_config中需要设置cookies与 headers，为字典格式，由于cookies会变化上传时删去了
## 关于代理设置 ##
在抓取十页左右后，会出现ip反爬，切换ip可以避免。利用崔老师的https://github.com/Python3WebSpider/ProxyPool代理池在本地5555端口获取代理，填入crawl_config即可