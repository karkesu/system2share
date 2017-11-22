function startTimer() {
	currentTimerStart = new Date().getTime()
}

function stopTimer() {
	currentTimerReading = new Date().getTime() - currentTimerStart;
	timeSpentReading += currentTimerReading;
}

function showShareForm() {
	startTimer();
	document.getElementById('screen').style.display = 'block';
}

function hideShareForm() {
	stopTimer();
	document.getElementById('screen').style.display = 'none';
}

function addHidden(form, key, value) {
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = value;
    form.appendChild(input);
}

function submitTask(url) {
	var form = document.forms['mturkForm'];
	addHidden(form, 'testing', 'a');
	addHidden(form, 'testing', 'b');
	form.submit();
    // var formData = new FormData(form)
    // var xhr = new XMLHttpRequest();
    // xhr.open("POST", "{{ data.amazon_host }}");
    // xhr.send(formData);
}

// var form = document.getElementById('mturkForm');
// form.addEventListener("submit", function (event) {
//      event.preventDefault();
//      submitTask();
//    });

var currentTimerStart = -1;
var timeSpentReading = 0;

window.onload = function () {
	// add stuff here
}