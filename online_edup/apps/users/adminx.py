__author__ = 'Zpf'
__date__ = '2019/6/22 下午5:25'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting:
    enable_themes = True
    # use_bootswatch = True


class GlobalSetting:
    site_title = 'Mooc后台管理系统'
    site_footer = 'Mooc网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin:
    list_display = ['code', 'email', 'send_type', 'send_time']  # 设置列表的展示字段
    search_fields = ['code', 'email', 'send_type']              # 设置搜索字段
    list_filter = ['code', 'email', 'send_type', 'send_time']   # 筛选字段


class BannerAmin:
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
