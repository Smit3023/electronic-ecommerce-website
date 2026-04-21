from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template.exceptions import TemplateDoesNotExist
from django.views import View
from .forms import ContactForm, JoinForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from .models import IndexSliderImage, AboutU, Categorie, FeatureProject, Founder, Partner, Client, Testimonial, Product, Solution, ProjectCategorie, Project, Blog, ContactU, JoinU

# Create your views here.

# Preparing Index Page
def index(request):
    slider_images = IndexSliderImage.objects.all()
    about_texts = AboutU.objects.all()
    categories = Categorie.objects.all()
    featureprojects = FeatureProject.objects.all()
    founders = Founder.objects.all()
    partners = Partner.objects.all()
    clients = Client.objects.all()
    testimonials = Testimonial.objects.all()

    context = {
        'slider_images': slider_images,
        'about_texts': about_texts,
        'categories':categories,
        'featureprojects': featureprojects,
        'founders':founders,
        'partners': partners,
        'clients':clients,
        'testimonials':testimonials
    }
    return render(request, 'index.html', context)

# Fetching about us details
def aboutus(request):
    about_content = AboutU.objects.all()
    return render(request, 'about.html', {'about_content': about_content})

# Fetching Product details
def products(request):
    product_content = Product.objects.all()
    return render(request, 'products.html', {'product_content': product_content})

# Fetching Solution details
def solutions(request):
    solution_content = Solution.objects.all()
    return render(request, 'solutions.html', {'solution_content': solution_content})

# Fetching Project details grouping by Categories
def projects(request):
    # Fetching all categories
    categories = ProjectCategorie.objects.all()
    print("Category: ", categories)

    # Grouping projects by their respective categories
    project_by_category = {
        category: Project.objects.filter(project_category=category)
        for category in categories
    }
    print("Projects: ", project_by_category)

    # Passing the grouped projects to the template
    context = {
        'project_by_category': project_by_category,
    }

    return render(request, 'projects.html', context)

# Fetching Blog details
def blogs(request):
    blog_content = Blog.objects.all()
    return render(request, 'blog.html', {'blog_content': blog_content})

# Rendering Blog Article by blog id
def blog_articles(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})
    
# Collecting Contact form detail
class ContactUs(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Send email notification to admin
            send_mail(
                subject=f"New Contact: {form.cleaned_data['subject']}",
                message=f"From: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}\n"
                        f"Email: {form.cleaned_data['email']}\n"
                        f"Phone: {form.cleaned_data['phone_number']}\n\n"
                        f"Message:\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            messages.success(request, 'Thank you! We will get back to you soon.')
            return redirect('ContactPage')
        return render(request, 'contact.html', {'form': form})




# REPLACE the JoinUs class with this:
class JoinUs(View):
    def get(self, request):
        form = JoinForm()
        return render(request, 'join.html', {'form': form})

    def post(self, request):
        form = JoinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            send_mail(
                subject=f"New Job Application from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
                message=f"Email: {form.cleaned_data['email']}\nPhone: {form.cleaned_data['phone_number']}\n\nResume uploaded to admin panel.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            messages.success(request, 'Application submitted! We will contact you soon.')
            return redirect('JoinPage')
        return render(request, 'join.html', {'form': form})
    



# ADD this new search view function
def search(request):
    query = request.GET.get('q', '').strip()
    results = {
        'products': [],
        'projects': [],
        'blogs':    [],
        'query':    query,
    }
    if query:
        results['products'] = Product.objects.filter(product_name__icontains=query)
        results['projects'] = Project.objects.filter(
            Q(project_title__icontains=query) |
            Q(project_category__category_name__icontains=query)
        )
        results['blogs'] = Blog.objects.filter(
            Q(blog_title__icontains=query) |
            Q(blog_content__icontains=query)
        )
    return render(request, 'search_results.html', results)


# REPLACE the blogs view with this (adds pagination):
def blogs(request):
    all_blogs = Blog.objects.all().order_by('-id')
    paginator = Paginator(all_blogs, 6)   # 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj})


# REPLACE the products view with this (adds pagination):
def products(request):
    all_products = Product.objects.filter(is_active=True)
    paginator = Paginator(all_products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'page_obj': page_obj})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    return render(request, 'product_detail.html', {
        'product': product,
        'related': related,
    })


#Add cart 
@login_required(login_url='/login/')
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.product_name}" added to cart!')
    return redirect('cart')


@login_required(login_url='/login/')
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('cart')


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')




import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem

@login_required(login_url='/login/')
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    # Pre-fill address from user profile
    try:
        profile = request.user.profile
    except:
        profile = None

    return render(request, 'checkout.html', {
        'cart': cart,
        'profile': profile,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })


@login_required(login_url='/login/')
def create_razorpay_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart = get_object_or_404(Cart, user=request.user)
    total = int(cart.get_total() * 100)  # Razorpay uses paise (1 INR = 100 paise)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        'amount': total,
        'currency': 'INR',
        'payment_capture': 1,
    })

    # Save order to DB with status Pending
    order = Order.objects.create(
        user             = request.user,
        total_amount     = cart.get_total(),
        razorpay_order_id = razorpay_order['id'],
        shipping_name    = request.POST.get('full_name'),
        shipping_phone   = request.POST.get('phone'),
        shipping_address = request.POST.get('address'),
        shipping_city    = request.POST.get('city'),
        shipping_state   = request.POST.get('state'),
        shipping_pincode = request.POST.get('pincode'),
    )

    # Save order items
    for item in cart.items.all():
        OrderItem.objects.create(
            order        = order,
            product      = item.product,
            quantity     = item.quantity,
            price_at_buy = item.product.price,
        )

    return render(request, 'payment.html', {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': total,
        'user': request.user,
    })


@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        payment_id  = request.POST.get('razorpay_payment_id')
        order_id    = request.POST.get('razorpay_order_id')
        signature   = request.POST.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id':   order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature':  signature,
            })
            # Payment verified — update order
            order = Order.objects.get(razorpay_order_id=order_id)
            order.razorpay_payment_id = payment_id
            order.is_paid  = True
            order.status   = 'Confirmed'
            order.save()

            # Reduce stock for each item
            for item in order.items.all():
                item.product.stock -= item.quantity
                item.product.save()

            # Clear the cart
            Cart.objects.filter(user=order.user).delete()

            # Send confirmation email
            send_mail(
                subject=f'Order #{order.id} Confirmed — IEPL',
                message=f'Dear {order.user.username},\n\nYour order #{order.id} worth ₹{order.total_amount} has been confirmed.\nWe will ship it soon!\n\nThank you,\nIEPL Team',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.user.email],
                fail_silently=True,
            )
            return redirect('order_success', order_id=order.id)

        except Exception:
            messages.error(request, 'Payment verification failed. Please contact support.')
            return redirect('cart')


@login_required(login_url='/login/')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order

})