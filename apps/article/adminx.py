import xadmin
from .models import Article


class ArticleAdmin(object):
    list_display = ["title", "author", "article_sn", "lable", "click_num", "fav_num",
                    "article_brief", "article_desc", "article_front_image", "is_recommend", "add_time"]
    search_fields = ['title', ]
    list_editable = ["is_recommend", ]
    list_filter = ["title", "article_sn", "lable", "click_num", "fav_num", "is_recommend",]
    style_fields = {"article_desc": "ueditor"}


xadmin.site.register(Article, ArticleAdmin)
