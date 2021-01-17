from django.contrib import admin
from .models import Tellonym, TellonymUser


class TellonymAdmin(admin.ModelAdmin):
    actions = ['make_new']

    def make_new(self, request, queryset):
        queryset.update(state="NEW")

    make_new.short_description = "Mark as new"


class TellonymInline(admin.TabularInline):
    readonly_fields = ('id',)
    model = Tellonym


class UserAdmin(admin.ModelAdmin):
    inlines = [TellonymInline]



admin.site.register(TellonymUser, UserAdmin)
admin.site.register(Tellonym, TellonymAdmin)
# Register your models here.
