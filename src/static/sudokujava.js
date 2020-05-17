var timers = []; // array of setTimeout functions, used for stop button event
var error_types = ["input_error","not_enough_squares","puzzle_complete"]; // types of input errors

$(document).ready(function () {

  // Get puzzle and reveal solution  
  $("#search-btn, #loop-btn, #algo-btn").click(function () {
    //timers = []; // Clear any timer data from previous executions

    // Get selected algorithm
    var selected_algo;
    if ($('input[name="simplesearch"]').is(":checked") && (this.id == "search-btn" || this.id == "loop-btn")){
      selected_algo = $('input[name="simplesearch"]:checked').val();
      if (this.id == "loop-btn"){
        selected_algo = selected_algo + "Loop";
      }    
    } else if ($('input[name="algosearch"]').is(":checked") && (this.id == "algo-btn")) {
      selected_algo = $('input[name="algosearch"]:checked').val();
    } else {
      window.alert("Please pick an algorithm");
      return;
    }

    // Disable page functionality, update status
    status_msg = statusMsg(selected_algo);
    freezePage(status_msg); 

    // Get puzzle and selected algorithm
    var puzzle_str = getPuzzle(); 
    var info = { algo: selected_algo, puzzle_str: puzzle_str };


    // Send user puzzle and selected algo to back-end 
    $.ajax({
      url: "/update_game",
      type: "POST",
      data: JSON.stringify(info),
      contentType: "application/json",
    }).done(function (data) {
      // Check if original input was invalid
      if (error_types.includes(data[0])) {
        errorMsg(data);
      }
      else {
        resetSquareCSS();

        // Incrementally reveal generated solution(s)
        var time = getTime(data[0].length); // Calcuate late depending on length of solution
        var totaltime = 100 + data[0].length * time;
        var scanCount = 1;
        for (i = 0; i < data[0].length; i++) {
          var $inputBox = $('.def-txt-input[name="[' + data[0][i] + ']"]');
          changeVal($inputBox, data, i, scanCount, time);
          scanCount++;
        }
        var squaresScanned = data[0].length;
        var squaresChanged = 0;
        for (i = 0; i < data[1].length; i++) {
          if (data[1][i] != "0") {
            squaresChanged++;
          }
        }
        if (squaresChanged == 0){
          var msg = "No changes made"
        } else {
          var msg = outputMsg(squaresScanned,squaresChanged,selected_algo)
        }
        unfreezePageTimed(totaltime, msg);
      }
    }); // end of ajax

  }); // end of simplesearch/algorithm button 

  // Reveal one square 
  $("#onesquare-btn").click(function () {
      var selected_algo = "onesquare";
      var puzzle_str = getPuzzle();
      var info = { algo: selected_algo, puzzle_str: puzzle_str };
      freezePage("");
      $.ajax({
        url: "/update_game",
        type: "POST",
        data: JSON.stringify(info),
        contentType: "application/json",
      }).done(function (data) {
        // Notify user if their original data was invalid
          if (error_types.includes(data[0])) {
          errorMsg(data);
        
        } else {
          // Incrementally reveal generated solution(s)
          resetSquareCSS();
          var time = 200;
          var scanCount = 1;
          var $inputBox = $('.def-txt-input[name="[' + data[0][0] + ']"]');
          changeVal($inputBox, data, 0, scanCount, 600);
          unfreezePageTimed(800,"One square revealed");
        }
      });
  });

  

  // Load puzzle from memory
  $("#easy-btn, #med-btn, #hard-btn").click(function () {
    if(this.id == "easy-btn"){
      var puzzle_difficulty = 0;
    } else if (this.id == "med-btn"){
      var puzzle_difficulty = 1;
    } else {
      var puzzle_difficulty = 2;
    }
    $.ajax({
      url: "/load_test",
      type: "POST",
      data: JSON.stringify(puzzle_difficulty),
      contentType: "application/json",
    }).done(function (data) {
      for (i = 0; i < 81; i++) {
        var $inputBox = $('.def-txt-input[name="[' + i + ']"]');
        if ((data[i] == "0") === true) {
          $inputBox.val("");
        } else {
          $inputBox.val(data[i]);
        }
      }
    });
    resetSquareCSS();
  });

  // Abort incremental solution reveal
  $("#stop-btn").click(function () {
    for (var i = 0; i< timers.length; i++){
            clearTimeout(timers[i]);
    }
    resetSquareCSS();
    unfreezePage("Scan Aborted!");
  });

  // Clear puzzle grid and text area, reset decoration. 
  $("#clear-btn").click(function() {
      for (i = 0; i < 81; i++) {
        var $inputBox = $('.def-txt-input[name="[' + i + ']"]');
        $inputBox.val("");
      }
      updateText("")
      resetSquareCSS();
  });

  // Enable tooltip hover
  $('[data-toggle="tooltip"]').tooltip();

});

