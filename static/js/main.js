function startWritingTimer() {
	currentTime = new Date().getTime()
	readingTimer += currentTime - currentTimerStart;
	currentTimerStart = currentTime;
}

function stopWritingTimer() {
	currentTime = new Date().getTime()
	writingTime += currentTime - currentTimerStart;
	currentTimerStart = currentTime;
}

function showShareForm() {
	startWritingTimer();
	document.getElementById('screen').style.display = 'block';
}

function hideShareForm() {
	stopWritingTimer();
	document.getElementById('screen').style.display = 'none';
}

function addHidden(form, name, value) {
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.id = name;
    input.innerHTML = value;
    form.appendChild(input);
}

function submitTask() {
	currentTimer = new Date().getTime();
	writingTimer += currentTime - currentTimerStart;
	var form = document.getElementById('mturkForm');
	addHidden(form, 'readingTime', readingTime.toString());
	addHidden(form, 'writingTime', writingTime.toString());
	form.submit();
}

var currentTimerStart = 0;
var writingTimer = 0;
var readingTimer = 0;
