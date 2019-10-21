var my_tm = JSON.parse(tm_data);
console.log(my_tm);

var state_num = 0;
var max_states = my_tm.length;

var current_state = document.getElementById("current_state");
var tape_row_top = document.getElementById("tape_row_top");
var tape_row_bottom = document.getElementById("tape_row_bottom");
var toggle_auto_button = document.getElementById("toggle_auto_button");
var delay_field = document.getElementById("delay_field");

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
	if (state_num < max_states-1) {
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

display_state(my_tm[state_num]);
