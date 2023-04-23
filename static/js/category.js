
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

openClose(".iconsShow1", ".first_post_category_1")
openClose(".iconsShow2", ".first_post_category_2")
openClose(".iconsShow3", ".first_post_category_3")