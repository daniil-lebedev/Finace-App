from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #url for main page
    path('',views.project_list,name='list'),
    #url for notes page
    path('notes', views.notes, name='notes'),
    #url to reload a page when note is deleted
    path('deleteNote/<note_id>', views.deleteNote, name='delete'),
    #url for sending HTTP resopnse to export all spendings
    path('export_csv', views.exportSpendingCsv, name="export"),
    #url for sending HTTP resopnse to export all notes
    path('export_csv_note', views.exportNotesCsv, name="exportnote"),
    #url for the page where a new budget is created
    path('add', views.ViewBudgets.as_view(),name='add'),
    #unique url for budget
    path('<slug:project_slug>',views.project_detail,name="detail")
]


