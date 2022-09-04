function readMore(id) {
    var btnText = document.getElementById("btn" + id);
    if (!$("#full" + id).is(":hidden")) {
      btnText.innerHTML = "Read more";
      $("#full" + id).prop("hidden", true);
      $("#msg" + id).prop("hidden", false);
    } else {
      btnText.innerHTML = "Read less";
      $("#full" + id).prop("hidden", false);
      $("#msg" + id).prop("hidden", true);
    }
  }
function delete_msg(id){
    let c = confirm("Are you sure you want to delete this message (cannot be undone)")
    if (!c) return
    fetch("/delete-message/"+id)
    .then((res) => res.json())
    .then((data) => {
        if (data == "ok") $('#'+id).remove()
    });
  }