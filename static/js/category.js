
//".firstCategory"
//".first_post_category_1"
function openClose(firstCat, firstPostCat) {
	let popup = document.querySelector(String(firstCat));
	let formBlock = document.querySelector(String(firstPostCat));
	formBlock.classList.add("disappear")
	
	popup.addEventListener("click", function(){

	if (formBlock.classList.contains("disappear")) {
		formBlock.classList.remove("disappear");
	}else{
		formBlock.classList.add("disappear")
    	}
	});
}

function openCloseIcon(firstCat, firstPostCat) {
	let right = document.querySelector(String(firstCat));
	let left = document.querySelector(String(firstPostCat));
	left.classList.add("disappear")
	
	right.addEventListener("click", function(){
	if (left.classList.contains("disappear")) {
		left.classList.remove("disappear");
		right.classList.add("disappear")
		
	}else{
		left.classList.add("disappear")
		right.classList.remove("disappear")
    	}
	});

	left.addEventListener("click", function(){
	if (right.classList.contains("disappear")) {
		right.classList.remove("disappear");
		left.classList.add("disappear")
		
	}else{
		right.classList.add("disappear")
		left.classList.remove("disappear")
    	}
	});
}

openClose(".iconsShow1", ".first_post_category_1")
openClose(".iconsShow2", ".first_post_category_2")
openClose(".iconsShow3", ".first_post_category_3")


openCloseIcon(".arrow-right-r1", ".arrow-down-r1")
openCloseIcon(".arrow-right-r2", ".arrow-down-r2")
openCloseIcon(".arrow-right-r3", ".arrow-down-r3")