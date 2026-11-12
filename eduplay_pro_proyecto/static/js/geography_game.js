document.addEventListener("DOMContentLoaded", () => {
    const trivia = [
        { q: "¿Cuál es la capital del estado Mérida?", options: ["Mérida", "Ejido", "El Vigía", "Tovar"], answer: "Mérida" },
        { q: "¿Cuál es el río más largo y caudaloso de Venezuela?", options: ["Río Orinoco", "Río Caroní", "Río Apure", "Río Chama"], answer: "Río Orinoco" },
        { q: "¿Cuál es el árbol nacional de Venezuela?", options: ["El Araguaney", "La Ceiba", "El Samán", "El Bucare"], answer: "El Araguaney" },
        { q: "¿En qué estado se encuentra el Salto Ángel (Kerepakupai Merú)?", options: ["Bolívar", "Amazonas", "Delta Amacuro", "Monagas"], answer: "Bolívar" },
        { q: "¿Cuál es el punto más alto de Venezuela?", options: ["Pico Bolívar", "Pico Humboldt", "Pico Naiguatá", "Roraima"], answer: "Pico Bolívar" },
        { q: "¿Cuál es la capital del estado Lara?", options: ["Barquisimeto", "Carora", "Cabudare", "El Tocuyo"], answer: "Barquisimeto" },
        { q: "¿Cuál es el ave nacional de Venezuela?", options: ["El Turpial", "El Cardenalito", "La Guacamaya", "El Cóndor"], answer: "El Turpial" },
        { q: "¿Cuál es la flor nacional de Venezuela?", options: ["La Orquídea", "La Cayena", "La Rosa de Montaña", "El Lirio"], answer: "La Orquídea" }
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
        if (currentIndex >= trivia.length) {
            questionBox.textContent = `¡Trivia completada! Obtuviste ${score} de ${trivia.length} aciertos.`;
            optionsBox.innerHTML = "";
            return;
        }

        const item = trivia[currentIndex];
        progressDisplay.textContent = `${currentIndex + 1} / ${trivia.length}`;
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
            feedback.textContent = "¡Correcto! Conoces muy bien nuestra geografía.";
            feedback.style.color = "#16a34a";
        } else {
            feedback.textContent = `Incorrecto. La respuesta correcta es: ${correct}.`;
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
