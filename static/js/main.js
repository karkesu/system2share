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

	goToPage(targetLink);
	return false;
}

function clickSubmitReview() {
	var elements = document.getElementById('LikertForm').elements;
	var targetLink = elements['targetLink'].value;
	var curr_cat = elements['curr_cat'].value;
	var summary_evaluation = elements['summary_evaluation'].value;
	var prior_knowledge = elements['prior_knowledge'].value;
	var learning = elements['learning'].value;

	targetLink += "&"+curr_cat+"_likert_="+summary_evaluation;
	targetLink += "&"+curr_cat+"_likert_="+prior_knowledge;
	targetLink += "&"+curr_cat+"_likert_="+learning;
	alert(targetLink);
	console.log(targetLink);
	// alert(targetLink);
	if (curr_cat != "uber"){
		curr_cat = getNextCat(curr_cat);
		targetLink += "&curr_cat="+curr_cat;
		goToPage(targetLink);
	} else {
		// submit to our server
		form.submit();
	}
}

// Only call this at step 2 (about to move on to a new category)
function getNextCat(curr_cat) {
	var next = {'amazon':'apple','apple':'uber','uber':'amazon'}
    return next[cat]
}

var currentTimerStart = new Date().getTime();
var writingTime = 0;
var readingTime = 0;

// Hackily watching for newsfeed articles. 
window.onload=function(){
	var one = document.getElementById("1")
	var two = document.getElementById("2")
	if (one != null && two != null) {
		document.getElementById("1").addEventListener ("click", redirectURL, false);
		document.getElementById("2").addEventListener ("click", redirectURL, false);
	}
}
