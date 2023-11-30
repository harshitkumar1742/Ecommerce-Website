//creating event handler 
var updatebuttons = document.getElementsByClassName('update-review')

for(i=0; i<updatebuttons.length; i++) {
    updatebuttons[i].addEventListener('click', function() {

        var review = this.dataset.review
        //var rate= this.dataset.rate
        var action = this.dataset.action 


        console.log('review:', review, 'action:', action)
    

//checking user status on click 

        console.log('User:', user)
            if (user == 'AnonymousUser') {
                console.log('user not authenticated')
        }
            else {
                Update_Order(review, action)
        }
        
    
    }
    )
//sending data
    function Update_Order(review, action) {
        console.log('user authenticated')

        var url='/shop/products/<str:name/'

        fetch(url,{
    //data type
            method: 'POST',
    //data
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrftoken,

            },
            body: JSON.stringify({'review': review, 'action': action})

        })
//returning promise 
//first response converted to json value 
//then console the data out 
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            
})
        .catch((error) => {
            console.error('Error:', error);
});



}
}