from django.contrib import admin
from .models import Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at', 'status')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'body', 'tags')
    prepopulated_fields = {
        'slug': ('title',)
    }
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('author__username', 'content')
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        if request:
            self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
        if request:
            self.message_user(request, f'{queryset.count()} comments disapproved.')
    disapprove_comments.short_description = "Disapprove selected comments"

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)