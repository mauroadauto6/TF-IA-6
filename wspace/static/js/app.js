index = 1;

function displayTransaction(transaction) {
    const transList = document.getElementById('trans-list');

    const transItem = document.createElement('li');
    const transactionString = `TransIndex: ${index}, Name: ${transaction.Name}, Last: ${transaction.Last}, TransCategory: ${transaction.TransCategory}, State: ${transaction.State}`;
    
    index = index + 1;
    transItem.innerText = transactionString;
    
    transList.insertBefore(transItem, transList.firstChild);
}

document.addEventListener('DOMContentLoaded', function (){
    function obtainTransaction() {
        fetch('/getTransRow')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`ERROR: ${response.statusText}`);
                }
                return response.json();
            })
            .then(transaction => {
                displayTransaction(transaction);
            })
            .catch(error => {
                console.error('ERROR', error);
            });
    }

    function transactionInterval() {
        setInterval(obtainTransaction, 4500);
    }
    
    transactionInterval();
});

