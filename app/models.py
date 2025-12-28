from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    """User model for both customers and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Ingredient(db.Model):
    """Ingredient model"""
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, default=0.0)  # Price per unit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    burger_ingredients = db.relationship('BurgerIngredient', backref='ingredient', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'

class Burger(db.Model):
    """Burger menu item model"""
    __tablename__ = 'burgers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ingredients = db.relationship('BurgerIngredient', backref='burger', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='burger', lazy=True)
    cart_items = db.relationship('CartItem', backref='burger', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Burger {self.name}>'

class BurgerIngredient(db.Model):
    """Association table for burgers and ingredients"""
    __tablename__ = 'burger_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    burger_id = db.Column(db.Integer, db.ForeignKey('burgers.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.Float, default=1.0)
    
    __table_args__ = (db.UniqueConstraint('burger_id', 'ingredient_id', name='uq_burger_ingredient'),)

class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, ready, delivered, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    stripe_payment_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    """Individual item in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    burger_id = db.Column(db.Integer, db.ForeignKey('burgers.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.burger_id} x{self.quantity}>'

class CartItem(db.Model):
    """Shopping cart item"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    burger_id = db.Column(db.Integer, db.ForeignKey('burgers.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'burger_id', name='uq_user_burger_cart'),)
    
    def __repr__(self):
        return f'<CartItem user={self.user_id} burger={self.burger_id}>'
