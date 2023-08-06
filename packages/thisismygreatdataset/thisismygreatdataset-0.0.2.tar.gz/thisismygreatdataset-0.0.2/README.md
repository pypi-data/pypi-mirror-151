# 帮助文档

bilibili_rank是一个用来快速爬取b站排行榜视频相关信息（视频名称、up主、播放了、tag）的包。目前功能较少，只有爬取和实现tag图云的功能。依赖的包有matplotlib、pandas、wordcloud、cv2。

一下为一例子：
```
import bilibili_rank as br

pd = br.get_b_rank()
pd

pd.show_word_cloud(show=True, save=True, path='img.png')
```