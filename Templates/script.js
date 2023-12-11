const output = document.getElementById('output');
const start = document.getElementById('start');
const stop = document.getElementById('stop');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

start.addEventListener('click', () => {
    recognition.start();
    console.log('recognition started');
})

recognition.lang = 'en';
recognition.interimResults = false;
recognition.continuous = true;

recognition.onresult = (event) => {
    output.textContent += event.results[event.results.length - 1][0].transcript;
    console.log(event);
}

stop.addEventListener('click', () => {
    recognition.stop();
    console.log('recognition stopped');
})