// Allow only numbers 1-9 inside grid cells
$(function () {
  var $inputs = $(".def-txt-input");
  var intRegex = /^[1-9]$/;
  // Prevents user from manually entering non-digits.
  $inputs.on("input.fromManual", function () {
    if (!intRegex.test($(this).val())) {
      $(this).val("");
    }
  });
});

// Collect the input puzzle and return it in the form of an 81 char string 
function getPuzzle(){
  var puzzle_str = "";
  var nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"];
  for (i = 0; i < 81; i++) {
        var cell = $('.def-txt-input[name="[' + i + ']"]').val();
        if (nums.includes(cell) === true) {
          puzzle_str += cell;
        } else {
          puzzle_str += "0";
        }
      }
  return puzzle_str;
}
// Incrementally diplay value changes using setTimeout
function changeVal(inputBox, data, i, scanCount, time) {
  timer = setTimeout(function () {
    inputBox.css("border", "2px solid #00FF7F");
  }, 100 + time * scanCount);
  timers.push(timer);

  timer = setTimeout(function () {
    if ((data[1][i] == "0") === true) {
      inputBox.val("");
    } else {
      inputBox.val(data[1][i]);
    }
  }, 400 + time * scanCount);
  timers.push(timer);

  timer = setTimeout(function () {
    inputBox.css("border", "");
  }, 600 + time * scanCount);
  timers.push(timer);
}

// Decide the time increments when displaying the solution
function getTime(amount_of_changes){
  var time = 400;
  if (amount_of_changes > 50000){
    time = 1;
  }else if (amount_of_changes > 10000){
    time = 4;
  }else if (amount_of_changes > 5000){
    time = 8;
  }else if (amount_of_changes > 2000){
    time = 20;
  }else if (amount_of_changes > 1000){
    time = 40;
  }else if (amount_of_changes > 500){
    time = 80;
  }else if (amount_of_changes > 250){
    time = 160;
  }else if (amount_of_changes > 100){
    time = 240;
  }else{
    time = 400;
  }
  return time;
}

// Used for complex algorithm searches, load a lot faster. Display all square entries. 
function updateVal(inputBox, data, i, scanCount){
    setTimeout(function (){
      if ((data[1][i] == "0") === true) {
        inputBox.val("");
      } else {
        inputBox.val(data[1][i]);
      }
    }, 10+ 10*scanCount);
}

// Disable page functionality
function freezePage(msg) {
  for (i = 0; i < 81; i++) {
    $('.def-txt-input[name="[' + i + ']"]').prop("disabled", true);
  }
  $("#search-btn").prop("disabled", true);
  $("#loop-btn").prop("disabled", true);
  $("#algo-btn").prop("disabled", true);
  $("#clear-btn").prop("disabled", true);
  $("#easy-btn").prop("disabled", true);
  $("#med-btn").prop("disabled", true);
  $("#hard-btn").prop("disabled", true);
  $("#onesquare-btn").prop("disabled", true);
  $("#stop-btn").prop("disabled", false);
  updateText(msg);
}

// Enable page functionality
function unfreezePage(msg) {
  for (i = 0; i < 81; i++) {
    $('.def-txt-input[name="[' + i + ']"]').prop("disabled", true);
  }
  $("#search-btn").prop("disabled", false);
  $("#loop-btn").prop("disabled", false);
  $("#algo-btn").prop("disabled", false);
  $("#clear-btn").prop("disabled", false);
  $("#easy-btn").prop("disabled", false);
  $("#med-btn").prop("disabled", false);
  $("#hard-btn").prop("disabled", false);
  $("#onesquare-btn").prop("disabled", false);
  $("#stop-btn").prop("disabled", true);
  updateText(msg);
}

