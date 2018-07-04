from django.db import models

class News(models.Model):

    is_top_choices = (
        (0, '不置顶'),
        (1, '置顶')
    )

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = "新闻"
        ordering = ['-is_top', '-create_time']

    def __str__(self):
        return self.title

    title = models.CharField(verbose_name="标题", max_length=50)
    img = models.ImageField(verbose_name='图片', default='none', upload_to="img")
    content = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    create_user = models.CharField(verbose_name="播报员", max_length=30)
    is_top = models.IntegerField(
        verbose_name='是否置顶', default=0, choices=is_top_choices)
    news_url = models.URLField(verbose_name="链接")


class HotVideo(models.Model):

    class Meta:
        verbose_name = "精彩视频"
        verbose_name_plural = "精彩视频"
        ordering = ['-add_time']

    title = models.CharField(verbose_name="标题", max_length=50)
    video_url = models.URLField(verbose_name="链接")
    add_time = models.DateTimeField(auto_now_add=True)
