function edit(id, first_name, last_name, email, phone) {
	$("#id").val(id);
	$("#fname").val(first_name);
	$("#lname").val(last_name);
	$("#email").val(email);
	$("#phone").val(phone);
}

function delete_contact() {
	let id = $("#id").val();
	var a = confirm(
		"Are you sure you want to delete this contact"
	);
	if (!a) return;
	fetch("/delete-contact/"+id)
	.then((res) => {
		location.reload()
	});
}

$(document).ready(function () {
	searchInput = document.getElementById("search")
	users = document.querySelectorAll(".fullName")
	
	searchInput.addEventListener("input", e => {
		const value = e.target.value.toLowerCase()
		users.forEach(user => {
			const isVisible = user.innerHTML.toLowerCase().includes(value)
			console.log(isVisible)
			let parent = user.parentElement.parentElement
			if (!isVisible){
				parent.style.display = "none"
			}
			else{
				parent.style.display = ""
			}
			
		  })
	})
	
});
