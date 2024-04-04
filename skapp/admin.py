from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name', 'code', 'mrp', 'title', 'stock']
    list_filter=['code']
    search_fields=['name__startswith']

admin.site.register(Enquiry)
admin.site.register(Support)
# admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Slider)
admin.site.register(cartModel)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(country)
admin.site.register(state)
admin.site.register(city)
admin.site.register(orderTracking)
