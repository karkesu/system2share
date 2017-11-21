function startTimer() {
	currentTimerStart = new Date().getTime()
}

function stopTimer() {
	currentTimerReading = new Date().getTime() - currentTimerStart;
	timeSpentReading += currentTimerReading;
}

// function logData(log) {
// 	var logJSON = JSON.stringify(log);
// 	var xhttp = new XMLHttpRequest();
// 	xhttp.open("POST", "/submit");
// 	xhttp.setRequestHeader("Content-type", "application/json");
// 	xhttp.send(logJSON);
// }
//
// function completeTask() {
// 	var form = document.getElementById('shareForm');
// 	console.log(form);
// 	var logJSON = JSON.stringify(form);
// 	console.log(logJSON);
//
// 	form.action ="{{ data.amazon_host }}";
// 	form.submit();
// 	console.log("SUBMITTED");
// }

function showShareForm() {
	startTimer();
	console.log("=======SHOW");
	document.getElementById('screen').style.display = 'block';
	document.getElementById('shareForm').style.display = 'block';
}

function hideShareForm() {
	stopTimer();
	document.getElementById('screen').style.display = 'none';
	document.getElementById('shareForm').style.display = 'none';
}

var currentTimerStart = -1;
var timeSpentReading = 0;

var log = new Object();
log.date = new Date();
// log.experiment = experiment;
