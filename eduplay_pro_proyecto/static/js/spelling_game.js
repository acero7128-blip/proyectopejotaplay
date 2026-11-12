document.addEventListener("DOMContentLoaded", () => {
    const questions = [
        { q: "Completa la palabra: El ár_ol del parque es muy alto.", options: ["b", "v"], answer: "b" },
        { q: "¿Cuál palabra está escrita correctamente?", options: ["Decisión", "Desición", "Decición"], answer: "Decisión" },
        { q: "Completa la oración: Mañana _amos a estudiar programación.", options: ["vamos", "bamos"], answer: "vamos" },
        { q: "Selecciona la palabra con tilde correcta:", options: ["Matemática", "Matematica", "Matématica"], answer: "Matemática" },
        { q: "Completa la palabra: El corre_o electrónico fue enviado.", options: ["r", "rr"], answer: "r" },
        { q: "¿Cuál es el sinónimo correcto de 'Veloz'?", options: ["Rápido", "Rapido", "Rápído"], answer: "Rápido" },
        { q: "Completa la palabra: La evaluación fue un é_ito.", options: ["x", "s", "c"], answer: "x" },
        { q: "Selecciona la forma correcta (uso de c/s/z):", options: ["Cazador", "Casador", "Cassador"], answer: "Cazador" }
    ];

    const questionBox = document.getElementById("question-box");
    const optionsBox = document.getElementById("options-box");
    const startBtn = document.getElementById("start-btn");
    const scoreDisplay = document.getElementById("score");
    const progressDisplay = document.getElementById("progress");
    const feedback = document.getElementById("feedback");

    let currentIndex = 0;
    let score = 0;

    function loadQuestion() {
        if (currentIndex >= questions.length) {
            questionBox.textContent = `¡Ejercicio finalizado! Puntaje: ${score} de ${questions.length}`;
            optionsBox.innerHTML = "";
            return;
        }

        const item = questions[currentIndex];
        progressDisplay.textContent = `${currentIndex + 1} / ${questions.length}`;
        questionBox.textContent = item.q;
        optionsBox.innerHTML = "";

        item.options.forEach(opt => {
            const btn = document.createElement("button");
            btn.className = "option-btn";
            btn.textContent = opt;
            btn.onclick = () => checkAnswer(opt, item.answer);
            optionsBox.appendChild(btn);
        });
    }

    function checkAnswer(selected, correct) {
        if (selected === correct) {
            score++;
            feedback.textContent = "¡Correcto! Buena ortografía.";
            feedback.style.color = "#16a34a";
        } else {
            feedback.textContent = `Incorrecto. La opción correcta era: "${correct}".`;
            feedback.style.color = "#dc2626";
        }
        scoreDisplay.textContent = score;
        currentIndex++;
        setTimeout(loadQuestion, 900);
    }

    startBtn.addEventListener("click", () => {
        currentIndex = 0;
        score = 0;
        scoreDisplay.textContent = score;
        feedback.textContent = "";
        loadQuestion();
    });
});
