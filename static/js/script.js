


document.addEventListener("DOMContentLoaded", function() {
    var quienesSomosBtn = document.getElementById("quienes-somos-btn");
    var quienesSomosContent = document.getElementById("quienes-somos-content");

    quienesSomosBtn.addEventListener("click", function(event) {
        event.preventDefault();
        if (quienesSomosContent.style.display === "none") {
            quienesSomosContent.style.display = "block";
        } else {
            quienesSomosContent.style.display = "none";
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var politicaPrivacidadBtn = document.getElementById("politica-privacidad-btn");
    var politicaPrivacidadContent = document.getElementById("politica-privacidad-content");

    politicaPrivacidadBtn.addEventListener("click", function(event) {
        event.preventDefault();
        if (politicaPrivacidadContent.style.display === "none") {
            politicaPrivacidadContent.style.display = "block";
        } else {
            politicaPrivacidadContent.style.display = "none";
        }
    });
});