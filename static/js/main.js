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

function submitTask() {
    var formData = new FormData(form)
    var xhr = new XMLHttpRequest();
    var formData = new FormData(form);
    xhr.open("POST", "{{ data.amazon_host }}");
    xhr.send(formData);
}

var form = document.getElementById('mturkForm');
form.addEventListener("submit", function (event) {
    event.preventDefault();
    submitTask();
  });

var currentTimerStart = -1;
var timeSpentReading = 0;