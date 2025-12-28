from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Burger, Ingredient, BurgerIngredient, Order

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('customer.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard"""
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    total_revenue = sum(o.total_price for o in Order.query.all() if o.payment_status == 'completed')
    
    burgers = Burger.query.all()
    unavailable_burgers = Burger.query.filter_by(is_available=False).count()
    
    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_revenue=total_revenue,
                         total_burgers=len(burgers),
                         unavailable_burgers=unavailable_burgers)

# ===== BURGER MANAGEMENT =====
@admin_bp.route('/burgers')
@admin_required
def list_burgers():
    """List all burgers"""
    page = request.args.get('page', 1, type=int)
    burgers = Burger.query.paginate(page=page, per_page=20)
    return render_template('admin/burgers.html', burgers=burgers)

@admin_bp.route('/burger/add', methods=['GET', 'POST'])
@admin_required
def add_burger():
    """Add new burger"""
    ingredients = Ingredient.query.all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price', type=float)
        
        if not name or not price:
            flash('Name and price are required', 'danger')
            return render_template('admin/add_burger.html', ingredients=ingredients)
        
        burger = Burger(name=name, description=description, price=price)
        db.session.add(burger)
        db.session.flush()
        
        # Add ingredients
        ingredient_ids = request.form.getlist('ingredients')
        for ing_id in ingredient_ids:
            try:
                quantity = float(request.form.get(f'quantity_{ing_id}', 1))
                bi = BurgerIngredient(burger_id=burger.id, ingredient_id=int(ing_id), quantity=quantity)
                db.session.add(bi)
            except (ValueError, TypeError):
                continue
        
        db.session.commit()
        flash(f'Burger "{name}" added successfully!', 'success')
        return redirect(url_for('admin.list_burgers'))
    
    return render_template('admin/add_burger.html', ingredients=ingredients)

@admin_bp.route('/burger/<int:burger_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_burger(burger_id):
    """Edit burger"""
    burger = Burger.query.get_or_404(burger_id)
    ingredients = Ingredient.query.all()
    
    if request.method == 'POST':
        burger.name = request.form.get('name', burger.name)
        burger.description = request.form.get('description', burger.description)
        burger.price = request.form.get('price', burger.price, type=float)
        
        # Update ingredients
        BurgerIngredient.query.filter_by(burger_id=burger_id).delete()
        
        ingredient_ids = request.form.getlist('ingredients')
        for ing_id in ingredient_ids:
            try:
                quantity = float(request.form.get(f'quantity_{ing_id}', 1))
                bi = BurgerIngredient(burger_id=burger.id, ingredient_id=int(ing_id), quantity=quantity)
                db.session.add(bi)
            except (ValueError, TypeError):
                continue
        
        db.session.commit()
        flash(f'Burger "{burger.name}" updated!', 'success')
        return redirect(url_for('admin.list_burgers'))
    
    return render_template('admin/edit_burger.html', burger=burger, ingredients=ingredients)

@admin_bp.route('/burger/<int:burger_id>/toggle-availability', methods=['POST'])
@admin_required
def toggle_burger_availability(burger_id):
    """Toggle burger availability"""
    burger = Burger.query.get_or_404(burger_id)
    burger.is_available = not burger.is_available
    db.session.commit()
    
    status = "available" if burger.is_available else "unavailable"
    flash(f'Burger "{burger.name}" marked as {status}.', 'success')
    return redirect(url_for('admin.list_burgers'))

@admin_bp.route('/burger/<int:burger_id>/delete', methods=['POST'])
@admin_required
def delete_burger(burger_id):
    """Delete burger"""
    burger = Burger.query.get_or_404(burger_id)
    name = burger.name
    db.session.delete(burger)
    db.session.commit()
    flash(f'Burger "{name}" deleted.', 'success')
    return redirect(url_for('admin.list_burgers'))

# ===== INGREDIENT MANAGEMENT =====
@admin_bp.route('/ingredients')
@admin_required
def list_ingredients():
    """List all ingredients"""
    page = request.args.get('page', 1, type=int)
    ingredients = Ingredient.query.paginate(page=page, per_page=20)
    return render_template('admin/ingredients.html', ingredients=ingredients)

@admin_bp.route('/ingredient/add', methods=['GET', 'POST'])
@admin_required
def add_ingredient():
    """Add new ingredient"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price', 0, type=float)
        
        if not name:
            flash('Name is required', 'danger')
            return render_template('admin/add_ingredient.html')
        
        ingredient = Ingredient(name=name, price=price)
        db.session.add(ingredient)
        db.session.commit()
        flash(f'Ingredient "{name}" added!', 'success')
        return redirect(url_for('admin.list_ingredients'))
    
    return render_template('admin/add_ingredient.html')

@admin_bp.route('/ingredient/<int:ingredient_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_ingredient(ingredient_id):
    """Edit ingredient"""
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    
    if request.method == 'POST':
        ingredient.name = request.form.get('name', ingredient.name)
        ingredient.price = request.form.get('price', ingredient.price, type=float)
        db.session.commit()
        flash(f'Ingredient "{ingredient.name}" updated!', 'success')
        return redirect(url_for('admin.list_ingredients'))
    
    return render_template('admin/edit_ingredient.html', ingredient=ingredient)

@admin_bp.route('/ingredient/<int:ingredient_id>/toggle-availability', methods=['POST'])
@admin_required
def toggle_ingredient_availability(ingredient_id):
    """Toggle ingredient availability"""
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    ingredient.is_available = not ingredient.is_available
    db.session.commit()
    
    status = "available" if ingredient.is_available else "unavailable"
    flash(f'Ingredient "{ingredient.name}" marked as {status}.', 'success')
    return redirect(url_for('admin.list_ingredients'))

@admin_bp.route('/ingredient/<int:ingredient_id>/delete', methods=['POST'])
@admin_required
def delete_ingredient(ingredient_id):
    """Delete ingredient"""
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    name = ingredient.name
    db.session.delete(ingredient)
    db.session.commit()
    flash(f'Ingredient "{name}" deleted.', 'success')
    return redirect(url_for('admin.list_ingredients'))

# ===== ORDER MANAGEMENT =====
@admin_bp.route('/orders')
@admin_required
def list_orders():
    """List all orders"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    
    query = Order.query
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders, current_status=status)

@admin_bp.route('/order/<int:order_id>')
@admin_required
def view_order(order_id):
    """View order details"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/order/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled']
    if new_status not in valid_statuses:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin.view_order', order_id=order_id))
    
    order.status = new_status
    db.session.commit()
    flash(f'Order #{order.id} status updated to {new_status}.', 'success')
    return redirect(url_for('admin.view_order', order_id=order_id))
