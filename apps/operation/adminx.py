import xadmin
from .models import UserFav, UserLeavingMessage, Questionnaire


class UserFavAdmin(object):
    list_display = ['user', 'article', "add_time"]


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'article', "message", "add_time"]


class QuestionnaireAdmin(object):
    list_display = ['user', 'choose', "add_time"]


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(Questionnaire, QuestionnaireAdmin)
