from django.contrib import admin
from .models import *

class SubjectInline(admin.StackedInline):
    model = Subject
    extra = 1


class FAQInline(admin.StackedInline):
    model = FAQ
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type')
    list_filter = ('type', )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [SubjectInline, FAQInline]
    list_display = ('name', 'slug', 'category', 'price', 'image_url')
    list_filter = ('category', )
    search_fields = ('name', )
    list_display_links = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image_url')
    search_fields = ('name', )
    list_filter = ('course__name', )
    prepopulated_fields = {'slug': ('name', )}

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'telegram_id')
    readonly_fields = ('username', 'telegram_id')


# admin.site.register(Subject)
# admin.site.register(FAQ)