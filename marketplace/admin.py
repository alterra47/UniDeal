from django.contrib import admin
from .models import (
    UserCredential, Admin as AdminModel, Product, ProductImage,
    Interest, Comment, Report, Transaction
)

admin.site.register(UserCredential)
admin.site.register(AdminModel)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Interest)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Transaction)
