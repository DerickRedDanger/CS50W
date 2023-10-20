
document.addEventListener("DOMContentLoaded",Snackbar());

// Snackbar
function Snackbar() {
  var x = document.getElementById("Snackbar");
  console.log(x)
  x.style.display = "block"
  x.classList.remove("hide")
  x.classList.add("show");

};

function Close(){
  var x = document.getElementById("Snackbar");
  x.classList.remove("show")
  x.classList.add("hide");
  setTimeout(function(){ x.style.display = "none"; }, 500);
};

// Reset Button
function resett(){
  var x = document.getElementById("reset")
  var y = document.getElementById("reset?")
  x.style.display = "block"
  y.style.display = "none"
  console.log(x)
  console.log(y)

};

function cancel(){
  var y = document.getElementById("reset?")
  var x = document.getElementById("reset")
  y.style.display = "block"
  x.style.display = "none"
  console.log(x)
  console.log(y)
};

// Sidenav - left

function openLNav() {
  document.getElementById("LSidenav").style.width = "250px";
  document.getElementById("LSOpenBtn").style.marginLeft = "249px";
  document.getElementById("main").style.marginLeft = "249px";
}

function closeLNav() {
  document.getElementById("LSidenav").style.width = "0";
  document.getElementById("LSOpenBtn").style.marginLeft= "0";
  document.getElementById("main").style.marginLeft= "0";
}

// Sidenav - right

function openRNav() {
  document.getElementById("RSidenav").style.width = "250px";
  document.getElementById("LSOpenBtn").style.marginRight = "249px";
  document.getElementById("main").style.marginRight = "249px";
}

function closeRNav() {
  document.getElementById("RSidenav").style.width = "0";
  document.getElementById("LSOpenBtn").style.marginRight= "0";
  document.getElementById("main").style.marginRight= "0";
}


/*

    snackbar=""
    alert=""
    link=""

            form = form.save()
            snackbar =f"The event '{form.title}' has been saved successfully" 
            alert="success"
            link=form.get_absolute_url()

  
            title = request.POST['title']
            snackbar =f"The event '{title}' wasn't valid - Check the errors warning at the beginning of the form for more information and directions" 
            alert="alert"


            "Snackbar":snackbar, "alert":alert, "link":link,
*/