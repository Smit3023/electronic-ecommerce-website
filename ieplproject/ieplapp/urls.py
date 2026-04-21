from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='IndexPage'),
    path('about-us/', views.aboutus, name='AboutPage'),
    path('products/', views.products, name='ProductPage'),
    path('products/<slug:slug>/', views.product_detail, name='ProductDetail'),
    path('solutions/', views.solutions, name='SolutionPage'),
    path('projects/', views.projects, name='ProjectPage'),
    path('blogs/', views.blogs, name='BlogPage'),
    path('blog-articles/<int:blog_id>/', views.blog_articles, name='BlogArticle'),
    path('contact-us/', views.ContactUs.as_view(), name='ContactPage'),
    path('join-us/', views.JoinUs.as_view(), name='JoinPage'),
    path('search/', views.search, name='Search'),

    # Cart URLs  ← these must be here
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout + Payment URLs  ← these must be here
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/create/', views.create_razorpay_order, name='create_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]
