from django.contrib import admin
from .models import Bill, BillLineItem

admin.site.register(Bill)
admin.site.register(BillLineItem)
