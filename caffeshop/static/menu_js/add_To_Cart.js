function addToCart(form_id) {
    event.preventDefault();
    let formElement = document.getElementById(form_id);
    let formData = new FormData(formElement);
    // let orders = getCookieObject('orders'); // gets oder object from cookie
    let orders = getLocalStorageObject('orders'); // gets oder object from cookie
    // let message = getCookie('message');
    let message = localStorage.getItem('message');
    let product = formData.get('product');
    let product_name = formData.get('product_name');
    let number_of_product = +formData.get('quantity');
    let product_price = +formData.get('price');
    let product_image_url = formData.get('image_url');
    let product_detail_url = formData.get('detail_url');

    if (JSON.stringify(orders) == '{}' ){ // alert('has entered to add level for non exist of last order')
        orders[product] = {};
        orders[product]['name'] = product_name ;
        orders[product]['quantity'] = number_of_product ;
        orders[product]['price'] = product_price;
        orders[product]['total_price'] = product_price * orders[product]['quantity'];
        orders[product]['image_url'] = product_image_url ;
        orders[product]['detail_url'] = product_detail_url ;
        message = "you created a shopping cart";
      }
    else {
      if (orders[product]){   // alert('has entered to update level for exist of last order')
            orders[product]['quantity'] = +orders[product]['quantity'] + number_of_product; 
            orders[product]['price'] = product_price;
            orders[product]['total_price'] = product_price * orders[product]['quantity'];
            message = "Order updated";
            }
        else {  // alert('has entered to add level for exist of last order')
            orders[product] = {};
            orders[product]['name'] = product_name ;
            orders[product]['quantity'] = number_of_product ;
            orders[product]['price'] = product_price;
            orders[product]['total_price'] = product_price * orders[product]['quantity'];
            orders[product]['image_url'] = product_image_url ;
            orders[product]['detail_url'] = product_detail_url ;
            message = "Order added";
            }
    }
    // setCookie('orders', JSON.stringify(orders), 60);
    localStorage.setItem('orders', JSON.stringify(orders));
    // setCookie('message', message, 60);
    localStorage.setItem('message', message);
    // setOrderItemsNumber(orders); // set number of order items in  cookie and cart button 
    setOrderItemsNumber(orders); // set number of order items in  cookie and cart button
 }