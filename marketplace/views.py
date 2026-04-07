"""
Views for UniDeal marketplace.
Thin views — business logic delegated to services.py, queries to selectors.py.
"""
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.views.decorators.http import require_POST

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserCredential, Admin, Product, Interest, Report
from .serializer import SignupSerializer, SigninSerializer
from . import services
from . import selectors


# ═══════════════════════════════════════════════════════════════════
# AUTH DECORATORS (session-based, using our custom UserCredential)
# ═══════════════════════════════════════════════════════════════════

def login_required_custom(view_func):
    """Require user to be logged in via session."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.warning(request, 'Please log in to continue.')
            return redirect('login')
        try:
            request.current_user = UserCredential.objects.get(
                id=request.session['user_id'], is_active=True
            )
        except UserCredential.DoesNotExist:
            request.session.flush()
            messages.error(request, 'Account not found or deactivated.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def seller_required(view_func):
    """Require logged-in user to be a seller."""
    @wraps(view_func)
    @login_required_custom
    def wrapper(request, *args, **kwargs):
        if request.current_user.role != 'seller':
            messages.error(request, 'Seller access only.')
            return redirect('browse_products')
        return view_func(request, *args, **kwargs)
    return wrapper


def buyer_required(view_func):
    """Require logged-in user to be a buyer."""
    @wraps(view_func)
    @login_required_custom
    def wrapper(request, *args, **kwargs):
        if request.current_user.role != 'buyer':
            messages.error(request, 'Buyer access only.')
            return redirect('browse_products')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Require admin session."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'admin_id' not in request.session:
            messages.warning(request, 'Admin login required.')
            return redirect('admin_login')
        try:
            request.current_admin = Admin.objects.get(id=request.session['admin_id'])
        except Admin.DoesNotExist:
            request.session.flush()
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ═══════════════════════════════════════════════════════════════════
# EXISTING API VIEWS (kept intact)
# ═══════════════════════════════════════════════════════════════════
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserCredential
from .serializer import SigninSerializer, SignupSerializer

# ======================
# PAGE VIEWS (HTML)
# ======================


def landing_page(request):
    return render(request, "main-before-login.html")


def signin_page(request):
    return render(request, "login-main.html")


def signup_page(request):
    return render(request, "signup-main.html")


def get_token_for_user(user):
    """Generate single JWT access token"""
    token = AccessToken()
    token["username"] = user.username
    return str(token)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    # print(f"Signup attempt")

    if serializer.is_valid():
        user = serializer.save()
        token = get_token_for_user(user)
        return Response(
            {"message": "User registered successfully", "token": token},
            status=drf_status.HTTP_201_CREATED
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def signin(request):
    serializer = SigninSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    try:
        user = UserCredential.objects.get(username=username)
    except UserCredential.DoesNotExist:
        return Response({"error": "Invalid username or password"}, status=drf_status.HTTP_401_UNAUTHORIZED)

    if not user.verify_password(password):
        return Response({"error": "Invalid username or password"}, status=drf_status.HTTP_401_UNAUTHORIZED)
    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]

    # print(f"Login attempt for {username}")

    try:
        user = UserCredential.objects.get(username=username)
    except UserCredential.DoesNotExist:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.verify_password(password):
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = get_token_for_user(user)
    return Response({"message": "Login successful", "token": token}, status=drf_status.HTTP_200_OK)


# ═══════════════════════════════════════════════════════════════════
# TEMPLATE-BASED AUTH VIEWS
# ═══════════════════════════════════════════════════════════════════

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        role = request.POST.get('role', 'buyer')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'marketplace/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'marketplace/register.html')

        if UserCredential.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'marketplace/register.html')

        user = UserCredential(username=username, email=email, phone=phone, role=role)
        user.set_password(password)
        user.save()

        request.session['user_id'] = user.id
        request.session['username'] = user.username
        request.session['role'] = user.role
        messages.success(request, f'Welcome to UniDeal, {user.username}!')

        if role == 'seller':
            return redirect('seller_dashboard')
        return redirect('browse_products')

    return render(request, 'marketplace/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = UserCredential.objects.get(username=username)
        except UserCredential.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'marketplace/login.html')

        if not user.is_active:
            messages.error(request, 'Your account has been deactivated. Contact admin.')
            return render(request, 'marketplace/login.html')

        if not user.verify_password(password):
            messages.error(request, 'Invalid username or password.')
            return render(request, 'marketplace/login.html')

        request.session['user_id'] = user.id
        request.session['username'] = user.username
        request.session['role'] = user.role
        messages.success(request, f'Welcome back, {user.username}!')

        if user.role == 'seller':
            return redirect('seller_dashboard')
        return redirect('browse_products')

    return render(request, 'marketplace/login.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# ═══════════════════════════════════════════════════════════════════
# ADMIN AUTH
# ═══════════════════════════════════════════════════════════════════

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            admin = Admin.objects.get(username=username)
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid admin credentials.')
            return render(request, 'marketplace/admin_login.html')

        if not admin.verify_password(password):
            messages.error(request, 'Invalid admin credentials.')
            return render(request, 'marketplace/admin_login.html')

        request.session['admin_id'] = admin.id
        request.session['admin_username'] = admin.username
        messages.success(request, 'Admin login successful.')
        return redirect('admin_dashboard')

    return render(request, 'marketplace/admin_login.html')


def admin_logout_view(request):
    request.session.flush()
    messages.success(request, 'Admin logged out.')
    return redirect('admin_login')


# ═══════════════════════════════════════════════════════════════════
# BUYER VIEWS
# ═══════════════════════════════════════════════════════════════════

def browse_products(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')

    products = selectors.get_approved_products(
        search=search or None,
        category=category or None,
        condition=condition or None,
    )

    # inject user context if logged in
    current_user = None
    if 'user_id' in request.session:
        try:
            current_user = UserCredential.objects.get(id=request.session['user_id'])
        except UserCredential.DoesNotExist:
            pass

    context = {
        'products': products,
        'search': search,
        'category': category,
        'condition': condition,
        'categories': Product.CATEGORY_CHOICES,
        'conditions': Product.CONDITION_CHOICES,
        'current_user': current_user,
    }
    return render(request, 'marketplace/browse_products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    current_user = None
    has_interest = False
    if 'user_id' in request.session:
        try:
            current_user = UserCredential.objects.get(id=request.session['user_id'])
            has_interest = selectors.has_buyer_expressed_interest(current_user.id, product_id)
        except UserCredential.DoesNotExist:
            pass

    comments = selectors.get_product_comments(product_id)

    context = {
        'product': product,
        'comments': comments,
        'current_user': current_user,
        'has_interest': has_interest,
        'report_reasons': Report.REASON_CHOICES,
    }
    return render(request, 'marketplace/product_detail.html', context)


@buyer_required
@require_POST
def express_interest_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, status='approved')
    message = request.POST.get('message', '')

    interest, created = services.express_interest(request.current_user, product, message)

    if created:
        messages.success(request, 'Your interest has been sent to the seller!')
    else:
        messages.info(request, 'You have already expressed interest in this product.')

    return redirect('product_detail', product_id=product_id)


@login_required_custom
@require_POST
def add_comment_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    text = request.POST.get('text', '').strip()

    if text:
        services.add_comment(request.current_user, product, text)
        messages.success(request, 'Comment added.')
    else:
        messages.error(request, 'Comment cannot be empty.')

    return redirect('product_detail', product_id=product_id)


@login_required_custom
@require_POST
def report_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reason = request.POST.get('reason', 'other')
    description = request.POST.get('description', '')

    services.submit_report(request.current_user, product, reason, description)
    messages.success(request, 'Report submitted. Admin will review it.')
    return redirect('product_detail', product_id=product_id)


@buyer_required
def buyer_interests_view(request):
    interests = selectors.get_buyer_interests(request.current_user.id)
    return render(request, 'marketplace/buyer_interests.html', {
        'interests': interests,
        'current_user': request.current_user,
    })


@buyer_required
def buyer_history_view(request):
    history = selectors.get_buyer_history(request.current_user.id)
    return render(request, 'marketplace/buyer_history.html', {
        'transactions': history,
        'current_user': request.current_user,
    })


# ═══════════════════════════════════════════════════════════════════
# SELLER VIEWS
# ═══════════════════════════════════════════════════════════════════

@seller_required
def seller_dashboard(request):
    products = selectors.get_seller_products(request.current_user.id)
    pending = products.filter(status='pending').count()
    approved = products.filter(status='approved').count()
    sold = products.filter(status='sold').count()
    rejected = products.filter(status='rejected').count()

    context = {
        'products': products,
        'pending_count': pending,
        'approved_count': approved,
        'sold_count': sold,
        'rejected_count': rejected,
        'current_user': request.current_user,
    }
    return render(request, 'marketplace/seller_dashboard.html', context)


@seller_required
def add_product_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0')
        category = request.POST.get('category', 'other')
        condition = request.POST.get('condition', 'good')
        images = request.FILES.getlist('images')

        if not title or not description or not price:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'marketplace/add_product.html', {
                'categories': Product.CATEGORY_CHOICES,
                'conditions': Product.CONDITION_CHOICES,
                'current_user': request.current_user,
            })

        if not images:
            messages.error(request, 'Please upload at least one image.')
            return render(request, 'marketplace/add_product.html', {
                'categories': Product.CATEGORY_CHOICES,
                'conditions': Product.CONDITION_CHOICES,
                'current_user': request.current_user,
            })

        try:
            price = float(price)
        except ValueError:
            messages.error(request, 'Invalid price.')
            return render(request, 'marketplace/add_product.html', {
                'categories': Product.CATEGORY_CHOICES,
                'conditions': Product.CONDITION_CHOICES,
                'current_user': request.current_user,
            })

        product = services.create_product(
            seller=request.current_user,
            title=title,
            description=description,
            price=price,
            category=category,
            condition=condition,
            images=images,
        )
        messages.success(request, 'Product submitted for approval!')
        return redirect('seller_dashboard')

    return render(request, 'marketplace/add_product.html', {
        'categories': Product.CATEGORY_CHOICES,
        'conditions': Product.CONDITION_CHOICES,
        'current_user': request.current_user,
    })


@seller_required
def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.current_user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0')
        category = request.POST.get('category', 'other')
        condition = request.POST.get('condition', 'good')
        new_images = request.FILES.getlist('images')
        remove_ids = request.POST.getlist('remove_images')

        try:
            price = float(price)
        except ValueError:
            messages.error(request, 'Invalid price.')
            return redirect('edit_product', product_id=product_id)

        services.update_product(
            product=product,
            title=title,
            description=description,
            price=price,
            category=category,
            condition=condition,
            new_images=new_images or None,
            remove_image_ids=remove_ids or None,
        )
        messages.success(request, 'Product updated and resubmitted for approval.')
        return redirect('seller_dashboard')

    return render(request, 'marketplace/edit_product.html', {
        'product': product,
        'categories': Product.CATEGORY_CHOICES,
        'conditions': Product.CONDITION_CHOICES,
        'current_user': request.current_user,
    })


@seller_required
@require_POST
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.current_user)
    services.delete_product(product)
    messages.success(request, 'Product deleted.')
    return redirect('seller_dashboard')


@seller_required
def seller_interests_view(request):
    interests = selectors.get_seller_all_interests(request.current_user.id)
    return render(request, 'marketplace/seller_interests.html', {
        'interests': interests,
        'current_user': request.current_user,
    })


@seller_required
@require_POST
def respond_interest_view(request, interest_id):
    interest = get_object_or_404(
        Interest, id=interest_id, product__seller=request.current_user
    )
    action = request.POST.get('action', 'reject')
    accept = (action == 'accept')

    services.respond_to_interest(interest_id, accept)

    if accept:
        messages.success(request, f'Interest from {interest.buyer.username} accepted! Contact info shared.')
    else:
        messages.info(request, f'Interest from {interest.buyer.username} rejected.')

    return redirect('seller_interests')


@seller_required
@require_POST
def complete_transaction_view(request, interest_id):
    interest = get_object_or_404(
        Interest, id=interest_id, product__seller=request.current_user, status='accepted'
    )
    
    if interest.product.status == 'sold':
        messages.info(request, f'Product {interest.product.title} is already marked as sold.')
    else:
        services.complete_transaction(interest.product, interest.buyer)
        messages.success(request, f'Transaction completed! {interest.product.title} marked as sold.')
        
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('seller_dashboard')


@seller_required
def seller_history_view(request):
    history = selectors.get_seller_history(request.current_user.id)
    return render(request, 'marketplace/seller_history.html', {
        'transactions': history,
        'current_user': request.current_user,
    })


# ═══════════════════════════════════════════════════════════════════
# ADMIN VIEWS
# ═══════════════════════════════════════════════════════════════════

@admin_required
def admin_dashboard_view(request):
    stats = selectors.get_admin_stats()
    return render(request, 'marketplace/admin_dashboard.html', {
        'stats': stats,
        'admin_user': request.current_admin,
    })


@admin_required
def admin_pending_view(request):
    products = selectors.get_pending_products()
    return render(request, 'marketplace/admin_pending.html', {
        'products': products,
        'admin_user': request.current_admin,
    })


@admin_required
@require_POST
def admin_approve_view(request, product_id):
    remarks = request.POST.get('remarks', '')
    services.approve_product(product_id, remarks)
    messages.success(request, 'Product approved.')
    return redirect('admin_pending')


@admin_required
@require_POST
def admin_reject_view(request, product_id):
    remarks = request.POST.get('remarks', '')
    services.reject_product(product_id, remarks)
    messages.success(request, 'Product rejected.')
    return redirect('admin_pending')


@admin_required
def admin_products_view(request):
    products = selectors.get_all_products()
    return render(request, 'marketplace/admin_products.html', {
        'products': products,
        'admin_user': request.current_admin,
    })


@admin_required
@require_POST
def admin_remove_product_view(request, product_id):
    services.admin_remove_product(product_id)
    messages.success(request, 'Product removed from marketplace.')
    return redirect('admin_products')


@admin_required
def admin_users_view(request):
    users = selectors.get_all_users()
    return render(request, 'marketplace/admin_users.html', {
        'users': users,
        'admin_user': request.current_admin,
    })


@admin_required
@require_POST
def admin_ban_seller_view(request, seller_id):
    services.admin_ban_seller(seller_id)
    messages.success(request, 'Seller banned and all their products removed.')
    return redirect('admin_users')


@admin_required
def admin_reports_view(request):
    reports = selectors.get_all_reports(resolved=False)
    return render(request, 'marketplace/admin_reports.html', {
        'reports': reports,
        'admin_user': request.current_admin,
    })


@admin_required
@require_POST
def admin_resolve_report_view(request, report_id):
    services.resolve_report(report_id)
    messages.success(request, 'Report resolved.')
    return redirect('admin_reports')
    return Response(
        {"message": "Login successful", "token": token}, status=status.HTTP_200_OK
    )
