# MyShop — Django E-Commerce Starter

A working online shop built with Django: product catalog with categories/search,
session-based cart, checkout, user accounts, and order history — styled with a
soft pastel "handmade shop" look.

## 1. Project layout

```
shopsite/
├── manage.py
├── requirements.txt
├── shopsite/        # project settings & root urls.py
├── store/           # Category, Product models + catalog views
├── cart/            # session-based shopping cart
├── orders/          # checkout + order history
├── accounts/        # signup/login/logout (built on Django's auth)
├── templates/        # all HTML templates
└── static/css/style.css
```

Each app is intentionally separate — this mirrors how real Django projects are
organized, and makes each piece easy to explain in a presentation or a report:
- **store** = what you're selling
- **cart** = what's currently in the visitor's basket (stored in their session)
- **orders** = what happens after checkout (a permanent record tied to a user)
- **accounts** = who is buying

## 2. Setup (run these in order)

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database tables
python manage.py migrate

# 4. Create an admin account (for /admin/)
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## 3. Add your first products

Go to http://127.0.0.1:8000/admin/, log in with the superuser you created, and:
1. Add a **Category** (e.g. "Charms").
2. Add a **Product** — give it a name, price, stock count, and upload an image.
   The slug field auto-fills from the name.

Products show up immediately on the storefront.

## 4. How each feature works (for your report / defense)

- **Catalog & search** (`store/views.py`): `product_list` filters by category
  slug and/or a `?q=` search query, then paginates results 12 per page.
- **Cart** (`cart/cart.py`): a plain Python class that reads/writes a
  dictionary in `request.session`. No database table needed — it disappears
  when the session ends, which is standard for shopping carts.
- **Checkout** (`orders/views.py`): `order_create` is `@login_required` —
  guests are redirected to log in first. On submit, it copies every cart line
  into permanent `Order`/`OrderItem` rows, then clears the cart.
- **Order history** (`orders/views.py`): `order_history` lists only the
  logged-in user's own orders (`Order.objects.filter(user=request.user)`).
- **Accounts**: uses Django's built-in `django.contrib.auth` — `SignUpForm`
  just extends `UserCreationForm` to also require an email.

## 5. Natural next steps

- Add real payment processing (e.g. PayPal or a local payment gateway) inside
  `orders/views.py::order_create`.
- Add product reviews/ratings as a new small app.
- Add an "order status" email notification when status changes to "shipped".
- Deploy: this runs as-is on Render, Railway, or PythonAnywhere — just set
  `DEBUG = False` and a proper `ALLOWED_HOSTS` / `SECRET_KEY` in `settings.py`
  first.
