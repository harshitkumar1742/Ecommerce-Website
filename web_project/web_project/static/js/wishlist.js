//creating event handler 
var updatebuttons = document.getElementsByClassName('update-wishlist')


for(i=0; i<updatebuttons.length; i++) {
    updatebuttons[i].addEventListener('click', function() {
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
                if (wishlist[uniqueid] == undefined) {
                    wishlist[uniqueid] = {'quantity' : 1}
                }
            // if uniqueid/product aready exists in cart and click action = add is being implemented, increment quantity of that product by 1
                else{
                    wishlist[uniqueid]['quantity'] += 1
                }
            }
            if (action== 'remove') {
                wishlist[uniqueid]['quantity'] -= 1

                if (wishlist[uniqueid]['quantity'] <= 0) {
                    console.log('product item should be deleted')
                    delete wishlist[uniqueid]
                    }
            }
            if (action== 'add and remove') {
                wishlist[uniqueid]['quantity'] -= 1
                cart[uniqueid]['quantity'] += 1
                

                if (wishlist[uniqueid]['quantity'] <= 0) {
                    console.log('product item should be deleted')
                    delete wishlist[uniqueid]
                    }

                
            }
            if (action== 'delete') {
                delete wishlist[uniqueid]

                
            }
            console.log('wishlist:', wishlist)
            document.cookie = 'wishlist=' + JSON.stringify(wishlist) + ";domain=;path=/"
            location.reload()



    }
//sending data
    function Update_Order(uniqueid, action) {
        console.log('user authenticated')

        const url='/update_wishlist/'

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
    