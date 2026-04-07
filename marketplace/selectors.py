"""
Selector layer for UniDeal marketplace.
All read queries live here — views call these instead of hitting ORM directly.
"""
from .models import (
    Product, Interest, Comment, Report, Transaction, UserCredential
)
from django.db.models import Q, Count


# ── Product Selectors ────────────────────────────────────────────

def get_approved_products(search=None, category=None, condition=None):
    """Get all approved products, with optional filters."""
    qs = Product.objects.filter(status='approved')

    if search:
        qs = qs.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    if category:
        qs = qs.filter(category=category)
    if condition:
        qs = qs.filter(condition=condition)

    return qs.select_related('seller').prefetch_related('images')


def get_product_by_id(product_id):
    """Get a single product with related data."""
    return Product.objects.select_related('seller').prefetch_related(
        'images', 'comments__user', 'interests__buyer'
    ).get(id=product_id)


def get_seller_products(seller_id):
    """Get all products for a specific seller."""
    return Product.objects.filter(
        seller_id=seller_id
    ).prefetch_related('images', 'interests').order_by('-created_at')


def get_pending_products():
    """Get products awaiting admin approval."""
    return Product.objects.filter(
        status='pending'
    ).select_related('seller').prefetch_related('images').order_by('created_at')


def get_all_products():
    """Get all products for admin view."""
    return Product.objects.select_related('seller').prefetch_related(
        'images'
    ).order_by('-created_at')


# ── Interest Selectors ───────────────────────────────────────────

def get_product_interests(product_id):
    """Get all interests for a specific product."""
    return Interest.objects.filter(
        product_id=product_id
    ).select_related('buyer', 'product')


def get_seller_all_interests(seller_id):
    """Get all interests across all products for a seller."""
    return Interest.objects.filter(
        product__seller_id=seller_id
    ).select_related('buyer', 'product').order_by('-created_at')


def get_buyer_interests(buyer_id):
    """Get all interests a buyer has expressed."""
    return Interest.objects.filter(
        buyer_id=buyer_id
    ).select_related('product__seller', 'product').prefetch_related(
        'product__images'
    ).order_by('-created_at')


def has_buyer_expressed_interest(buyer_id, product_id):
    """Check if buyer already expressed interest in a product."""
    return Interest.objects.filter(
        buyer_id=buyer_id, product_id=product_id
    ).exists()


# ── History Selectors ────────────────────────────────────────────

def get_seller_history(seller_id):
    """Get completed sales for a seller."""
    return Transaction.objects.filter(
        seller_id=seller_id
    ).select_related('product', 'buyer').prefetch_related(
        'product__images'
    ).order_by('-completed_at')


def get_buyer_history(buyer_id):
    """Get completed purchases for a buyer."""
    return Transaction.objects.filter(
        buyer_id=buyer_id
    ).select_related('product', 'seller').prefetch_related(
        'product__images'
    ).order_by('-completed_at')


# ── Comment Selectors ────────────────────────────────────────────

def get_product_comments(product_id):
    """Get all comments for a product."""
    return Comment.objects.filter(
        product_id=product_id
    ).select_related('user').order_by('-created_at')


# ── Report Selectors ─────────────────────────────────────────────

def get_all_reports(resolved=None):
    """Get all reports, optionally filtered by resolved status."""
    qs = Report.objects.select_related('product__seller', 'reporter')
    if resolved is not None:
        qs = qs.filter(is_resolved=resolved)
    return qs.order_by('-created_at')


# ── User Selectors ───────────────────────────────────────────────

def get_all_users():
    """Get all users (buyers + sellers)."""
    return UserCredential.objects.all().order_by('-created_at')


def get_all_sellers():
    """Get all sellers."""
    return UserCredential.objects.filter(role='seller').order_by('-created_at')


def get_all_buyers():
    """Get all buyers."""
    return UserCredential.objects.filter(role='buyer').order_by('-created_at')


# ── Dashboard Stats ──────────────────────────────────────────────

def get_admin_stats():
    """Get aggregate stats for admin dashboard."""
    return {
        'total_users': UserCredential.objects.count(),
        'total_sellers': UserCredential.objects.filter(role='seller').count(),
        'total_buyers': UserCredential.objects.filter(role='buyer').count(),
        'total_products': Product.objects.count(),
        'pending_products': Product.objects.filter(status='pending').count(),
        'approved_products': Product.objects.filter(status='approved').count(),
        'sold_products': Product.objects.filter(status='sold').count(),
        'total_reports': Report.objects.filter(is_resolved=False).count(),
        'total_transactions': Transaction.objects.count(),
    }
