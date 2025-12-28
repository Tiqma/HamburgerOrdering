# Hamburger Shop - Full-Stack Flask Application

A complete food ordering website built with **Flask**, **SQLAlchemy**, and **SQLite**. Features separate systems for customers and administrators.

## Features

### Customer Features
- 🛒 Browse and order hamburgers
- 🛒 Shopping cart management
- 💳 Payment processing (Stripe integration ready)
- 📋 Order history and tracking
- 🔐 User authentication

### Admin Features  
- 🍔 Manage hamburger menu (add, edit, delete)
- ⚠️ Mark burgers as unavailable
- 🥒 Manage ingredients (add, edit, delete)
- ⚠️ Mark ingredients as missing/unavailable
- 📊 View all orders and customer information
- 📈 Update order status (pending → confirmed → preparing → ready → delivered)
- 💰 Track revenue and order statistics

## Tech Stack

- **Backend:** Flask 2.3.3
- **Database:** SQLAlchemy with SQLite
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF
- **Frontend:** Bootstrap 5
- **Payment:** Stripe (test mode)

## Project Structure

```
hamburger-shop/
├── app/
│   ├── models.py              # Database models
│   ├── auth.py                # Authentication routes
│   ├── auth_forms.py          # Login/Register forms
│   ├── customer.py            # Customer routes
│   ├── admin.py               # Admin routes
│   ├── __init__.py            # Flask app factory
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── customer/
│   │   └── admin/
│   └── static/
│       └── css/style.css
├── config.py                  # App configuration
├── run.py                     # Entry point + CLI commands
└── requirements.txt
```

## Installation & Setup

### 1. Install Dependencies

```bash
cd hamburger-shop
pip install -r requirements.txt
```

### 2. Start the Server (Database Initializes Automatically)

**Option A - Recommended (Python script):**
```bash
python start.py
```

**Option B - Using Flask directly:**
```bash
python run.py
```

**Option C - Using bash script:**
```bash
bash startup.sh
```

The server will automatically:
- Create the SQLite database
- Add 10 sample ingredients
- Add 5 sample burgers
- Create the admin account

### 3. Access the Application

Visit: **http://localhost:5000**

The app will redirect you to login if not authenticated.

## Default Accounts

### Admin Account
- **Email:** admin@example.com
- **Password:** admin123
- **Access:** Admin panel to manage burgers, ingredients, and orders

### Create Customer Accounts
Register new customer accounts via the website signup page.

## Database Models

### User
- Username, Email, Password (hashed)
- Full Name
- Admin flag
- Relationships: Orders, Cart Items

### Burger
- Name, Description, Price
- Availability status
- Associated ingredients
- Relationships: Order Items, Cart Items

### Ingredient
- Name, Price
- Availability status (for marking missing items)
- Relationships: Burger associations

### Order
- Customer reference
- Total price, Status, Payment status
- Order date & timestamps
- Relationships: Order Items

### CartItem
- User reference
- Burger reference
- Quantity

## API Routes

### Authentication
- `GET/POST /auth/login` - Login
- `GET/POST /auth/register` - Register
- `GET /auth/logout` - Logout

### Customer
- `GET /shop/` - Browse burgers
- `GET /shop/burger/<id>` - Burger details
- `GET/POST /shop/cart` - Shopping cart
- `POST /shop/cart/add/<id>` - Add to cart
- `POST /shop/cart/remove/<id>` - Remove from cart
- `GET/POST /shop/checkout` - Checkout
- `GET/POST /shop/payment/<order_id>` - Payment
- `GET /shop/orders` - Order history
- `GET /shop/order/<id>` - Order details

### Admin
- `GET /admin/` - Dashboard
- `GET /admin/burgers` - Burger list
- `GET/POST /admin/burger/add` - Add burger
- `GET/POST /admin/burger/<id>/edit` - Edit burger
- `POST /admin/burger/<id>/toggle-availability` - Toggle burger availability
- `GET /admin/ingredients` - Ingredient list
- `GET/POST /admin/ingredient/add` - Add ingredient
- `POST /admin/ingredient/<id>/toggle-availability` - Mark ingredient missing/available
- `GET /admin/orders` - Orders list
- `POST /admin/order/<id>/status` - Update order status

## Configuration

Edit `config.py` to customize:
- Database URL
- Secret key (use strong key in production)
- Stripe API keys
- Session settings

## Features to Enhance

- [ ] Email notifications on order status changes
- [ ] Real Stripe payment integration
- [ ] Order ratings and reviews
- [ ] Special discounts and coupons
- [ ] Inventory management system
- [ ] Multi-location support
- [ ] Mobile app API (REST/GraphQL)
- [ ] Admin analytics dashboard

## License

MIT
