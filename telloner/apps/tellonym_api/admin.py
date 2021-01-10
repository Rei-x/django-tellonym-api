from django.contrib import admin
from .models import Tellonym, TellonymUser


class TellonymInline(admin.TabularInline):
    readonly_fields = ('id',)
    model = Tellonym


class UserAdmin(admin.ModelAdmin):
    inlines = [TellonymInline]


admin.site.register(TellonymUser, UserAdmin)
# Register your models here.
