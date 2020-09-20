// Toggle 
$(document).ready(function(){
  $(".default-button").addClass("active");
  $(".five-state-toggle-button").click(function() {
    $(this).siblings(":button").removeClass("active");
    $(this).addClass("active");
  });
});

// Get newest data from back-end to browser through api  
$(document).ready(function() {
  function getData(){
    var job_dict
    $.ajax({
      'url': './list_all',
      'method': 'GET',
      'data': {job_dict},//something must be here,
      success: function(data) {
        console.log(`Successed: ${data}`);
        console.log(data);
      }
    });
  }
  getData();
  //setInterval(function() {getData()},15000);
});

// Update each toggle button state whenever refresh or reopen browser page
function ToggValue(){
  var job_dict
  var count = 4
  $.ajax({
    'url': './list_all',   
    'method': 'GET',
    'data': {job_dict},//something must be here,
    success: function(data) {
    console.log(`Successed: ${data}`);
    $(".five-state-toggle-button").removeClass("active");
    for (var i=1; i<=count; i++){ 
      var update_value = data[`toggle${i}`]['toggle_value']
      console.log('current toggle value: ' + update_value);
      switch(update_value){
        case 0:
            $(`#toggle${i}-button1`).addClass("active");
            break;
        case 1:
            $(`#toggle${i}-button0`).addClass("active");
            break;
        case 2:
            $(`#toggle${i}-button2`).addClass("active");
            break;
        case 3:
            $(`#toggle${i}-button3`).addClass("active");
            break;
        case 4:
            $(`#toggle${i}-button4`).addClass("active");
            break;
        case null:
            $(`#toggle${i}-button1`).addClass("active");
      }      
      //update_toggle_state(toggle_value);
      }
    }
  }); 
}

// Update each trigger state regularly
function triggerstatus(){
  var job_dict
  var count = 4
  $.ajax({
    'url': './list_all',
    'method': 'GET',
    'data': {job_dict},//something must be here,
    success: function(data) {
      console.log(`Successed: ${data}`);
      for (var i=1; i<=count; i++){
        trigger_status = data[`toggle${i}`]['trigger_status']
        console.log(`current trigger status: ` + trigger_status);
        if(trigger_status == 1){  
          $(`#notify-${i}`).removeClass("notify-off");
          $(`#notify-${i}`).addClass("notify-on"); 
        }
        if(trigger_status == 0){ 
          $(`#notify-${i}`).removeClass("notify-on");
          $(`#notify-${i}`).addClass("notify-off");
        }
      }
    }
  });
}
setInterval(function() {triggerstatus()},5000);

  
// Shared function
function push (feature, data, callback) {
  $.ajax({
    'url': './' + feature,
    'method': 'POST',
    'contentType': 'application/json', 
    'data': JSON.stringify(data),
  }).done(function (msg) {
    console.log(`Successed: ${msg}`);
    console.log(`toggle_id: ${msg.id}, turn_off_time: ${msg.turn_off_time}`);
    $(`#span-${msg.id}`).text(`${msg.turn_off_time}`);
  }).fail(function (msg) {
    console.log('failed: '+ msg.status +','+ msg.responseText);
    $('#message').text('failed: '+ msg.status +','+ msg.responseText);
  }).always(function() {
    if (typeof callback === 'function') {
      callback();
    } 
  });
}

$(function () {
    console.log('YA, loading success');
});
