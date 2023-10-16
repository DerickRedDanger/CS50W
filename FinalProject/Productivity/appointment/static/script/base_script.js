
document.addEventListener("DOMContentLoaded",Snackbar());

function Snackbar() {
  var x = document.getElementById("Snackbar");
  x.style.display = "block"
  x.classList.remove("hide")
  x.classList.add("show");

}

function Close(){
  var x = document.getElementById("Snackbar");
  x.classList.remove("show")
  x.classList.add("hide");
  setTimeout(function(){ x.style.display = "none"; }, 500);
}

/*
Snackbar = "This is a success"
alert = "success"

    return render(request, "test.html",{"Snackbar":Snackbar, "alert":alert})

*/