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

function addHidden(form, key, value) {
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = value;
    form.appendChild(input);
}

function submitTask() {
	currentTime = new Date().getTime();
	writingTime += currentTime - currentTimerStart;
	var form = document.getElementById('mturkForm');
	addHidden(form, 'dummy', 'testing');
	addHidden(form, 'readingTime', readingTime.toString());
	addHidden(form, 'writingTime', writingTime.toString());
	form.submit();
}

var currentTimerStart = 0;
var writingTimer = 0;
var readingTimer = 0;
