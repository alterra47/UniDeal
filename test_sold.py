import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UniDeal.settings')
django.setup()

from django.test import Client
from marketplace.models import UserCredential, Product, Interest

# we need a seller, buyer, product, interest
client = Client()

seller = UserCredential.objects.filter(role='seller').first()
buyer = UserCredential.objects.filter(role='buyer').first()

if not buyer:
    buyer = UserCredential.objects.create(username='testbuyer', role='buyer')
    buyer.set_password('test1234')
    buyer.save()

client.login(username=seller.username, password='test1234')

# create a dummy product and interest
product = Product.objects.create(seller=seller, title='Test Product', price=100, status='approved')
interest = Interest.objects.create(product=product, buyer=buyer, status='accepted')

response = client.post(f'/seller/interest/{interest.id}/complete/')
print("Status Code:", response.status_code)
print("Product status after:", Product.objects.get(id=product.id).status)
