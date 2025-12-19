// static/js/translator.js (New file)

const container = document.getElementById("videoContainer");
const statusElement = document.getElementById("status");
const inputElement = document.getElementById("textInput");

// --- Initialization ---
window.onload = () => {
    // Start with the default idle video on load
    renderVideo("/static/videos/idle.mp4", true, "Welcome to SignSpeak!");
};



function renderVideo(src, loop, message) {
    const uniqueSrc = src + "?v=" + new Date().getTime();

    container.innerHTML = "";
    statusElement.innerText = message;

    const video = document.createElement("video");
    video.src = uniqueSrc;

    video.autoplay = true;
    video.muted = true;   // ✅ REQUIRED
    video.playsInline = true;

    if (loop) video.loop = true;

    container.appendChild(video);

    video.load();
    video.play().catch(() => console.log("Autoplay blocked"));

    if (!loop) {
        video.onended = () => {
            renderVideo("/static/videos/idle.mp4", true, "Ready");
        };
    }
}



/**
 * Handles the user input and fetches the video URL from Flask.
 */
function translateAndAnimate() {
    const text = inputElement.value.trim();
    
    if (!text) {
        renderVideo("/static/videos/idle.mp4", true, "Please type a word.");
        return;
    }

    statusElement.innerText = `Translating "${text}"...`;

    fetch("/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        // data.idle tells us if the video should loop (default/error)
        const message = data.message || `Sign for "${text}" is complete.`;
        renderVideo(data.video, data.idle, message);
    })
    .catch(error => {
        statusElement.innerText = "Error contacting server. Check console.";
        renderVideo("/static/videos/idle.mp4", true, "Connection Error."); 
    });
}

// Attach the main function to the global scope for the button
window.translateAndAnimate = translateAndAnimate;