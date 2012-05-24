from drawings.models import Drawing
from django.contrib import admin

class DrawingAdmin(admin.ModelAdmin):
    fieldsets=[
               (None,    {'fields':['drawingpart']}),
               ('Date',    {'fields':['create_date'], 'classes':['collapse']}),
               ]

admin.site.register(Drawing, DrawingAdmin)