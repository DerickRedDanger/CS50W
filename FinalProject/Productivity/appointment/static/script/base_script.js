document.addEventListener("DOMContentLoaded", function() {
  Snackbar();
});

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



// New Sort
  function sort_list() {
    // get the global values of the criterias and it's order(asc/desc)
    // putting each in a array to loop over

    // Get the RSideNav
    let div = document.getElementById('RSidenav');

    // Create a array of all of it's children's element but the first, since it's the search element.
    let elements = Array.from(div.children).slice(1);

    // Creating the function for the sort function, looping through the arrays to check the
    // dataset inside the elements
    function MultiCriteriaSort(a, b) {

      for (let i = 0; i < sort_rules.length; i++) {

        criteria = sort_rules[i].criteria
        orders = sort_rules[i].orders
        // If the criteria is date, turn the value inside the dataset in seconds
        if(criteria==="date"|| criteria=="deadline"){
          // if this criteria's order is ascending
          if (orders === "asc") {
            // If their values are different
            if (new Date(a.dataset[criteria]).getTime() != new Date(b.dataset[criteria]).getTime()) {
                // return the difference between A and B, if A is higher, the result
                // will be positive and the sort function it will be moved lower in the order.
                // otherwise it will be moved higher
                return new Date(a.dataset[criteria]).getTime() - new Date(b.dataset[criteria]).getTime();
            }
          //if this criteria's order is descending
          } else if (orders === "desc") {

            if (new Date(a.dataset[criteria]).getTime() != new Date(b.dataset[criteria]).getTime()) {
                // return the difference between B and A, following the same logic as before
                // but this time, if A is higher, it will be moved higher in the order,
                // otherwise it will be moved lower
                return new Date(b.dataset[criteria]).getTime() - new Date(a.dataset[criteria]).getTime();
            }
        }
        }else if(criteria !== 0){

          if (orders === "asc") {

            if (a.dataset[criteria] != b.dataset[criteria]) {

                return a.dataset[criteria] - b.dataset[criteria];
            }
          } else if (orders === "desc") {

            if (a.dataset[criteria] != b.dataset[criteria]) {

                return b.dataset[criteria] - a.dataset[criteria];
            }
        }

        }

      }
  }
    // sort the array based on the global variables
    elements = elements.sort(MultiCriteriaSort);

    // Using the array as base, find the element based on the id and append them in order in the div
    // Since the elements are in the div already, they are moved to the botton of it.
    for(i = 0; i < (elements.length); i++){
      div.appendChild(elements[i]);
    }
}







