from django.contrib import admin
from .models import Project, Expense, Notes

admin.site.register(Project)
admin.site.register(Expense)
admin.site.register(Notes)
