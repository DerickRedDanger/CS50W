
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
  button = document.getElementById("LSOpenBtn")
  if (button.value ="o<br>p<br>e<br>n"){
  document.getElementById("LSidenav").style.width = "450px";
  button.style.marginLeft = "449px";
  button.value="c<br>l<br>o<br>s<br>e"
  document.getElementById("main").style.marginLeft = "449px";
  

  } else if (button.value ="c<br>l<br>o<br>s<br>e"){
  document.getElementById("LSidenav").style.width = "0";
  button.style.marginLeft= "0";
  button.value ="o<br>p<br>e<br>n"
  document.getElementById("main").style.marginLeft= "0";
  
  }
}

function closeLNav() {
  document.getElementById("LSidenav").style.width = "0";
  document.getElementById("LSOpenBtn").style.marginLeft= "0";
  document.getElementById("main").style.marginLeft= "0";
}

// Sidenav - right

function openRNav() {
  button = document.getElementById("RSOpenBtn");
  console.log(button);
  console.log(button.innerHTML);

  if (button.dataset.open == "1"){
  console.log("open -> close");
  document.getElementById("RSidenav").style.width = "450px";
  button.style.marginRight = "449px";
  button.innerHTML="c<br>l<br>o<br>s<br>e";
  button.dataset.open = "0"
  document.getElementById("main").style.marginRight = "449px";
  
  } else if (button.dataset.open == "0"){
  console.log("close -> open");
  document.getElementById("RSidenav").style.width = "0";
  button.style.marginRight= "0";
  button.innerHTML ="o<br>p<br>e<br>n";
  button.dataset.open = "1"
  document.getElementById("main").style.marginRight= "0";
  
  }
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