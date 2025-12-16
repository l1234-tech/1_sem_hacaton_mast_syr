from django.contrib import admin
from .models import Category, Tag, Note

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
    search_fields = ('name',)
    list_filter = ('color',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'text', 'user__username')
    list_filter = ('user', 'category', 'created_at')
    list_editable = ('category',)
    list_per_page = 20

    # Только основные поля для редактирования
    fields = ('user', 'title', 'text', 'category', 'tags')

    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)

# Регистрация моделей
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Note, NoteAdmin)