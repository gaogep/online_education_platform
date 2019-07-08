__author__ = 'Zpf'
__date__ = '2019/6/22 下午5:25'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
# from xadmin.layout import Fieldset, Main, Side, Row, FormHelper

from .models import EmailVerifyRecord, Banner, UserProfile


class UeserProfileAdmin(UserAdmin):
    pass
    # def get_form_layout(self):
    #     if self.org_obj:
    #         self.form_layout = (
    #             Main(
    #                 Fieldset('',
    #                          'username', 'password',
    #                          css_class='unsort no_title'
    #                          ),
    #                 Fieldset(_('Personal info'),
    #                          Row('first_name', 'last_name'),
    #                          'email'
    #                          ),
    #                 Fieldset(_('Permissions'),
    #                          'groups', 'user_permissions'
    #                          ),
    #                 Fieldset(_('Important dates'),
    #                          'last_login', 'date_joined'
    #                          ),
    #             ),
    #             Side(
    #                 Fieldset(_('Status'),
    #                          'is_active', 'is_staff', 'is_superuser',
    #                          ),
    #             )
    #         )


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
    model_icon = 'fa fa-user'  # 设置icon


class BannerAmin:
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile, UeserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
