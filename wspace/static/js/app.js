function displayTransaction(transaction) {
    const transList = document.getElementById('trans-list');

    const transItem = document.createElement('li');
    
    transItem.innerText = JSON.stringify(transaction);
    
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
        setInterval(obtainTransaction, 2500);
    }
    
    transactionInterval();
});