// Sort

  //Function adapted and modified from www.w3schools.com
  function sortList(sidenav,dataset1) {
    var list, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    list = document.getElementById(sidenav);
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc"; 
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = list.children;
      //If set to sort by importance
      if(dataset1 == "importance"){
          /*Loop through all list's rows:*/
          for (i = 0; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].dataset.importance;
            y = rows[i + 1].dataset.importance;
            /*check if the two rows should switch place,
            based on the direction, asc or desc:*/
            if (dir == "asc") {
              if (Number(x) > Number(y)) {
              //if so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (Number(x) < Number(y)) {
              //if so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
          }
        }
      
      //If set to sort by date
      if(dataset1 == "date"){
          /*Loop through all list's rows:*/
          for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*from the two elements you want to compare,
            one from current row and one from the next
            get their dataset for year,month and day:*/
            x_year = rows[i].dataset.year;
            y_year = rows[i + 1].dataset.year;
            x_month = rows[i].dataset.month;
            y_month = rows[i + 1].dataset.month;
            x_day = rows[i].dataset.day;
            y_day = rows[i + 1].dataset.day;
            
            if (dir == "asc") {
            // Check if X_year is higher than Y's
              if (Number(x_year) > Number(y_year)) {
              //if so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            // if both year is the same
            } else if (Number(x_year) == Number(y_year)) {
              // check their month
              if (Number(x_month) > Number(y_month)) {
                //if so, mark as a switch and break the loop:
                shouldSwitch = true;
                break;
              // if again, they are the same, check their day
              } else if (Number(x_month) == Number(y_month)) {
                if (Number(x_day) > Number(y_day)) {
                  //if so, mark as a switch and break the loop:
                  shouldSwitch = true;
                  break;
              }
            }
          }

            } else if (dir == "desc") {
              if (Number(x_year) < Number(y_year)) {
                //if so, mark as a switch and break the loop:
                shouldSwitch = true;
                break;
              } else if (Number(x_year) == Number(y_year)) {
                if (Number(x_month) < Number(y_month)) {
                  //if so, mark as a switch and break the loop:
                  shouldSwitch = true;
                  break;
                } else if (Number(x_month) == Number(y_month)) {
                  if (Number(x_day) < Number(y_day)) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
              }
            }
          }
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        //Each time a switch is done, increase this count by 1:
        switchcount ++;      
      } else {
        /*If no switching has been done AND the direction is "asc",
        set the direction to "desc" and run the while loop again.*/
        if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }

// Sort - changing button's orientation
function arrowUpdate(event){
  if (event == 'importance'){
    arrow=document.getElementById("sort_importance")
  
    if (arrow.dataset.arrow=="up"){
      arrow.innerHTML="by importance &darr;"
      arrow.dataset.arrow="down"
    } else  if (arrow.dataset.arrow=="down"){
      arrow.innerHTML="by importance &uarr;"
      arrow.dataset.arrow="up"

    }} else if (event == 'date'){
  arrow=document.getElementById("sort_date")

  if (arrow.dataset.arrow=="up"){
    arrow.innerHTML="by date &darr;"
    arrow.dataset.arrow="down"
  } else  if (arrow.dataset.arrow=="down"){
    arrow.innerHTML="by date &uarr;"
    arrow.dataset.arrow="up"
    }}}

// search - global variables
  //variables that define if case sensitive and where to search
var Case = "";
var where = "title"

// search - function to change global variables
  function updateSearch(){
    if (document.getElementById("Case").checked){
      Case = "sensitive"
    } else{
      Case = ""
    }
    where = document.getElementById("search_options").value
  }

// search - function

  function Search(Case,where) {
    var search, filter, list, row, a, i, txtValue; 
    search = document.getElementById("search");
    if (Case == "sensitive"){
      filter = search.value;
    } else {
      filter = search.value.toUpperCase();
    }
    list = document.getElementById("RSidenav");
    row = list.children;
    if (where == "everywhere"){
      for (i = 1; i < row.length; i++) {
          a = row[i];
          txtValue = a.textContent;
          if (Case != "sensitive"){
            txtValue = txtValue.toUpperCase();
          }  
          console.log(txtValue);
          if (txtValue.indexOf(filter) > -1) {
              row[i].style.display = "";
          } else {
              row[i].style.display = "none";
          }
      }

    } else if (where == "title"){
      for (i = 1; i < row.length; i++) {
        a = row[i].getElementsByTagName("a")[0];
        console.log(a); 
        txtValue = a.textContent;
        if (Case != "sensitive"){
          txtValue = txtValue.toUpperCase();
        }  
        console.log(txtValue);
        if (txtValue.indexOf(filter) > -1) {
            row[i].style.display = "";
        } else {
            row[i].style.display = "none";
        }
    }

    } else if (where == "date"){
      for (i = 1; i < row.length; i++) {
        a = row[i].getElementsByTagName("a")[0];
        b = row[i];
        txtValue = a.textContent +" "+ b.dataset.date +" "+ b.dataset.deadline;
        if (Case != "sensitive"){
          txtValue = txtValue.toUpperCase();
        }  
        console.log(txtValue);
        if (txtValue.indexOf(filter) > -1) {
            row[i].style.display = "";
        } else {
            row[i].style.display = "none";
        }
    }
    }
}

// Go to top of page - function
  function gotop(){
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
// Go to top of scroll - function
  function scrolltop(){
    let element = document.getElementById("myElement");
    element.scrollTop = 0;
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