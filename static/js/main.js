function startWritingTimer() {
	currentTime = new Date().getTime();
	readingTime += currentTime - currentTimerStart;
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
    input.value = value;
    form.appendChild(input);
}

function submitArticle() {
	currentTime = new Date().getTime();
	writingTime += currentTime - currentTimerStart;
	var form = document.getElementById('mturkForm');
	addHidden(form, 'readingTime', readingTime.toString());
	addHidden(form, 'writingTime', writingTime.toString());
	form.submit();
}

function submitReview() {
	var form = document.getElementById('LikertForm');
	form.submit()	
}

var currentTimerStart = new Date().getTime();
var writingTime = 0;
var readingTime = 0;
