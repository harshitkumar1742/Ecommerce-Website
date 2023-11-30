//creating event handler 
var updatebuttons = document.getElementsByClassName('update-cart')

for(i=0; i<updatebuttons.length; i++) {
    updatebuttons[i].addEventListener('click', function() {
       // var productname = this.dataset.productname
        //var productid = this.dataset.product
        var uniqueid = this.dataset.uniqueid
        var action = this.dataset.action 


        console.log('uniqueid:', uniqueid, 'action:', action)
    

//checking user status on click 

        console.log('User:', user)
            if (user == 'AnonymousUser') {
                add_cookie_item(uniqueid, action)        }
            else {
                Update_Order(uniqueid, action)
        }
        
    
    }
    )

    function add_cookie_item(uniqueid, action) {
            console.log('user not authenticated')

            if (action== 'add') {
            // go ahead and get the uniqueid of the product which needs to be added to the cart but does not exist yet in the cart 
                if (cart[uniqueid] == undefined) {
                    cart[uniqueid] = {'quantity' : 1}
                }
            // if uniqueid/product aready exists in cart and click action = add is being implemented, increment quantity of that product by 1
                else{
                    cart[uniqueid]['quantity'] += 1
                }
            }
            if (action== 'remove') {
                cart[uniqueid]['quantity'] -= 1

                if (cart[uniqueid]['quantity'] <= 0) {
                    console.log('product item should be deleted')
                    delete cart[uniqueid]
                    }
            }

            if (action== 'add and remove') {
                cart[uniqueid]['quantity'] += 1
            }
           

                
            if (action== 'delete') {
                delete cart[uniqueid]

                
            }
            console.log('cart:', cart)
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
            location.reload()


    }
//sending data
    function Update_Order(uniqueid, action) {
        console.log('user authenticated')

        var url='/update_cart/'

        fetch(url,{
    //data type
            method: 'POST',
    //data
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrftoken,

            },
            body: JSON.stringify({'uniqueid': uniqueid,  'action' : action})

        })
//returning promise 
//first response converted to json value 
//then console the data out 
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            //location reload used so that update-wishlist icon in navigation bar gets updated as soon as an item is added to the list. 
            location.reload()
})
        .catch((error) => {
            console.error('Error:', error);
});



}
}
    