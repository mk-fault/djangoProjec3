from django.contrib import admin
from drf.models import Course
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','introduction','teacher','price')
    search_fields = list_display
    list_filter = list_display
    list_editable = ['price']