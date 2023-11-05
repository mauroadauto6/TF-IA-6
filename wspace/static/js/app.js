document.addEventListener('DOMContentLoaded', function () {

    // Wait for the document to load before adding event listeners
    const purchaseButton = document.getElementById('purchase-button');

    purchaseButton.addEventListener('click', function () {
        // Create a new element for the popup message
        const popupMessage = document.createElement('div');
        popupMessage.className = 'popup-message';
        popupMessage.innerText = 'Purchase Completed';

        // Position the popup next to the purchase button
        const buttonRect = purchaseButton.getBoundingClientRect();
        popupMessage.style.top = buttonRect.top + 'px';
        popupMessage.style.left = (buttonRect.right + 10) + 'px';

        // Append the popup message to the document body
        document.body.appendChild(popupMessage);

        // Close the popup after a few seconds (adjust the time as needed)
        setTimeout(function () {
            popupMessage.style.display = 'none';
        }, 1500);
    });
});

function generateRandomPurchase() {
    const data = {
        'Unnamed: 0': Math.floor(Math.random() * 1000),
        'trans_date_trans_time': new Date().toISOString(),
        'cc_num': Math.floor(Math.random() * 10000000000000000),
        'merchant': 'Random Merchant ' + Math.floor(Math.random() * 100),
        'category': ['entertainment', 'food_dining', 'gas_transport', 'grocery_net', 'grocery_pos', 'health_fitness', 'home', 'kids_pets', 'misc_net', 'misc_pos', 'personal_care', 'shopping_net', 'shopping_pos', 'travel'][Math.floor(Math.random() * 14)],
        'amt': Math.random() * 100,
        'first': ['firstName', 'Pisos', 'Parque', 'Sociedad', 'Jairo', 'Mauro', 'Andy', 'David'][Math.floor(Math.random() * 8)],
        'last': ['lastName', 'Picados', 'Placentero', 'Sibarita', 'Calla', 'Adauto', 'Muñico', 'Niño'][Math.floor(Math.random() * 8)],
        'gender': Math.random() < 0.5 ? 'F' : 'M',
        'street': 'Random Street Address',
        'city': 'Random City',
        'state': 'Random State',
        'zip': Math.floor(Math.random() * 100000),
        'lat': Math.random() * 90,
        'long': Math.random() * 180,
        'city_pop': Math.floor(Math.random() * 100000),
        'job': 'Random Job',
        'dob': 'Random Date of Birth',
        'trans_num': 'Random Transaction Number',
        'unix_time': Math.floor(Date.now() / 1000),
        'merch_lat': Math.random() * 90,
        'merch_long': Math.random() * 180,
        'is_fraud': Math.random() < 0.1 ? 1 : 0, // 10% chance of fraud
    };
    return data;
}

function displayPurchaseData(purchaseData) {
    const purchaseList = document.getElementById('purchase-list');
    const listItem = document.createElement('li');
    listItem.innerText = JSON.stringify(purchaseData);
    purchaseList.appendChild(listItem);
}

document.addEventListener('DOMContentLoaded', function () {
    const purchaseButton = document.getElementById('purchase-button');
    purchaseButton.addEventListener('click', function () {
        specific_name = generateRandomPurchase().first;
        specific_last = generateRandomPurchase().last;
        specific_date = generateRandomPurchase().trans_date_trans_time;

        specific_data = [specific_name, specific_last, specific_date];
        const randomPurchase = specific_data;

        // Send the data to the server in the desired JSON format
        fetch('/save_purchase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'Unnamed: 0': 0,
                "trans_date_trans_time": specific_date,
                "cc_num": generateRandomPurchase().cc_num,
                "merchant": generateRandomPurchase().merchant,
                "category": generateRandomPurchase().category,
                "amt": generateRandomPurchase().amt,
                "first": specific_name,
                "last": specific_last,
                "gender": generateRandomPurchase().gender,
                "street": generateRandomPurchase().street,
                "city": generateRandomPurchase().city,
                "state": generateRandomPurchase().state,
                "zip": generateRandomPurchase().zip,
                "lat": generateRandomPurchase().lat,
                "long": generateRandomPurchase().long,
                "city_pop": generateRandomPurchase().city_pop,
                "job": generateRandomPurchase().job,
                "dob": generateRandomPurchase().dob,
                "trans_num": generateRandomPurchase().trans_num,
                "unix_time": generateRandomPurchase().unix_time,
                "merch_lat": generateRandomPurchase().merch_lat,
                "merch_long": generateRandomPurchase().merch_long,
                "is_fraud": generateRandomPurchase().is_fraud
            }),
        })
            .then(response => response.json())
            .catch(error => {
                console.error('Error:', error);
            });
        
        displayPurchaseData(randomPurchase);
    });
});