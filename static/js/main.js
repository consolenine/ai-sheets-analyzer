$(document).ready(function() {
	const startBtn = $('#start-btn');
	const responseBtn = $("#play-response");
	const resultDiv = $('#result p');
	
	var recognition = null;
	var language = "en-IN";

	$("#lang-select").on('change', function() {
		language = $(this).val();
	})

	responseBtn.on('click', () => {
		speakResponse(resultDiv.text())
	})

	startBtn.on('touchstart mousedown', function() {
		recognition = new webkitSpeechRecognition() || SpeechRecognition();
		recognition.lang = language;

		recognition.onresult = function(event) {
			const transcript = event.results[0][0].transcript;
			console.log(transcript);
			processInput(transcript);
		};
		recognition.start();
		$("#result").css('display', 'flex');
	});
	startBtn.on('touchend mouseup', function() {
		$(this).blur();
		setTimeout(() => {
			recognition.stop();
		}, 1000);
	});

	function processInput(message) {
		var filename = new Date().toISOString();
		resultDiv.html("Processing....")
		$.ajax({
			url: '/process_input',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({message: message, language: language}),
			success: function(res) {
				console.log(res);
				if (res["data"]) {
					resultDiv.html(res["data"])
				} else {
					resultDiv.html("Unable to Process")
				}

				speakResponse(resultDiv.text())
			}
		})
	}

	function speakResponse(text) {
		var utterance = new SpeechSynthesisUtterance(text);
		utterance.lang = language;

		speechSynthesis.speak(utterance);
	}
	
});