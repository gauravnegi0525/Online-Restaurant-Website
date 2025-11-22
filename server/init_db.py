from server.app import app, db

with app.app_context():
    # Create all database tables
    db.create_all()

    # Import models
    from server.models.models import User, MenuItem

    # Create admin user if not exists
    admin_email = 'admin@example.com'
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            name='Admin',
            email=admin_email,
            password='admin123',  # Password will be hashed in User model's __init__
            phone='1234567890',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{admin_email}' created.")
    else:
        print(f"Admin user '{admin_email}' already exists.")

    # Add some sample menu items if the table is empty
    sample_items = [
        {
            'name': 'Truffle Pasta',
            'description': 'Handmade pasta with black truffle and parmesan',
            'price': 24.99,
            'category': 'main',
            'image': 'truffle-pasta.jpg',
            'is_featured': True
        },
        {
            'name': 'Grilled Salmon',
            'description': 'Fresh Atlantic salmon with lemon butter sauce',
            'price': 28.99,
            'category': 'main',
            'image': 'grilled-salmon.jpg',
            'is_featured': True
        },
        # Add more items as needed
    ]

    added_count = 0
    for item_data in sample_items:
        if not MenuItem.query.filter_by(name=item_data['name']).first():
            item = MenuItem(**item_data)
            db.session.add(item)
            added_count += 1

    if added_count > 0:
        db.session.commit()
        print(f"{added_count} sample menu item(s) added.")
    else:
        print("Sample menu items already exist.")

    print("Database initialized successfully!")