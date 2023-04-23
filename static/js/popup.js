

let popup = document.querySelector(".popup");
let formBlock = document.querySelector(".formBlock");

popup.addEventListener("click", function(){
	setTimeout(() => {Clicked = true}, 2000);


	if (formBlock.classList.contains("disappear")) {
		formBlock.classList.remove("disappear");
		formBlock.style.opacity = "1"
    	formBlock.style.display = "flex"
    	
	}else{
		formBlock.style.opacity = "0"
		setTimeout(() => {formBlock.classList.add("disappear")}, 2000);
       	
    }
});

