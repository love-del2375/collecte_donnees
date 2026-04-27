<meta name='viewport' content='width=device-width, initial-scale=1'/><script>document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function (event) {
            const age = form.age.value;
            const poids = form.poids.value;
            const taille = form.taille.value;
            const tension = form.tension.value;

            let errors = [];

            if (age <= 0) errors.push("L'âge doit être supérieur à 0.");
            if (poids <= 0) errors.push("Le poids doit être supérieur à 0.");
            if (taille <= 0) errors.push("La taille doit être supérieure à 0.");
            if (tension <= 50 || tension >= 250) errors.push("La tension doit être comprise entre 50 et 250 mmHg.");

            if (errors.length > 0) {
                event.preventDefault();
                alert("Erreur(s) détectée(s):\n" + errors.join("\n"));
            }
        });

        const button = document.querySelector("button");
        if (button) {
            button.addEventListener("mouseover", () => {
                button.style.transform = "scale(1.05)";
            });
            button.addEventListener("mouseout", () => {
                button.style.transform = "scale(1)";
            });
        }
    }
});</script>