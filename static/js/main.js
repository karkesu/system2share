function startTimer() {
	currentTimerStart = new Date().getTime()
}

function stopTimer() {
	currentTimerReading = new Date().getTime() - currentTimerStart;
	timeSpentReading += currentTimerReading;
}

function logData() {

}

function showPostForm() {
	startTimer()
	document.getElementById('post-form').style.display = 'block'
}

function hidePostForm() {
	stopTimer()
	document.getElementById('post-form').style.display = 'none'
}

var currentTimerStart = -1;
var timeSpentReading = 0;