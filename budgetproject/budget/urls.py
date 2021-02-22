from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.project_list,name='list'),
    path('notes', views.notes, name='notes'),
    path('deleteNote/<note_id>', views.deleteNote, name='delete'),
    path('add', views.ViewBudgets.as_view(),name='add'),
    path('<slug:project_slug>',views.project_detail,name="detail")#generally using data already obtained. For instance, a slug uses the title of an article to generate a URL.
]
