document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', function () {
        this.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    // Shopping Cart Functionality
    const cartBtn = document.getElementById('cart-btn');
    const cartSidebar = document.getElementById('cart-sidebar');
    const closeCart = document.getElementById('close-cart');
    const cartOverlay = document.getElementById('cart-overlay');
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const cartCount = document.querySelector('.cart-count');

    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Open/Close Cart
    cartBtn.addEventListener('click', () => {
        cartSidebar.classList.add('active');
        cartOverlay.classList.add('active');
        updateCart();
    });

    closeCart.addEventListener('click', () => {
        cartSidebar.classList.remove('active');
        cartOverlay.classList.remove('active');
    });

    cartOverlay.addEventListener('click', () => {
        cartSidebar.classList.remove('active');
        cartOverlay.classList.remove('active');
    });

    // Add to Cart buttons
    document.querySelectorAll('.btn-add').forEach(button => {
        button.addEventListener('click', function () {
            const offerCard = this.closest('.offer-card');

            const item = {
                id: Date.now(),
                title: offerCard.querySelector('h3').textContent,
                price: parseFloat(offerCard.querySelector('.price').textContent.replace(/[^\d.]/g, '')),
                image: offerCard.querySelector('img').src,
                quantity: 1
            };

            // Check if item already exists in cart
            const existingItem = cart.find(cartItem => cartItem.title === item.title);

            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push(item);
            }

            updateCart();
            showAddToCartAnimation(this);
        });
    });

    // Update Cart Function
    function updateCart() {
        localStorage.setItem('cart', JSON.stringify(cart));

        // Update cart count
        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        cartCount.textContent = totalItems;

        // Update cart items
        cartItemsContainer.innerHTML = '';

        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
            cartTotal.textContent = '$0.00';
            return;
        }

        let total = 0;

        cart.forEach(item => {
            total += item.price * item.quantity;

            const cartItemElement = document.createElement('div');
            cartItemElement.className = 'cart-item';

            cartItemElement.innerHTML = `
                <img src="${item.image}" alt="${item.title}">
                <div class="cart-item-details">
                    <div class="cart-item-title">${item.title}</div>
                    <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                    <button class="cart-item-remove">Remove</button>
                    <div class="cart-item-quantity">
                        <button class="quantity-btn minus">-</button>
                        <input type="number" class="quantity-input" value="${item.quantity}" min="1">
                        <button class="quantity-btn plus">+</button>
                    </div>
                </div>
            `;

            cartItemsContainer.appendChild(cartItemElement);

            // Add event listeners for quantity buttons
            const minusBtn = cartItemElement.querySelector('.minus');
            const plusBtn = cartItemElement.querySelector('.plus');
            const quantityInput = cartItemElement.querySelector('.quantity-input');
            const removeBtn = cartItemElement.querySelector('.cart-item-remove');

            minusBtn.addEventListener('click', () => {
                if (item.quantity > 1) {
                    item.quantity--;
                    quantityInput.value = item.quantity;
                    updateCart();
                }
            });

            plusBtn.addEventListener('click', () => {
                item.quantity++;
                quantityInput.value = item.quantity;
                updateCart();
            });

            quantityInput.addEventListener('change', () => {
                const newQuantity = parseInt(quantityInput.value);
                if (newQuantity >= 1) {
                    item.quantity = newQuantity;
                    updateCart();
                }
            });

            removeBtn.addEventListener('click', () => {
                cart = cart.filter(cartItem => cartItem.id !== item.id);
                updateCart();
            });
        });

        cartTotal.textContent = `$${total.toFixed(2)}`;
    }

    // Add to Cart Animation
    function showAddToCartAnimation(button) {
        const animation = document.createElement('div');
        animation.className = 'add-to-cart-animation';
        animation.innerHTML = '<i class="fas fa-check"></i> Added to Cart';

        const rect = button.getBoundingClientRect();

        animation.style.left = `${rect.left + window.scrollX}px`;
        animation.style.top = `${rect.top + window.scrollY}px`;

        document.body.appendChild(animation);

        setTimeout(() => {
            animation.style.opacity = '0';
            animation.style.transform = 'translateY(-20px)';
        }, 100);

        setTimeout(() => {
            animation.remove();
        }, 1000);
    }

    // Add CSS for animation
    const style = document.createElement('style');
    style.textContent = `
        .add-to-cart-animation {
            position: fixed;
            background-color: #2d6a4f;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            z-index: 1000;
            pointer-events: none;
            transition: all 0.5s ease;
            opacity: 1;
        }
        .add-to-cart-animation i {
            margin-right: 5px;
        }
    `;
    document.head.appendChild(style);

    // Reservation Modal
    const reservationBtn = document.querySelector('.btn-reservation');
    const reservationModal = document.getElementById('reservation-modal');
    const closeModal = document.querySelector('.close-modal');

    reservationBtn.addEventListener('click', () => {
        reservationModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    });

    closeModal.addEventListener('click', () => {
        reservationModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    window.addEventListener('click', (e) => {
        if (e.target === reservationModal) {
            reservationModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Reservation Form
    const reservationForm = document.getElementById('reservation-form');

    reservationForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const guests = document.getElementById('guests').value;

        // Here you would typically send this data to a server
        console.log('Reservation Details:', {
            name,
            email,
            phone,
            date,
            time,
            guests
        });

        // Show success message
        alert(`Thank you, ${name}! Your reservation for ${guests} on ${date} at ${time} has been received. We'll send a confirmation to ${email}.`);

        // Close modal and reset form
        reservationModal.style.display = 'none';
        document.body.style.overflow = 'auto';
        reservationForm.reset();
    });

    // Newsletter Form
    const newsletterForm = document.getElementById('newsletter-form');

    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input').value;

        // Here you would typically send this to a server
        console.log('Newsletter Subscription:', email);

        // Show success message
        alert(`Thank you for subscribing with ${email}! You'll receive our newsletter soon.`);

        // Reset form
        newsletterForm.reset();
    });

    // Set minimum date for reservation (today)
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').min = today;

    // Initialize cart on page load
    updateCart();
});