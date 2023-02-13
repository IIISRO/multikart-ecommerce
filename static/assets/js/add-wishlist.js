var addWishlistBTN=document.getElementsByClassName('wishlist-al')
for(var i = 0; i<addWishlistBTN.length;i++){
    addWishlistBTN[i].addEventListener('click', function(){
        var productId = this.dataset.productid
        var action = this.dataset.action
        if(action==='add'){
            this.dataset.action='remove'
            this.innerHTML='<i class="fa fa-heart" style="color:orangered;" aria-hidden="true"></i>'
            $.notify({
                icon: 'fa fa-check',
                title: 'Success!',
                message: 'Item Successfully added in wishlist'
            }, {
                element: 'body',
                position: null,
                type: "danger",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: true,
                placement: {
                    from: "top",
                    align: "right"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    '<span data-notify="message">{2}</span>' +
                    '<div class="progress" data-notify="progressbar">' +
                    '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                    '</div>'
            });
        }else if(action==='remove'){
            this.dataset.action='add'
            this.innerHTML='<i class="ti-heart" aria-hidden="true"></i>'
            $.notify({
                icon: 'fa fa-check',
                title: 'Success!',
                message: 'Item Successfully removed in wishlist'
            }, {
                element: 'body',
                position: null,
                type: "secondary",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: true,
                placement: {
                    from: "top",
                    align: "right"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    '<span data-notify="message">{2}</span>' +
                    '<div class="progress" data-notify="progressbar">' +
                    '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                    '</div>'
            });
        }
        addWhislist(productId,action)
    })
}


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

function addWhislist(productId,action) {
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
    })
}
