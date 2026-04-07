"""
Service layer for UniDeal marketplace.
Business logic lives here — views stay thin.
"""
from .models import (
    Product, ProductImage, Interest, Comment, Report, Transaction, UserCredential, Admin
)
from django.utils import timezone


# ── Product Services ─────────────────────────────────────────────

def create_product(seller, title, description, price, category, condition, images):
    """Create a new product with images. Status defaults to 'pending'."""
    product = Product.objects.create(
        seller=seller,
        title=title,
        description=description,
        price=price,
        category=category,
        condition=condition,
        status='pending',
    )
    for i, img in enumerate(images):
        ProductImage.objects.create(
            product=product,
            image=img,
            is_primary=(i == 0),
        )
    return product


def update_product(product, title, description, price, category, condition, new_images=None, remove_image_ids=None):
    """Update product details. Resets status to pending for re-approval."""
    product.title = title
    product.description = description
    product.price = price
    product.category = category
    product.condition = condition
    product.status = 'pending'
    product.save()

    if remove_image_ids:
        product.images.filter(id__in=remove_image_ids).delete()

    if new_images:
        has_primary = product.images.filter(is_primary=True).exists()
        for i, img in enumerate(new_images):
            ProductImage.objects.create(
                product=product,
                image=img,
                is_primary=(not has_primary and i == 0),
            )

    return product


def delete_product(product):
    """Delete a product."""
    product.delete()


# ── Admin Approval Services ──────────────────────────────────────

def approve_product(product_id, remarks=''):
    """Approve a product for listing."""
    product = Product.objects.get(id=product_id)
    product.status = 'approved'
    product.admin_remarks = remarks
    product.save()
    return product


def reject_product(product_id, remarks=''):
    """Reject a product."""
    product = Product.objects.get(id=product_id)
    product.status = 'rejected'
    product.admin_remarks = remarks
    product.save()
    return product


def admin_remove_product(product_id):
    """Admin removes a product from the marketplace."""
    product = Product.objects.get(id=product_id)
    product.status = 'removed'
    product.save()
    return product


def admin_ban_seller(seller_id):
    """Ban a seller — deactivate account and remove all their products."""
    seller = UserCredential.objects.get(id=seller_id)
    seller.is_active = False
    seller.save()
    seller.products.update(status='removed')
    return seller


# ── Interest Services ────────────────────────────────────────────

def express_interest(buyer, product, message=''):
    """Buyer expresses interest in a product."""
    interest, created = Interest.objects.get_or_create(
        product=product,
        buyer=buyer,
        defaults={'message': message, 'status': 'pending'}
    )
    return interest, created


def respond_to_interest(interest_id, accept):
    """Seller accepts or rejects an interest."""
    interest = Interest.objects.get(id=interest_id)
    interest.status = 'accepted' if accept else 'rejected'
    interest.save()
    return interest


def complete_transaction(product, buyer):
    """Mark product as sold and create transaction record."""
    product.status = 'sold'
    product.save()

    transaction = Transaction.objects.create(
        product=product,
        seller=product.seller,
        buyer=buyer,
    )
    # reject all other pending interests
    product.interests.filter(status='pending').update(status='rejected')
    return transaction


# ── Comment & Report Services ────────────────────────────────────

def add_comment(user, product, text):
    """Add a comment to a product."""
    return Comment.objects.create(
        product=product,
        user=user,
        text=text,
    )


def submit_report(reporter, product, reason, description=''):
    """Submit a report against a product/seller."""
    return Report.objects.create(
        product=product,
        reporter=reporter,
        reason=reason,
        description=description,
    )


def resolve_report(report_id):
    """Mark a report as resolved."""
    report = Report.objects.get(id=report_id)
    report.is_resolved = True
    report.save()
    return report
