# 2rss
想用python去完成Yahoo pipe的事情, 输出'''优质的带全文内容的RSS源'''

一直没明白RSS没落, 而各种新闻客户端崛起的原因,本人实在是RSS的死忠, 并且带全文口味的 :) 最开始一直通过feed43, yahoo pipe之类的第三方工具去生成rss feed, 由于抓取的细节变数太多, 前面提到的第三方工具的pattern用起来还是有一些不顺手, 于是决定用python + 正则来自己做全文RSS源了. 本着分享致死的精神, 也放到github上了.

python写的比较小白, 大神笑后如能指点一二, 感激不尽. 也欢迎更多喜欢RSS的人分享自己的全文RSS源. 本项目没有限制, 基本上是python => XML 的就可以了.. 


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
