from django.contrib import admin
from . import models
from .models import Recipe, MultiRecipe, Fork

admin.site.register(Recipe)
admin.site.register(MultiRecipe)
admin.site.register(Fork)