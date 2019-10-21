import xadmin
from .models import Scenic, ScenicImage, Banner, HotSearchWords


class ScenicAdmin(object):
    list_display = ["name", "scenic_sn", "lable", "province", "city", "address",
                    "click_num", "visit_num", "fav_num", "price", "scenic_brief", "scenic_desc",
                    "is_ticket", "scenic_front_image", "is_recommend", "add_time"]
    search_fields = ['name', ]
    list_editable = ["is_recommend", ]
    list_filter = ["name", "click_num", "visit_num", "fav_num", "price", "is_ticket", "is_recommend", "add_time"]
    style_fields = {"scenic_desc": "ueditor"}

    class ScenicImagesInline(object):
        model = ScenicImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [ScenicImagesInline]


class BannerGoodsAdmin(object):
    list_display = ["scenic", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


xadmin.site.register(Scenic, ScenicAdmin)
xadmin.site.register(Banner, BannerGoodsAdmin)
xadmin.site.register(HotSearchWords, HotSearchAdmin)
