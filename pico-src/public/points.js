

// Use global variable for status so we know if we need to send ajax if change
var button_pressed = '';

$(document).ready(function() {
// define handlers
$('#sw_1_1').click(function(){ButtonClicked1('1')});
$('#sw_2_1').click(function(){ButtonClicked1('2')});
$('#sw_3_1').click(function(){ButtonClicked1('3')});
$('#sw_4_1').click(function(){ButtonClicked1('4')});

$('#sw_1_2').click(function(){ButtonClicked2('1')});
$('#sw_2_2').click(function(){ButtonClicked2('2')});
$('#sw_3_2').click(function(){ButtonClicked2('3')});
$('#sw_4_2').click(function(){ButtonClicked2('4')});



}); // end ready



// handle button 1 (eg. up)
function ButtonClicked1 (button) {
    $.get ('/points', 'point='+button+"&position=1", displayResponse);
}


// handle button 2 (eg. down)
function ButtonClicked2 (button) {
    $.get ('/points', 'point='+button+"&position=1", displayResponse);
}


function displayResponse (data) {
    $('#status').html(data);
}
