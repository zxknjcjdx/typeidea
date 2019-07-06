import xadmin
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
from .models import Comment
from typeidea.custom_site import custom_site


@xadmin.sites.register(Comment)
class CommentAdmin(object):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time', 'operator')

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'
