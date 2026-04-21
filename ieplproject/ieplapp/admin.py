from django.contrib import admin
from .models import (IndexSliderImage, AboutU, Categorie, FeatureProject,
                     Founder, Partner, Client, Testimonial, Product,
                     Solution, ProjectCategorie, Project, Blog, ContactU, JoinU)


@admin.register(ContactU)
class ContactUAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'email', 'phone_number', 'subject')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone_number', 'subject', 'message')


@admin.register(JoinU)
class JoinUAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone_number', 'resume')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display  = ('blog_title', 'blog_datemonth', 'blog_dateday')
    search_fields = ('blog_title',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('project_title', 'project_category')
    list_filter   = ('project_category',)
    search_fields = ('project_title',)

from .models import Order, OrderItem, Cart, CartItem

class OrderItemInline(admin.TabularInline):
    model   = OrderItem
    extra   = 0
    readonly_fields = ('product', 'quantity', 'price_at_buy')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ('id', 'user', 'total_amount', 'status', 'is_paid', 'created_at')
    list_filter    = ('status', 'is_paid')
    search_fields  = ('user__username', 'razorpay_order_id')
    list_editable  = ('status',)
    inlines        = [OrderItemInline]
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'is_paid', 'created_at')


admin.site.register(IndexSliderImage)
admin.site.register(AboutU)
admin.site.register(Categorie)
admin.site.register(FeatureProject)
admin.site.register(Founder)
admin.site.register(Partner)
admin.site.register(Client)
admin.site.register(Testimonial)
admin.site.register(Product)
admin.site.register(Solution)
admin.site.register(ProjectCategorie)
admin.site.register(Cart)
admin.site.register(CartItem)