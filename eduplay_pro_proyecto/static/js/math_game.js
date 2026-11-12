document.addEventListener("DOMContentLoaded", () => {
    const questionBox = document.getElementById("question-box");
    const answerInput = document.getElementById("answer-input");
    const submitBtn = document.getElementById("submit-btn");
    const startBtn = document.getElementById("start-btn");
    const scoreDisplay = document.getElementById("score");
    const streakDisplay = document.getElementById("streak");
    const feedback = document.getElementById("feedback");

    let currentAnswer = 0;
    let score = 0;
    let streak = 0;

    function generateQuestion() {
        const operators = ["+", "-", "*", "/"];
        const op = operators[Math.floor(Math.random() * operators.length)];
        let a = Math.floor(Math.random() * 20) + 1;
        let b = Math.floor(Math.random() * 15) + 1;

        if (op === "+") {
            currentAnswer = a + b;
            questionBox.textContent = `¿Cuánto es ${a} + ${b}?`;
        } else if (op === "-") {
            if (a < b) [a, b] = [b, a];
            currentAnswer = a - b;
            questionBox.textContent = `¿Cuánto es ${a} - ${b}?`;
        } else if (op === "*") {
            a = Math.floor(Math.random() * 12) + 1;
            b = Math.floor(Math.random() * 12) + 1;
            currentAnswer = a * b;
            questionBox.textContent = `¿Cuánto es ${a} × ${b}?`;
        } else if (op === "/") {
            b = Math.floor(Math.random() * 10) + 1;
            currentAnswer = Math.floor(Math.random() * 12) + 1;
            a = b * currentAnswer;
            questionBox.textContent = `¿Cuánto es ${a} ÷ ${b}?`;
        }

        answerInput.value = "";
        answerInput.focus();
    }

    function checkAnswer() {
        const userVal = parseInt(answerInput.value, 10);
        if (isNaN(userVal)) return;

        if (userVal === currentAnswer) {
            score++;
            streak++;
            feedback.textContent = "¡Excelente! Respuesta correcta.";
            feedback.style.color = "#16a34a";
        } else {
            streak = 0;
            feedback.textContent = `Incorrecto. La respuesta correcta era ${currentAnswer}.`;
            feedback.style.color = "#dc2626";
        }

        scoreDisplay.textContent = score;
        streakDisplay.textContent = streak;
        generateQuestion();
    }

    startBtn.addEventListener("click", () => {
        score = 0;
        streak = 0;
        scoreDisplay.textContent = score;
        streakDisplay.textContent = streak;
        feedback.textContent = "";
        answerInput.disabled = false;
        submitBtn.disabled = false;
        generateQuestion();
    });

    submitBtn.addEventListener("click", checkAnswer);
    answerInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") checkAnswer();
    });
});
