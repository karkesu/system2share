// Send data to be logged
function postData(logObject) {
	var logJSON = JSON.stringify(logObject);
	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", "./log.php", true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(logJSON);
}

// things to be done when the trial completes
function completeExperiment() {
	postData(log);
	clearContent();
	var t = document.querySelector('#end');
	var clone = document.importNode(t.content, true);
	contentBlock.appendChild(clone);
}

// renders the form that gets user data from the template in index.html
function showUserInfoForm() {
	var t = document.querySelector('#user-info-form');
	var clone = document.importNode(t.content, true);
	contentBlock.appendChild(clone);
}

// handles the user pressing submit on the form; stores data and advances the experiment
function handleUserInfoSubmit() {
	var form = document.querySelector('#form');
	log.name = document.querySelector('#name').value;
	// log.email = document.querySelector('#email').value;
	log.device = document.querySelector('#device').value;
	advanceExperiment();
	return false;
}

// shows a prompt by adding the necessary content to the prompt template
function showPrompt(prompt) {
	var t = document.querySelector('#prompt');
	t.content.querySelector('#prompt-title').textContent = prompt.promptTitle;
	t.content.querySelector('#prompt-text').textContent = prompt.promptText;
	t.content.querySelector('#prompt-image').src = prompt.promptImage;
	var clone = document.importNode(t.content, true);
	contentBlock.appendChild(clone);
}

// shows a trial by adding the necessary content to the trial template
function showTrial(trial) {

	// add data about trial to template
	var t = document.querySelector('#trial');
	t.content.querySelector('#trial-text').textContent = trial.trialText;
	var clone = document.importNode(t.content, true);
	contentBlock.appendChild(clone);

	// add click listeners to option buttons
	var optionButtons = document.querySelectorAll('.option');
	for (var i = 0; i < optionButtons.length; i++) {
		optionButtons[i].addEventListener('click', function() { makeTrialSelection(this.id); });
	}

}

// called when an option is selected for a trial
function makeTrialSelection(id) {
	// store the user's action
	log.experiment[experimentProgress].action = "";

	// move to the trial results
	clearContent();
	showTrialComplete();
}

// shows the result at the end of the trial
function showTrialComplete() {
	var t = document.querySelector('#trial-complete');
	t.content.querySelector('#trial-text').textContent = experiment[experimentProgress].trialText;
	t.content.querySelector('#trial-image').src = experiment[experimentProgress].trialImage;
	var clone = document.importNode(t.content, true);
	contentBlock.appendChild(clone);
}

// a utility functiont to empty the content block
function clearContent() {
	contentBlock.innerHTML = '';
}

// move the experiment forward
function advanceExperiment() {
	clearContent();
	experimentProgress++;
	if (experimentProgress < experiment.length) showExperimentBlock(experimentProgress);
	else completeExperiment();
}

// render the experiment step we are currently at
function showExperimentBlock(i) {
	if (experiment[i].dataType == 'prompt') showPrompt(experiment[i]);
	if (experiment[i].dataType == 'trial') showTrial(experiment[i]);
}

var contentBlock = document.querySelector('#content');

// function for looping a trial
function createTrial() {
	// 	var trial = {}
	// 	experiment.push(trial)
}

// function for making one experiment
function createExperiment() {

	var experiment = [];

	var prompt = {};
	prompt.dataType = '';
	prompt.promptTitle = '';
	prompt.promptText = '';
	prompt.promptImage = '';
	experiment.push(prompt);

	createTrial();
	return experiment;
}

experiment = createExperiment();

// current experiment step
// (this starts at -1 because we start at the user info form, which calls advanceExperiment() which increments
// this before it actually renders anything)
var experimentProgress = -1;

// create log object
var log = new Object();
log.date = new Date();
log.experiment = experiment;

// start by rendering the user info form
showUserInfoForm();
