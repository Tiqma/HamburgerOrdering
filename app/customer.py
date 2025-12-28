from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Burger, CartItem, Order, OrderItem

customer_bp = Blueprint('customer', __name__, url_prefix='/shop')

@customer_bp.route('/')
@customer_bp.route('/dashboard')
@login_required
def dashboard():
    """Customer dashboard - browse burgers"""
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    burgers = Burger.query.paginate(page=page, per_page=12)
    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return render_template('customer/dashboard.html', burgers=burgers, cart_count=cart_count)

@customer_bp.route('/burger/<int:burger_id>')
@login_required
def burger_detail(burger_id):
    """View burger details"""
    burger = Burger.query.get_or_404(burger_id)
    return render_template('customer/burger_detail.html', burger=burger)

@customer_bp.route('/cart')
@login_required
def view_cart():
    """View shopping cart"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.burger.price * item.quantity for item in cart_items)
    
    return render_template('customer/cart.html', cart_items=cart_items, total=total)

@customer_bp.route('/cart/add/<int:burger_id>', methods=['POST'])
@login_required
def add_to_cart(burger_id):
    """Add burger to cart"""
    burger = Burger.query.get_or_404(burger_id)
    
    if not burger.is_available:
        flash('This burger is not available', 'warning')
        return redirect(url_for('customer.dashboard'))
    
    quantity = request.form.get('quantity', 1, type=int)
    if quantity < 1:
        quantity = 1
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, burger_id=burger_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, burger_id=burger_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'Added {burger.name} to cart!', 'success')
    return redirect(url_for('customer.view_cart'))

@customer_bp.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('customer.view_cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'info')
    return redirect(url_for('customer.view_cart'))

@customer_bp.route('/cart/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart(cart_item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    quantity = request.json.get('quantity', 1)
    
    if quantity < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    return jsonify({'success': True})

@customer_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout and create order"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('customer.view_cart'))
    
    if request.method == 'POST':
        total_price = sum(item.burger.price * item.quantity for item in cart_items)
        
        # Create order
        order = Order(user_id=current_user.id, total_price=total_price, status='pending')
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                burger_id=cart_item.burger_id,
                quantity=cart_item.quantity,
                price_at_order=cart_item.burger.price
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        flash('Order created! Proceeding to payment...', 'success')
        return redirect(url_for('customer.payment', order_id=order.id))
    
    total = sum(item.burger.price * item.quantity for item in cart_items)
    return render_template('customer/checkout.html', cart_items=cart_items, total=total)

@customer_bp.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment(order_id):
    """Payment page (using Stripe)"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('customer.dashboard'))
    
    if request.method == 'POST':
        # In production, integrate with Stripe here
        # For now, simulate successful payment
        order.payment_status = 'completed'
        order.status = 'confirmed'
        db.session.commit()
        
        flash('Payment successful! Your order has been confirmed.', 'success')
        return redirect(url_for('customer.orders'))
    
    return render_template('customer/payment.html', order=order)

@customer_bp.route('/orders')
@login_required
def orders():
    """View customer orders"""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('customer/orders.html', orders=orders)

@customer_bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """View order details"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('customer.orders'))
    
    return render_template('customer/order_detail.html', order=order)
