// var my_tm = JSON.parse(tm_data);
// console.log(my_tm);
var my_tm;

var state_num = 0;

var current_state = document.getElementById("current_state");
var tape_row_top = document.getElementById("tape_row_top");
var tape_row_bottom = document.getElementById("tape_row_bottom");
var toggle_auto_button = document.getElementById("toggle_auto_button");
var delay_field = document.getElementById("delay_field");
var tm_data_text_area = document.getElementById("tm_data_text_area");
var error_field = document.getElementById("error_field");
var input_string_field = document.getElementById("input_string_field");

tm_data_text_area.value = "\
state_start # -> look_for_0 # R \n\
look_for_0 X -> look_for_0 X R \n\
look_for_0 0 -> look_for_1 X R \n\
look_for_0 1 -> state_reject 1 R \n\
look_for_0 2 -> state_reject 2 R \n\
look_for_0 _ -> state_accept _ R \n\
look_for_1 0 -> look_for_1 0 R \n\
look_for_1 X -> look_for_1 X R \n\
look_for_1 1 -> look_for_2 X R \n\
look_for_1 2 -> state_reject 2 R \n\
look_for_1 _ -> state_reject _ R \n\
look_for_2 1 -> look_for_2 1 R \n\
look_for_2 X -> look_for_2 X R \n\
look_for_2 2 -> state_start X R \n\
look_for_2 _ -> state_reject _ R \n\
 \n\
state_start * -> state_start * L \n\
";

var is_auto_on = false;
var cur_auto_id = null;

function display_state(tm_state){
	current_state.innerText = tm_state["cur_state"];
	tape_row_top.innerHTML = "";
	tape_row_bottom.innerHTML = "";
	for (var i=0; i<tm_state["tape"].length; i++){
		var new_top_cell = document.createElement("td");
		var new_bottom_cell = document.createElement("td");
		
		new_top_cell.innerText = tm_state["tape"][i];
		if (i === tm_state["cur_head_pos"]){
			new_top_cell.className="cur_selected_top_cell";
			new_bottom_cell.innerText = "^";
		}
		
		tape_row_top.appendChild(new_top_cell);
		tape_row_bottom.appendChild(new_bottom_cell);
	}
}

function advance_state(){
	if (state_num < my_tm.length-1) {
		state_num++;
		display_state(my_tm[state_num]);
	} else if (is_auto_on) {
		toggle_auto();
	}
}

function reset_state(){
	state_num = 0;
	display_state(my_tm[state_num]);
	
	if (is_auto_on) {
		toggle_auto();
	}
}

function regress_state(){
	if (state_num > 0) {
		state_num--;
		display_state(my_tm[state_num]);
	}
}

function start_auto(){
	is_auto_on = true;
	cur_auto_id = setInterval(advance_state, parseInt(delay_field.value));
	toggle_auto_button.innerText = "Auto off";
}

function stop_auto(){
	is_auto_on = false;
	clearInterval(cur_auto_id);
	cur_auto_id = null;
	toggle_auto_button.innerText = "Auto on";
}

function toggle_auto(){
	if (!is_auto_on){
		start_auto();
	} else {
		stop_auto();
	}
}

function submit_tm(){
	var xhttp = new XMLHttpRequest();
	var tm_rule_text = tm_data_text_area.value;
	var start_state = "state_start";
	var input_string = input_string_field.value;
	var data_dict = {"tm_data": tm_rule_text,
					"start_state": start_state,
					"input_string": input_string
					};
	
	error_field.innerText = "Simulating TM...";
	
	xhttp.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200) {
			response_json = JSON.parse(this.responseText);
			console.log(JSON.parse(this.responseText));
			if (!response_json["error"]){
				my_tm = response_json["data"];
				error_field.innerText = "TM Registered!";
				reset_state();
			} else {
				error_field.innerText = response_json["data"];
			}
		}
	}
	
	xhttp.open("POST", "/generate_tm", true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(JSON.stringify(data_dict));
}

submit_tm();