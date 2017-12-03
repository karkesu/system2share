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

function createDynamicURL() {
	var URL;
	// console.log(form)
	var article_selected = parent.firstChild;
	var params = {}
	params['task'] = '';
	params['newsfeed'] = '';
	params['newsfeed_order'] = '';
	params['promptId'] = '';
	params['prompt'] = '';
	params['placeholder'] = '';
	params['curr_cat'] = '';
	params['curr_article'] = '';
	params['curr_articleTitle'] = '';
	params['curr_articleByLine'] = '';
	params['curr_articleText'] = '';
	params['assignmentId'] = '';
	params['hitId'] = '';
	params['workerId'] = '';
	params['amazon_newsfeed_order'] = '';
	params['amazon_newsfeed_annotation_a1'] = '';
	params['amazon_newsfeed_annotation_a2'] = '';
	params['amazon_articleId'] = '';
	params['amazon_promptId'] = '';
	params['amazon_time_reading'] = '';
	params['amazon_time_writing'] = '';
	params['amazon_annotation'] = '';
	for (p in params){
		if (p != ''){
			console.log(p);
		}
	}
}

function redirectURL() {
	console.log(this.firstChild.value);
	console.log(this);
	// window.location= createDynamicURL();
}

function submitTask() {
	currentTime = new Date().getTime();
	writingTime += currentTime - currentTimerStart;
	var form = document.getElementById('mturkForm');
	addHidden(form, 'readingTime', readingTime.toString());
	addHidden(form, 'writingTime', writingTime.toString());
	form.submit();
}

var currentTimerStart = new Date().getTime();
var writingTime = 0;
var readingTime = 0;
document.getElementById ("article_summary").addEventListener ("click", redirectURL, false);
