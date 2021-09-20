from django.contrib import admin
from .models import Finch, Feeding, Photo

# Register your models here.

admin.site.register(Finch)
admin.site.register(Feeding)
admin.site.register(Photo)