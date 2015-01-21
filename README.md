# 2rss
想用python去完成Yahoo pipe的事情


# 结构介绍
- 每一个feed 对应 一个 .py文件, python foo.py 会在原目录生成 foo.xml
- 本人是直接将py 文件部署到自己服务器上,以便生成一个url可以让rss阅读器可以抓到的
- 如何更新rss源: 通过服务器的 cron 定时生成 foo.xml

# 已经完成的RSS
- Donews 业内人说板块 (个人感觉还是比较有深度的) [donews.py]
- 京东众筹的智能硬件板块[jdzc.py]
- 南方翻译学院首页新闻 (纯个人关注的点, 可无视)[tcsisu.py]


# 没琢磨明白的
- InfoQ的rss 没有提供全文内容, 原网站通过js 加了一些混淆 没弄明白 [infoq]