from django.urls import path
from . import views

app_name = 'tellonym_api'

urlpatterns = [
    path('list/', views.list_tellonyms, name='list'),
    path('login/', views.login, name='login'),
    path('patch/<int:tellonym_id>/', views.update_tellonym, name='update')
]