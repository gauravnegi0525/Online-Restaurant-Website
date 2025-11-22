// reservations.js
async function createReservation(reservationData) {
    try {
        const response = await authFetch('/api/reservations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reservationData),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create reservation');
        }

        return await response.json();
    } catch (error) {
        console.error('Reservation error:', error);
        throw error;
    }
}

async function getReservations() {
    try {
        const response = await authFetch('/api/reservations');

        if (!response.ok) {
            throw new Error('Failed to fetch reservations');
        }

        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Example usage in your reservation form
document.getElementById('reservation-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        guests: document.getElementById('guests').value,
        specialRequests: document.getElementById('special-requests').value,
    };

    try {
        const reservation = await createReservation(formData);
        // Show success message
        alert('Reservation created successfully!');
        // Optionally redirect or clear form
        this.reset();
    } catch (error) {
        alert(error.message);
    }
});