function startTimer() {
	currentTimerStart = new Date().getTime()
}

function stopTimer() {
	currentTimerReading = new Date().getTime() - currentTimerStart;
	timeSpentReading += currentTimerReading;
}

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