// Enable page functionality after elapsed period of time
function unfreezePageTimed(time, msg) {
  setTimeout(function () {
    for (i = 0; i < 81; i++) {
      $('.def-txt-input[name="[' + i + ']"]').prop("disabled", false);
    }
    $("#search-btn").prop("disabled", false);
    $("#loop-btn").prop("disabled", false);
    $("#algo-btn").prop("disabled", false);
    $("#clear-btn").prop("disabled", false);
    $("#easy-btn").prop("disabled", false);
    $("#med-btn").prop("disabled", false);
    $("#hard-btn").prop("disabled", false);
    $("#onesquare-btn").prop("disabled", false);
    $("#stop-btn").prop("disabled", true);
    updateText(msg);
  }, time);
}

// Reset square decoration
function resetSquareCSS() {
  for (i = 0; i < 81; i++) {
    $('.def-txt-input[name="[' + i + ']"]').css("border", "");
  }
}

// Notify user of error 
function errorMsg(data){
  if (data[0] == "input_error"){
    for (i = 0; i < data[1].length; i++) {
      var $inputBox = $('.def-txt-input[name="[' + data[1][i] + ']"]');
      $inputBox.css("border", "2px solid red");
    }
    unfreezePageTimed(500, "Please fix input error on puzzle");
    window.alert("Input error detected!");
  } else if(data[0] == "puzzle_complete"){
    unfreezePageTimed(500, "Puzzle already solved!");
    window.alert("Puzzle already solved!");
  } else if(data[0] == "not_enough_squares"){
    unfreezePageTimed(500, "Not enough squares to find a solution.");
    window.alert("Not enough squares entered.");
  }
}

// string to display status during solution reveal
function statusMsg(selected_algo){
  if (selected_algo == "onesquare"){
    return "Revealing one square..";
  } else if (selected_algo == "horizontalfs") {
    return "Performing a single search through unfilled squares from left to right...";
  } else if (selected_algo == "horizontalfsLoop") {
    return "Performing a looping search through unfilled squares from left to right...";
  } else if (selected_algo == "verticalfs") {
    return "Performing a single search through unfilled squares from top to bottom...";
  } else if (selected_algo == "verticalfsLoop") {
    return "Performing a looping search through unfilled squares from top to bottom...";
  } else if (selected_algo == "bestfs") {
    return "Performing a single search through unfilled squares in order of least possible solutions...";
  } else if (selected_algo == "bestfsLoop") {
    return "Performing a looping search through unfilled squares in order of least possible solutions...";
  } else if (selected_algo == "astar") {
    return "Performing an A Star search...";
  } else if (selected_algo == "depthfs") {
    return "Performing a depth first search...";
  } else {
    return "";
  }
}

// string to return algorithm stats after execution
function outputMsg(squares_scanned,squares_changed,selected_algo){
  if (selected_algo == "onesquare"){
    return "Revealing one square";
  } else if (selected_algo == "horizontalfs") {
    return "Simple Search: Left to right, single scan" + "\nSquares Scanned: " + squares_scanned + "\nSquares Changed: " + squares_changed;
  } else if (selected_algo == "horizontalfsLoop") {
    return "Simple Search: Left to right, loop until no solutions remaining" + "\nSquares Scanned: " + squares_scanned + "\nSquares Changed: " + squares_changed;
  } else if (selected_algo == "verticalfs") {
    return "Simple Search: Top to bottom, single scan" + "\nSquares Scanned: " + squares_scanned + "\nSquares Changed: " + squares_changed;
  } else if (selected_algo == "verticalfsLoop") {
    return "Simple Search: Top to bottom, loop until no solutions remaining" + "\nSquares Scanned: " + squares_scanned + "\nSquares Changed: " + squares_changed;
  } else if (selected_algo == "bestfs") {
    return "Simple Search: Best first search, single scan" + "\nSquares scanned: " + squares_scanned + "\nSquares Changed: " + squares_changed;
  } else if (selected_algo == "bestfsLoop") {
    return "Simple Search: Best first search, loop until no solutions remaining" + "\nSquares Scanned: " + squares_scanned + "\nSquares Changed: " + squares_changed;
  } else if (selected_algo == "astar") {
    return "Algorithmic Solution: A Star Algorithm" + "\nSquares Changed: " + squares_changed;
  } else if (selected_algo == "depthfs") {
    return "Algorithmic Solution: Depth First Search" + "\nSquares Changed: " + squares_changed;
  } else {
    return "";
  }
}

// Update text box
function updateText(text) {
  $("textarea#content").val(text);
}
