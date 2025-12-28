import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app, db
from app.models import User, Burger, Ingredient, BurgerIngredient

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Burger': Burger, 'Ingredient': Ingredient}

@app.cli.command()
def init_db():
    """Initialize the database with sample data."""
    db.create_all()
    
    # Create sample ingredients
    ingredients_data = [
        ('Beef Patty', 3.00),
        ('Tomato', 0.50),
        ('Lettuce', 0.30),
        ('Cheese', 0.75),
        ('Onion', 0.25),
        ('Pickle', 0.20),
        ('Bacon', 1.00),
        ('Mushroom', 0.60),
        ('Mayo', 0.15),
        ('Ketchup', 0.10),
    ]
    
    for name, price in ingredients_data:
        if not Ingredient.query.filter_by(name=name).first():
            ingredient = Ingredient(name=name, price=price)
            db.session.add(ingredient)
    
    db.session.commit()
    
    # Create sample burgers
    burgers_data = [
        {
            'name': 'Classic Hamburger',
            'description': 'A timeless burger with beef patty, tomato, lettuce, and onion',
            'price': 8.99,
            'ingredients': ['Beef Patty', 'Tomato', 'Lettuce', 'Onion', 'Ketchup']
        },
        {
            'name': 'Cheese Burger',
            'description': 'Classic burger topped with melted cheddar cheese',
            'price': 9.99,
            'ingredients': ['Beef Patty', 'Cheese', 'Tomato', 'Lettuce', 'Onion']
        },
        {
            'name': 'Bacon Burger',
            'description': 'Juicy burger with crispy bacon and cheese',
            'price': 11.99,
            'ingredients': ['Beef Patty', 'Bacon', 'Cheese', 'Tomato', 'Lettuce']
        },
        {
            'name': 'Mushroom Swiss',
            'description': 'Burger with sautéed mushrooms and swiss cheese',
            'price': 10.99,
            'ingredients': ['Beef Patty', 'Mushroom', 'Cheese', 'Lettuce', 'Tomato']
        },
        {
            'name': 'Deluxe Burger',
            'description': 'The ultimate burger with all the toppings',
            'price': 12.99,
            'ingredients': ['Beef Patty', 'Bacon', 'Cheese', 'Tomato', 'Lettuce', 'Onion', 'Pickle', 'Mushroom']
        },
    ]
    
    for burger_data in burgers_data:
        if not Burger.query.filter_by(name=burger_data['name']).first():
            burger = Burger(
                name=burger_data['name'],
                description=burger_data['description'],
                price=burger_data['price']
            )
            db.session.add(burger)
            db.session.flush()
            
            for ing_name in burger_data['ingredients']:
                ingredient = Ingredient.query.filter_by(name=ing_name).first()
                if ingredient:
                    bi = BurgerIngredient(burger_id=burger.id, ingredient_id=ingredient.id, quantity=1)
                    db.session.add(bi)
    
    db.session.commit()
    
    # Create sample admin user
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            full_name='Admin User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✓ Admin user created: admin@example.com / admin123')
    
    print('✓ Database initialized with sample data!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
