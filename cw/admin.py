from django.contrib import admin
from .models import Professor, Module, List, Rate
# Register your models here.
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(List)
admin.site.register(Rate)
