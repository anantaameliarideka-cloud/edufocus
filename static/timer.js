let studyTime = 25 * 60;
let breakTime = 5 * 60;
let timeLeft = studyTime;
let isStudy = true;
let timerInterval = null;

function formatTime(seconds) {
    let m = Math.floor(seconds / 60);
    let s = seconds % 60;
    return `${m}:${s < 10 ? "0" : ""}${s}`;
}

function updateTimer() {
    const timer = document.getElementById("timer");
    if (!timer) return;

    timer.innerText = formatTime(timeLeft);

    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        timerInterval = null;

        if (isStudy) {
            alert("⏸️ Waktunya ISTIRAHAT 5 menit!");
            timeLeft = breakTime;
        } else {
            alert("🔥 Waktunya BELAJAR lagi 25 menit!");
            timeLeft = studyTime;
        }

        isStudy = !isStudy;
        startTimer();
        return;
    }

    timeLeft--;
}

function startTimer() {
    if (timerInterval) return;
    timerInterval = setInterval(updateTimer, 1000);
}

function resetTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    isStudy = true;
    timeLeft = studyTime;
    const timer = document.getElementById("timer");
    if (timer) timer.innerText = formatTime(timeLeft);
}
