function edit(id, heading, desc, date) {
	console.log(id)
	$("#id").val(id);
	$("#heading").val(heading);
	$("#desc").val(desc);
	$("#date").val(date);
}

function delete_blog(id=$("#id").val()) {
	var a = confirm("Are you sure you want to delete this blog");
	if (!a) return;
	fetch("/delete-blog/"+id)
	.then((res)=>location.reload())
}
