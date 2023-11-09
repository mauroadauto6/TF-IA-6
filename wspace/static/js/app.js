function generateRandomPurchase() {
    const randomDateTime = () => {
        const y = 2019; 
        const y2 = 2024;  
        const year = y + Math.floor(Math.random() * (y2 - y + 1));
        const month = 1 + Math.floor(Math.random() * 12); 
        const day = 1 + Math.floor(Math.random() * 28); 
        const hours = Math.floor(Math.random() * 24); 
        const minutes = Math.floor(Math.random() * 60); 
        const seconds = Math.floor(Math.random() * 60); 

        return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')} ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
    return {
        'Unnamed: 0': Math.floor(Math.random() * 1000),
        'trans_date_trans_time': randomDateTime(), 
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
        'is_fraud': Math.random() < 0.35 ? 1 : 0, // 35% chance of fraud
    };
}

function displayPurchaseData(purchaseData) {
    const purchaseList = document.getElementById('purchase-list');
    const listItem = document.createElement('li');
    listItem.innerText = JSON.stringify(purchaseData);
    purchaseList.appendChild(listItem);
}

document.addEventListener('DOMContentLoaded', function () {
    function generatePurchase(){
        const randomPurchase = generateRandomPurchase();

        specific_name = randomPurchase.first;
        specific_last = randomPurchase.last;
        specific_date = randomPurchase.trans_date_trans_time;

        specific_data = [specific_name, specific_last, specific_date];

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

        displayPurchaseData(specific_data);
    }
    
    function generatePurchaseInterval() {
        setInterval(generatePurchase, 2500);
    }
    
    generatePurchaseInterval();
});


