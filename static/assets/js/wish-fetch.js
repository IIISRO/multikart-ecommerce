
function main(){

    async function Products(api_url='/api/wishlist') {
        const response = await fetch(api_url, {
            method: 'GET', // *GET, POST, PUT, DELETE, etc.
        });
        
        return response.json(); // parses JSON response into native JavaScript objects
    }

    Products('/api/wishlist')
    .then((data) => {
        if(data.length>0){
            document.getElementById('items').innerHTML=
`            <table class="table cart-table table-responsive-xs">
            <thead>
                <tr class="table-head">
                    <th scope="col">image</th>
                    <th scope="col">product name</th>
                    <th scope="col">price</th>
                    <th scope="col">action</th>
                </tr>
            </thead>
            ${
                (function products() {
                  
                  var products=[]
                    for(i in data){
                        products.push(
                            `
                            <tbody>
                            <tr>
                                <td>
                                    <a href="${data[i].url}"><img src="${data[i].main_img}" alt=""></a>
                                </td>
                                <td><a href="${data[i].url}">${data[i].title}</a>
                                   
                                </td>
                                <td>
                                    <h2>$${data[i].actual_price.toFixed(2)}</h2>
                                </td>
                                <td><button style="background-color: white ;border: none;"  data-productId=${data[i].id} data-action='remove' id="remove-wish"> <i class="ti-close"></i></button></td>
                            </tr>
                        </tbody>
                        `
                        )
                    }
                    return products
                })()
            }
    
            </table>`
       





        document.getElementById('remove-wish').addEventListener('click', function(){
            var productId = this.dataset.productid
            var action = this.dataset.action
            removeWishList(productId,action)
        })
    


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    function removeWishList(productId,action) {
        var url = '/account/add-wishlist/'
        fetch(url,{
            method:"POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                'Content-Type': 'application/json'
              },
            body:JSON.stringify({'productId':productId,
                                 'action':action,
                                 'userId':userId
                                })
        })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            console.log(data)
            main()
        })
    }

}else{
    document.getElementById('items').innerHTML="<h1>You don't have any items</h1>"
}
    });

}

            
main()

