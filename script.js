const micButton = document.getElementById('micButton');
const responseBox = document.getElementById('response');
const loading = document.getElementById('loading');

let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';

micButton.addEventListener('click', () => {
    recognition.start();
    loading.style.display = 'block';
});

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    responseBox.innerHTML += `<div>User: ${transcript}</div>`;
    
    fetch('http://localhost:5000/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: transcript })
    })
    .then(response => response.json())
    .then(data => {
        responseBox.innerHTML += `<div>JARVIS: ${data.response}</div>`;
        loading.style.display = 'none';
    });
};

recognition.onerror = () => {
    loading.style.display = 'none';
};
