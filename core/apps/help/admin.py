from django.contrib import admin

from .models.faq import FAQ
from .models.help_article import HelpArticle
from .models.help_category import HelpCategory


@admin.register(HelpCategory)
class HelpCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(HelpArticle)
class HelpArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'view_count']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'content', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = []


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_published', 'order']
    list_filter = ['is_published', 'category']
    search_fields = ['question', 'answer']
