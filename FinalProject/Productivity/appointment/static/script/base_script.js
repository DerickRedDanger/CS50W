console.log(document.readyState)
document.addEventListener("DOMContentLoaded", function() {
  console.log(document.readyState)
  Snackbar();
});

// Snackbar
function Snackbar() {
  var x = document.getElementById("Snackbar");
  if (x){
    console.log(x)
    x.style.display = "block"
    x.classList.remove("hide")
    x.classList.add("show");
  }
  

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

// --- Sort funtion, it's sub functions and varaibles ---

  // Getting a array of the sort buttons to use in the sort functions
  let sort_buttons = Array.from(document.getElementById('sort').children)

  // creating a array with the original Html of the buttons for later use
  let buttons_original_Html = [];
  for( i=0; i < sort_buttons.length; i++){
    buttons_original_Html.push(sort_buttons[i].innerHTML);
  };
 
  // initialise the arrays for the sort_rules array
  let criteria = [0,0,0];
  let orders = [0,0,0];
  let clicks = [0,0,0];

  // Creats a array of objects based on criteria, orders and click
  let sort_rules = criteria.map((item, index) => ({criteria: item, orders: orders[index], clicks: clicks[index]}));
  console.dir(sort_rules)

  // when the DOM is loaded, ad the following functions to the sort buttons
  document.addEventListener("DOMContentLoaded", function() {
    for (let i = 0; i < sort_buttons.length; i++) {
      sort_buttons[i].addEventListener('click', function() {
        Sort_rules_update(this);
        sort_list();
        sort_button_upate();
      });
    }
  });


// -- Function to update the sort rules, based on the sort button clicked --
function Sort_rules_update(element){

    //Loop inside sort_rules and check if this element's criteria is inside it.
    for (let i = 0; i < sort_rules.length; i++) {
      // If it find a empty criteria overwrite it with this element's, 
      // update the elements priority to i and break.
      if (sort_rules[i].criteria === 0){
        sort_rules[i].criteria = element.dataset.criteria;
        sort_rules[i].orders = element.dataset.orders;
        sort_rules[i].clicks++ ;
        element.dataset.priority = i
        element.dataset.clicks = sort_rules[i].clicks
        break

      // If this element is already inside it,
      } else if (sort_rules[i].criteria === element.dataset.criteria){
        //check if this is the third time it's clicked
        // If it's, reset it to 0, reset the button's dataset to the initial and break
        if (sort_rules[i].clicks >= 2){
          sort_rules[i].criteria = 0;
          sort_rules[i].orders = 0;
          sort_rules[i].clicks = 0;
          element.dataset.orders = "asc"
          element.dataset.priority = -1
          element.dataset.clicks = sort_rules[i].clicks
          break
          
          // if it isn't the third time, increase the number of times it was clicked
          // update the element's dataset.orders and break
        } else {
          element.dataset.orders = "desc"
          sort_rules[i].orders = element.dataset.orders;
          sort_rules[i].clicks++ ;
          element.dataset.clicks = sort_rules[i].clicks
          break
        }
      }
    }

    // Loops inside the sort_rule again, checking for empty criterias. If found,
    // check if there is another criteria after it, and if there is, check if it's not empty.
    // if it's not empty,replace the current with the next criteria and reset the next.
    // effectively moving empty criterias to the end of the array.
    for (let i = 0; i < sort_rules.length; i++) {
      if (sort_rules[i].criteria === 0 && i + 1 < sort_rules.length && sort_rules[i+1].criteria !==0){
        sort_rules[i].criteria = sort_rules[i+1].criteria;
        sort_rules[i].orders = sort_rules[i+1].orders;
        sort_rules[i].clicks = sort_rules[i+1].clicks;
        sort_rules[i+1].criteria = 0;
        sort_rules[i+1].orders = 0;
        sort_rules[i+1].clicks = 0;
      }
    }

    // Updates the buttons dataset.priority, based on the new composition of the sort_rules array
    for (let i = 0; i < sort_buttons.length; i++){
      let button_inside_rule = "0"
      for (let j = 0; j < sort_rules.length; j++){
        if (sort_rules[j].criteria == sort_buttons[i].dataset.criteria){
          button_inside_rule= "1"
          sort_buttons[i].dataset.priority=j
        }
      }
        if(button_inside_rule == "0"){
          sort_buttons[i].dataset.priority=-1
        }
    }
  }


// -- Variables for the sort_list--
  //Get the RSideNav Div
  let RSideNav = document.getElementById('RSidenav');

  // Make a array of the defult order of the list.
  let original_list_order = Array.from(RSideNav.children).slice(1);

// -- Mult criteria sort function, that sort the list elements based on up to 3 critrias
// Or back to the defaul order if all criterias are empty--
function sort_list() {
    

    // Create a array of all of RSideNav children's element but the first, since the first is the search element.
    // thus creating a array of the lists inside RSideNav
    let list_elements = Array.from(RSideNav.children).slice(1);

    // Variable to check how many criteria were empty
    let empty_criteria = 0

    // loop inside the sort_rules and check how many criterias are empty
    for (let i=0;i<sort_rules.length; i++){
      if(sort_rules[i].criteria == 0){
        empty_criteria++
      }
    }

    // If all criterias were empty, sort the list based on the orignal position of it's elements
    if (empty_criteria == 3 ) {
      for(i = 0; i < (original_list_order.length); i++){
        // Using the Original_order array as base, append the elements in order on the div
        // Since the elements are already in the div, they are moved to the botton of it.
        RSideNav.appendChild(original_list_order[i]);
      }
      // and break out of the funtion
      return
    } 
    
    // If at least one of the criteria aren't empty, continue the function 

    // the function for the sort function, looping through the arrays to check the
    // dataset inside the elements
    function MultiCriteriaSort(a, b) {

      for (let i = 0; i < sort_rules.length; i++) {
        // putting the values in variables to make it easier to read and understand
        criteria = sort_rules[i].criteria
        orders = sort_rules[i].orders

        // If the criteria is date/deadline, turn the value inside the dataset in seconds
        if(criteria==="date"|| criteria=="deadline"){
          // if this criteria's order is ascending
          if (orders === "asc") {
            // If their values are different
            if (new Date(a.dataset[criteria]).getTime() != new Date(b.dataset[criteria]).getTime()) {
                // return the difference between A and B to the sort function
                // if A is higher, the result will be positive and the sort function 
                // will move A lower in the order. Otherwise it will move A higher.
                return new Date(a.dataset[criteria]).getTime() - new Date(b.dataset[criteria]).getTime();
            }
          //if this criteria's order is descending
          } else if (orders === "desc") {

            if (new Date(a.dataset[criteria]).getTime() != new Date(b.dataset[criteria]).getTime()) {
                // return the difference between B and A to the sort function
                // if A is higher, the result will be negatove and the sort function 
                // will move A higher in the order. Otherwise it will move A lower.
                return new Date(b.dataset[criteria]).getTime() - new Date(a.dataset[criteria]).getTime();
            }
        }
        // If the criteria isn't date/deadline, nor empty(o)
        }else if(criteria !== 0){

          if (orders === "asc") {
            if (a.dataset[criteria] != b.dataset[criteria]) {
                return a.dataset[criteria] - b.dataset[criteria];
            }

          } else if (orders === "desc") {
            if (a.dataset[criteria] != b.dataset[criteria]) {
                return b.dataset[criteria] - a.dataset[criteria];
            }
        }}
      }
  }

    // sort the array based on the global variable sort_rule
    list_elements = list_elements.sort(MultiCriteriaSort);

    // sort the list in the new order

      // Using the sorted array as base, append the elements in order on the div
      // Since the elements are already in the div, they are moved to the botton of it.
      for(i = 0; i < (list_elements.length); i++){
        RSideNav.appendChild(list_elements[i]);
      }


}



// Function that updates the sort button's HTML based on it's presence/or lack of in the sort_rules
  function sort_button_upate(){
    frontOptions = ["1°", "2°", "3°"]
    behindOptions = ["&uarr;", "&darr;"]


    // Loops thought the buttons inside the array
    for (let i = 0; i < sort_buttons.length; i++) {
      
      // get the element, it's priority and order, In order to make the following less verbose
      let element = sort_buttons[i]
      let priority = sort_buttons[i].dataset.priority;
      let order = sort_buttons[i].dataset.orders;
      let clicks = sort_buttons[i].dataset.clicks
      
      // Based on the priority, if it's in the sort_rules and it's position
      switch (priority) {

        // if the priority is -1 (not in the sort rule), check if the element.innerHTML
        // is the initial one, if it isn't, reset to it.
        case "-1":
          if(element.innerHTML!== buttons_original_Html[i]){
            element.innerHTML = buttons_original_Html[i]
            }
          break;

        // otherwise, modify the html to have it's position in the sort_rule in
        // front of the html and if it's ascending or descending behind it

        // If it's the first in the order, add a 1° in front
        case "0":
            // if ascending add a arrow pointing up after it
          if(order == "asc" && element.innerHTML !== frontOptions[0] + " " + buttons_original_Html[i] + " " + behindOptions[0]){
            element.innerHTML = frontOptions[0] + " " + buttons_original_Html[i] + " " + behindOptions[0];
            // if descending add a arrow pointing down
          } else if (order == "desc" && element.innerHTML!==frontOptions[0] + " " + buttons_original_Html[i] + " " + behindOptions[1]){
            element.innerHTML = frontOptions[0] + " " + buttons_original_Html[i] + " " + behindOptions[1];
          }
          break;

        // If it's the first in the order, add a 2° in front
        case "1":
          if(order == "asc" && element.innerHTML!==frontOptions[1] + " " + buttons_original_Html[i] + " " + behindOptions[0]){
            element.innerHTML = frontOptions[1] + " " + buttons_original_Html[i] + " " + behindOptions[0];

          } else if (order == "desc" && element.innerHTML!==frontOptions[1] + " " + buttons_original_Html[i] + " " + behindOptions[1]){
            element.innerHTML = frontOptions[1] + " " + buttons_original_Html[i] + " " + behindOptions[1];
          }
          break;

        // If it's the first in the order, add a 3° in front
        case "2":
          if(order == "asc" && element.innerHTML!==frontOptions[2] + " " + buttons_original_Html[i] + " " + behindOptions[0]){
            element.innerHTML = frontOptions[2] + " " + buttons_original_Html[i] + " " + behindOptions[0];

          } else if (order == "desc" && element.innerHTML !== frontOptions[2] + " " + buttons_original_Html[i] + " " + behindOptions[1]){
            element.innerHTML = frontOptions[2] + " " + buttons_original_Html[i] + " " + behindOptions[1];
          }
          break;
        
        // On the unlikely case it's not one of the 4 options, warn of the error and break
        default:
          console.log("Error in the Button update, it reached the default case")
          break;
      }
      switch(clicks){
        case "0":
          element.classList.remove("clicks-1","clicks-2")
          element.classList.add("clicks-0")
          break

        case "1":
          element.classList.remove("clicks-0","clicks-2")
          element.classList.add("clicks-1")
          break

        case "2":
          element.classList.remove("clicks-0","clicks-1")
          element.classList.add("clicks-2")
          break
      }
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