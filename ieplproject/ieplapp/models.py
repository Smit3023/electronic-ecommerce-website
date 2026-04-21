from django.db import models
from django.utils.text import slugify

# Create your models here.

# Username: interiorlights
# Password: interiorlights

# Model for Index page slider images
class IndexSliderImage(models.Model):
    slider_image = models.FileField(upload_to='index_slider_images/')

    def __str__(self):
        return f'Image {self.id}'

# Model for About Us contents
class AboutU(models.Model):
    what_we_offer_text = models.CharField(max_length=350)
    about_us_content_1 = models.CharField(max_length=350)
    about_us_content_2 = models.CharField(max_length=350)
    about_us_content_3 = models.CharField(max_length=350)
    about_us_content_4 = models.CharField(max_length=350)
    about_image_1 = models.FileField(upload_to='about_images/')
    about_image_2 = models.FileField(upload_to='about_images/')
    about_image_3 = models.FileField(upload_to='about_images/')
    our_mission_heading = models.CharField(max_length=200)
    our_mission_content = models.CharField(max_length=500)
    core_value_heading_1 = models.CharField(max_length=100)
    core_value_content_1 = models.CharField(max_length=300)
    core_value_heading_2 = models.CharField(max_length=100)
    core_value_content_2 = models.CharField(max_length=300)
    core_value_heading_3 = models.CharField(max_length=100)
    core_value_content_3 = models.CharField(max_length=300)

    def __str__(self):
        return 'About'

# Model for Categories
class Categorie(models.Model):
    category_name = models.CharField(max_length=100)
    category_content = models.CharField(max_length=500)
    category_image = models.FileField(upload_to='category_images/')

    def __str__(self):
        return self.category_name
    
# Model for Feature Projects
class FeatureProject(models.Model):
    feature_image = models.FileField(upload_to='feature_projects_images/')
    feature_title = models.CharField(max_length=100)

    def __str__(self):
        return self.feature_title

# Model for Founders
class Founder(models.Model):
    founder_name = models.CharField(max_length=50)
    founder_position = models.CharField(max_length=100)
    founder_description = models.CharField(max_length=500)
    founder_image = models.FileField(upload_to='founder_images/')
    founder_linkedin = models.CharField(max_length=500)

    def __str__(self):
        return self.founder_name

# Model for Partners
class Partner(models.Model):
    partner_name = models.CharField(max_length=50)
    partner_image = models.FileField(upload_to='partner_images/')

    def __str__(self):
        return self.partner_name
    
# Model for Clients
class Client(models.Model):
    client_name = models.CharField(max_length=50)
    client_image = models.FileField(upload_to='client_images/')

    def __str__(self):
        return self.client_name
    
# Model for Testimonials
class Testimonial(models.Model):
    testimonial_name = models.CharField(max_length=50)
    testimonial_position = models.CharField(max_length=50)
    testimonial_brand = models.CharField(max_length=50)
    testimonial_description = models.CharField(max_length=500)

    def __str__(self):
        return self.testimonial_name
    
# Model for Products

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bulb',    'Bulbs'),
        ('panel',   'Panels'),
        ('fixture', 'Fixtures'),
        ('strip',   'Strip Lights'),
        ('outdoor', 'Outdoor'),
        ('other',   'Other'),
    ]
    product_name     = models.CharField(max_length=100)
    slug             = models.SlugField(max_length=120, unique=True, blank=True)
    product_image    = models.FileField(upload_to='product_images/')
    category         = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description      = models.TextField(blank=True)
    price            = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock            = models.PositiveIntegerField(default=0)
    wattage          = models.CharField(max_length=30, blank=True)
    color_temp       = models.CharField(max_length=30, blank=True)
    ip_rating        = models.CharField(max_length=20, blank=True)
    is_active        = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

# ADD these new models BELOW the Product class:

class Cart(models.Model):
    user       = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending',   'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped',   'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user             = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    total_amount     = models.DecimalField(max_digits=10, decimal_places=2)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    razorpay_order_id   = models.CharField(max_length=200, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True)
    is_paid          = models.BooleanField(default=False)
    # Shipping address (copied from profile at time of order)
    shipping_name    = models.CharField(max_length=200)
    shipping_phone   = models.CharField(max_length=15)
    shipping_address = models.TextField()
    shipping_city    = models.CharField(max_length=100)
    shipping_state   = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=10)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order        = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity     = models.PositiveIntegerField()
    price_at_buy = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.price_at_buy * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
# Model for Solutions
class Solution(models.Model):
    solution_content_1 = models.CharField(max_length=500)
    solution_content_2 = models.CharField(max_length=500)

    def __str__(self):
        return 'Solutions'

# Model for Project Categories
class ProjectCategorie(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

# Model for Projects
class Project(models.Model):
    project_title = models.CharField(max_length=100)
    project_image = models.FileField(upload_to='project_images/')
    project_category = models.ForeignKey(ProjectCategorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_title
    
# Model for Blogs
class Blog(models.Model):
    blog_title = models.CharField(max_length=250)
    blog_content = models.CharField(max_length=500)
    blog_image = models.FileField(upload_to='blog_post_images/')
    blog_dateday = models.CharField(max_length=50, null=True, default='')
    blog_datemonth = models.CharField(max_length=50, null=True, default='')

    def __str__(self):
        return self.blog_title

# Model for Contact us
class ContactU(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# Model for Join us
class JoinU(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"








    
# Multiple images per project
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image   = models.FileField(upload_to='project_gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.project.project_title}"


# Product detail fields (add to existing Product or use this extended version)
class ProductDetail(models.Model):
    product     = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detail')
    description = models.TextField(blank=True)
    wattage     = models.CharField(max_length=50, blank=True)
    color_temp  = models.CharField(max_length=50, blank=True)
    ip_rating   = models.CharField(max_length=50, blank=True)
    dimensions  = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Detail — {self.product.product_name}"