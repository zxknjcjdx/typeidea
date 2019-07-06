import xadmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry
# Register your models here.
from .models import Category, Tag, Post
from .adminforms import PostAdminForm
# from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


#实现在分类里面添加修改文章的功能，其中fields是可以修改文章的哪些项
# class PostInline(object):
#     # fields = ('title', 'desc')
#     # extra = 1
#     # model = Post
#     form_layout = (
#         Container(
#             Row('title', 'desc')
#         )
#     )
#     extra = 1
#     model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

#save_model这里实现的功能是将登录的用户名给owner对象
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

#添加一个展示字段为post_count
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'tag_count')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)

    def tag_count(self, obj):
        return obj.post_set.count()
    tag_count.short_description = '标签数量'


class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __int__(self, field, request, params, model, admin_view, field_path):
        super().__init__(field, request, params, model, admin_view, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)
    #自定义过滤器只展示当前用户分类
    # title = '分类过滤器'
    # parameter_name = 'owner_category'
    #
    # def lookups(self, request, model_admin):
    #     return Category.objects.filter(owner=request.user).values_list('id', 'name')
    #
    # def queryset(self, request, queryset):
    #     category_id = self.value()
    #     if category_id:
    #         return queryset.filter(category_id=self.value())
    #     return queryset


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'status', 'created_time', 'owner', 'operator')
    # list_display_links = ['title', 'category']  这个是用来配置哪些字段可以作为链接，点击他们可以进入到编辑界面
    exclude = ('owner',)

    list_filter = ['category']
    search_fields = ['title', 'category__name']

    filter_horizontal = ('tag',)
    #这个可以把标签从左边拉到右边去，如果是filter_vertical那么就是把上面的拉到下面去，个人觉得，水平的比较好看

    actions_on_top = True
    # actions_on_bottom = True 这个是展示页面的动作

    # save_on_top = True  这个是增加页面的操作项，默认下面有了

    # fieldsets = (
    #     ('基础配置', {
    #         'description': '基础配置描述',
    #         'fields': (
    #             ('title', 'category'),
    #             'status',
    #         )
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc',
    #             'content',
    #         )
    #     }),
    #     ('额外信息', {
    #         'classes': ('collapse',),
    #         'fields': ('tag',),
    #     })
    # )
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", 'category'),
            'status',
            'tag'
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

#这里虽然也是添加一个字段到展示界面，但是实际上这个实现了一个编辑的功能，其中reverse可以将url组合
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>', reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'


# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(object):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)

#这个函数和上面的CategoryOwnerFilter函数组合，可以实现在文章展示里面只展示本用户的文章
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )








