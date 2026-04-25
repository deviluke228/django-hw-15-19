from django.contrib import admin
from .models import IceCreamSet, Topping
from .models import PremiumIceCream
from bboard.models import Bb, Rubric

class BbAdmin(admin.ModelAdmin):
    list_display = ('title_and_price', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title_and_price', 'content')
    search_fields = ('title_and_price', 'content')

admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(IceCreamSet)
admin.site.register(Topping)
admin.site.register(PremiumIceCream)