from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Перерегистрируем модель User для лучшего отображения
admin.site.unregister(User)
admin.site.register(User, UserAdmin)