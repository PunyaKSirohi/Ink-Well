from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug' , 'created_at', 'status')
    list_display = ('status',)
    search_fields = ('title', 'body', 'tags')
    prepopulated_fields = {
        'slug': ('title',)
    }



admin.site.register(Post, PostAdmin)