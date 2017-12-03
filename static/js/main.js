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

function goToPage(link) {
	window.location = link;
}

function redirectURL() {
	var id = this.id;
	this.setAttribute("href",this.href+"&curr_article="+this.id);
	alert(this.href);
	goToPage(this.href);
}

function clickSubmit() {
	currentTime = new Date().getTime();
	writingTime += currentTime - currentTimerStart;
	var form = document.getElementById('mturkForm');
	addHidden(form, 'readingTime', readingTime.toString());
	addHidden(form, 'writingTime', writingTime.toString());
	var elements = form.elements;

	// alert("WHAT IS GOING ON");

	var targetLink = elements['targetLink'].value;
	var category = elements['curr_cat'].value;
    var promptId = elements['promptId'].value;
    var time_reading = elements['readingTime'].value;
    var time_writing = elements['writingTime'].value;
    var annotation = elements['annotation'].value;
	
	targetLink += "&"+category+"_promptId="+promptId;
	targetLink += "&"+category+"_time_reading="+time_reading;
	targetLink += "&"+category+"_time_writing="+time_writing;
	targetLink += "&"+category+"_annotation="+annotation;

	// alert(targetLink);
	if (category != "uber"){
		goToPage(targetLink);
		return false;
	} else {
		form.submit();
	}
}

var currentTimerStart = new Date().getTime();
var writingTime = 0;
var readingTime = 0;

window.onload=function(){
    document.getElementById("1").addEventListener ("click", redirectURL, false);
	document.getElementById("2").addEventListener ("click", redirectURL, false);
}
