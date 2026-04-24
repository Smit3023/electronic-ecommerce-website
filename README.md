# 🛒 Electronics E-Commerce Website

> A full-stack e-commerce web application for an electronics/lighting company — built with **Django** — featuring a product catalog, shopping cart, Razorpay payment integration, user authentication, blog, and an admin dashboard.

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Application Flow](#-application-flow)
- [Database Models](#-database-models)
- [Getting Started](#-getting-started)
- [Admin Access](#-admin-access)
- [Environment Variables](#-environment-variables)

---

## 📖 About the Project

This is a **production-ready e-commerce platform** built for an electronics/lighting company (IEPL). Users can browse products, add them to a cart, place orders via **Razorpay payment gateway**, and track their order history — all through a clean, content-managed web interface.

The platform is also a **content website**, meaning the company can manage pages like About Us, Projects, Blogs, Solutions, and team members directly from the Django admin panel.

---

## 🧰 Tech Stack

| Layer        | Technology                    |
|--------------|-------------------------------|
| Backend      | Python 3.10+, Django          |
| Database     | SQLite (dev) / PostgreSQL (prod ready) |
| Payments     | Razorpay API                  |
| Email        | Django `send_mail` (SMTP)     |
| Frontend     | Django Templates, HTML/CSS    |
| Media Files  | Django `MEDIA_ROOT` file uploads |

---

## ✅ Features

### 🛍️ E-Commerce
- Product catalog with categories (Bulbs, Panels, Fixtures, Strip Lights, Outdoor, etc.)
- Product detail pages with slug-based URLs
- Shopping cart (add, update quantity, remove items)
- Checkout with shipping address form
- **Razorpay payment gateway** integration
- Payment signature verification for security
- Order confirmation with email notification
- Stock management (auto-decrements on successful order)

### 👤 User Authentication
- Register, Login, Logout
- User profile page with editable shipping address
- Order history on profile page
- Login required for cart and checkout

### 📋 Content Management (via Admin)
- Homepage slider images
- About Us content and images
- Product categories
- Projects (with gallery images, grouped by category)
- Blog posts (with pagination)
- Testimonials, Partners, Clients, Founders
- Solutions page content
- Contact form submissions
- Job applications (with resume upload)

### 🔍 Other
- Site-wide search (across products, projects, blogs)
- Contact Us form with email notification to admin
- Join Us / Career application form

---

## 📁 Project Structure

```
electronic-ecommerce-website-main/
│
├── ieplproject/                  # Django root project
│   ├── ieplproject/              # Project settings & URLs
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── .env                  # Environment variables
│   │
│   ├── ieplapp/                  # Main application
│   │   ├── models.py             # All data models
│   │   ├── views.py              # All page & API views
│   │   ├── urls.py               # URL routing
│   │   ├── forms.py              # Contact & Join forms
│   │   ├── admin.py              # Admin panel configuration
│   │   └── migrations/           # Database migrations
│   │
│   ├── accounts/                 # Authentication app
│   │   ├── models.py             # UserProfile model
│   │   ├── views.py              # Register, Login, Logout, Profile
│   │   ├── urls.py               # Auth URL routing
│   │   └── forms.py              # Registration form
│   │
│   └── db.sqlite3                # SQLite database
```

---

## 🔄 Application Flow

### 🛒 Customer Purchase Flow

```
Home Page
   │
   ├──▶ Products Page (paginated, category filtered)
   │         │
   │         └──▶ Product Detail Page
   │                    │
   │                    └──▶ Add to Cart  ──▶ [Login Required]
   │
   └──▶ Cart Page
              │
              └──▶ Checkout Page (enter shipping address)
                        │
                        └──▶ Razorpay Payment Gateway
                                    │
                              ┌─────┴──────┐
                              │            │
                           Success       Failure
                              │            │
                        Order Confirmed   Redirect to Cart
                        Email Sent        Error Message
                        Stock Updated
```

### 👤 Authentication Flow

```
Register ──▶ UserProfile auto-created ──▶ Login
   │
   └──▶ Profile Page
              ├── Edit shipping address
              └── View order history
```

### 📞 Contact / Career Flow

```
Contact Us Form ──▶ Saved to DB ──▶ Email sent to Admin
Join Us Form    ──▶ Saved to DB ──▶ Resume uploaded ──▶ Email sent to Admin
```

---

## 🗄️ Database Models

| Model            | Purpose                                          |
|------------------|--------------------------------------------------|
| `Product`        | Electronics product with price, stock, category  |
| `Cart`           | One cart per logged-in user                      |
| `CartItem`       | Products in cart with quantity                   |
| `Order`          | Placed order with shipping address & status      |
| `OrderItem`      | Individual items in an order with price snapshot |
| `UserProfile`    | Extended user data (phone, address, profile pic) |
| `AboutU`         | About Us page content                            |
| `Categorie`      | Product category showcase                        |
| `Project`        | Completed project with gallery images            |
| `Blog`           | Blog posts with date                             |
| `Testimonial`    | Customer testimonials                            |
| `ContactU`       | Contact form submissions                         |
| `JoinU`          | Job applications with resume                     |
| `Founder`        | Team/founder profiles                            |
| `Partner`/`Client` | Partner and client logos                       |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/electronic-ecommerce-website.git
cd electronic-ecommerce-website/ieplproject

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables (see section below)

# 5. Apply migrations
python manage.py migrate

# 6. Run the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## 🔑 Admin Access

Access the Django admin panel at **http://127.0.0.1:8000/admin/**

| Field    | Value            |
|----------|------------------|
| Username | `interiorlights` |
| Password | `interiorlights` |

---

## ⚙️ Environment Variables

Create a `.env` file inside the `ieplproject/` folder:

```env
SECRET_KEY=your-django-secret-key

# Razorpay Payment Gateway
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=admin-notify@gmail.com
```

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
