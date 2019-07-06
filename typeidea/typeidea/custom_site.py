from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = '博客后台管理'
    site_title = 'Typeidea管理后台'
    index_title = '我的blog后台'


custom_site = CustomSite(name='cus_admin')
#这里只是继承了admin的功能，然后改了一下名字而已，另外在url里面配置了将用户和管理界面分开了