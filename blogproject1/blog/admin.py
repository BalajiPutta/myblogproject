from django.contrib import admin
from .models import Post,Comments
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','body','publish','created','updated','status']
    list_filter = ('status','created','publish')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}
    ordering = ['status','publish']
    raw_id_fields = ('author',)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name','email','comment','created','updated','active']
    list_filter = ('active','created','updated')
    search_fields = ('name','email','comment')
admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentsAdmin)
