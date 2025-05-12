var newQuantity = 1;
document.addEventListener('DOMContentLoaded', function () {

    var unitButtons = document.querySelectorAll('.unit-button');
    
    var priceButtons = document.querySelectorAll('.price-button');
    var addToCartButton = document.querySelector('.btn-addtocart');
   
    var selectedUnit = null;
    var selectedSize = null;
    var response = null;
    unitButtons.forEach(function (unitButton) {
        unitButton.addEventListener('click', function () {
            selectedUnit = this.getAttribute('data-unit');
            updateSelected(this, unitButtons);
            updateProductInfo();
        });
    });

    

    function updateSelected(clickedButton, allButtons) {
        allButtons.forEach(function (button) {
            button.classList.remove('clicked');
        });

        clickedButton.classList.add('clicked');
    }

    function updateProductInfo() {
        if (selectedUnit) {
            console.log('Selected Unit:', selectedUnit);
           

            fetch('/api/pro-var-unit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    unit: selectedUnit,
                }),
            })
            .then(response => response.json())
            .then(data => {
               
                if (data.status === 'success') {
                    variationID = data.VariationID;
                    console.log('VariationID:', variationID);
      
                    return fetch('/api/insert-into-cart', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            variationID: variationID,
                        }),
                    });
                } else {
                    console.error('Error:', data.message);
                    priceButtons.forEach(function (button) {
                        button.classList.remove('unclickable');
                    });
                    throw new Error('Error fetching /api/pro-var-unit');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
               
                priceButtons.forEach(function (button) {
                    button.classList.add('unclickable');
                });
   
                sendToServer(selectedUnit);
   
                fetch('/api/insert-into-cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        variationID: variationID,
                    }),
                })
                .then(response => response.json())
                .then(data => {
                   
                    if (data.status === 'success') {
                        console.log('Variation inserted into cart successfully');
                    } else {
                        console.error('Error:', data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        }
    }
   
    function sendToServer(unit) {
        var xhr = new XMLHttpRequest();
        var url = '/api/view-product-variation';

        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                   
                    response = JSON.parse(xhr.responseText);
                   
                    document.getElementById('quan-disp').innerHTML = `
                        <p>Stock: ${response.quantity}</p>
                    `;
                    document.getElementById('plusminuscart').innerHTML = `
                        <button id="quantity-minus" class="adjust-quantity" onclick="adjustQuantity(-1)">-</button>
                        <span class="quantity-display">1</span>
                        <button id="quantity-plus" class="adjust-quantity" onclick="adjustQuantity(1)">+</button>
                    `;
                   
                    document.getElementById('plusminuscart').style.display = 'block';
               
                    highlightPriceButton(response.price);
                } else {
                    console.error('Error:', xhr.status);
                }
            }
        };

        var data = JSON.stringify({
            unit: unit
        });

        xhr.send(data);
    }

    function highlightPriceButton(selectedPrice) {
        priceButtons.forEach(function (button) {
            if (button.getAttribute('data-price') == selectedPrice) {
                button.classList.add('clicked');
            } else {
                button.classList.remove('clicked');
            }
        });
    }

    window.adjustQuantity = function(amount) {
        var quantityDisplay = document.querySelector('.quantity-display');
        var currentQuantity = parseInt(quantityDisplay.innerText);
        newQuantity = currentQuantity + amount;

        console.log('Adjusting quantity by:', amount);
        console.log('Current Quantity:', currentQuantity);
        console.log('New Quantity:', newQuantity);

        newQuantity = (newQuantity < 1) ? 1 : (newQuantity > response.quantity) ? response.quantity : newQuantity;

        quantityDisplay.textContent = newQuantity;

        console.log('Final Quantity:', newQuantity);
    };

    addToCartButton.addEventListener('click', function () {
        var productId = addToCartButton.getAttribute('data-product-id');

        console.log('ProductID:', productId);

        var data = {
            productID: productId,
            newQuantity: newQuantity,
            variationID: variationID
        };

        fetch('/add-to-cart-quan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
           
            console.log('Response from server:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('quantity-minus').addEventListener('click', function () {
        adjustQuantity(-1);
    });

    document.getElementById('quantity-plus').addEventListener('click', function () {
        adjustQuantity(1);
    });
});