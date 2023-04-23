let popup = document.querySelector(".popup");
let formBlock = document.querySelector(".formBlock");
let formInner = document.querySelector(".form_inner");
isShow = false

popup.addEventListener("click", function(){
	if (!isShow) {
		formBlock.style.opacity = "1"
    	formBlock.style.display = "flex"
        isShow = true
	}else{
		formBlock.style.opacity = "0"
		setTimeout(() => { formBlock.style.display = "none" }, 2200)
       	isShow = false
    }
});