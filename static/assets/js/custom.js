function quickviewclose(product){
    modal = product.parentElement.parentElement.parentElement
    modal.style.display = 'none'
}

function quickview(product){
    modal = document.getElementsByName(product.getAttribute('id'))[0] 
    modal.style.display = 'block'
    modal.scrollIntoView()

}

