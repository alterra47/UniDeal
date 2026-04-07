from django.urls import path
from . import views

urlpatterns = [
    # ── Existing API endpoints ────────────────────────────────
    path('api/signup/', views.signup, name='api_signup'),
    path('api/signin/', views.signin, name='api_signin'),

    # ── Auth (template-based) ─────────────────────────────────
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── Browse / Product Detail ───────────────────────────────
    path('', views.browse_products, name='browse_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/interest/', views.express_interest_view, name='express_interest'),
    path('product/<int:product_id>/comment/', views.add_comment_view, name='add_comment'),
    path('product/<int:product_id>/report/', views.report_product_view, name='report_product'),

    # ── Buyer ─────────────────────────────────────────────────
    path('buyer/interests/', views.buyer_interests_view, name='buyer_interests'),
    path('buyer/history/', views.buyer_history_view, name='buyer_history'),

    # ── Seller ────────────────────────────────────────────────
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/product/add/', views.add_product_view, name='add_product'),
    path('seller/product/<int:product_id>/edit/', views.edit_product_view, name='edit_product'),
    path('seller/product/<int:product_id>/delete/', views.delete_product_view, name='delete_product'),
    path('seller/interests/', views.seller_interests_view, name='seller_interests'),
    path('seller/interest/<int:interest_id>/respond/', views.respond_interest_view, name='respond_interest'),
    path('seller/interest/<int:interest_id>/complete/', views.complete_transaction_view, name='complete_transaction'),
    path('seller/history/', views.seller_history_view, name='seller_history'),

    # ── Admin Panel ───────────────────────────────────────────
    path('admin-panel/login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-panel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/products/pending/', views.admin_pending_view, name='admin_pending'),
    path('admin-panel/products/', views.admin_products_view, name='admin_products'),
    path('admin-panel/product/<int:product_id>/approve/', views.admin_approve_view, name='admin_approve'),
    path('admin-panel/product/<int:product_id>/reject/', views.admin_reject_view, name='admin_reject'),
    path('admin-panel/product/<int:product_id>/remove/', views.admin_remove_product_view, name='admin_remove_product'),
    path('admin-panel/users/', views.admin_users_view, name='admin_users'),
    path('admin-panel/seller/<int:seller_id>/ban/', views.admin_ban_seller_view, name='admin_ban_seller'),
    path('admin-panel/reports/', views.admin_reports_view, name='admin_reports'),
    path('admin-panel/report/<int:report_id>/resolve/', views.admin_resolve_report_view, name='admin_resolve_report'),
]