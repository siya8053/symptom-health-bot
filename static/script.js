let selected = [];

document.querySelectorAll(".pill").forEach(btn => {

    btn.addEventListener("click", () => {

        btn.classList.toggle("active");

        let value = btn.innerText.toLowerCase();

        if (selected.includes(value)) {
            selected = selected.filter(v => v !== value);
        } else {
            selected.push(value);
        }
    });
});

function analyze() {

    // EXTRA SYMPTOMS FROM TEXTAREA
    let extra = document.getElementById("extra")
    .value
    .toLowerCase()
    .split(",");

    extra = extra.map(e => e.trim());

    let finalSymptoms = [...selected, ...extra];

    fetch("/analyze", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            symptoms: finalSymptoms
        })
    })

    .then(res => res.json())

    .then(data => {

        let html = "";

        if (data.length === 0) {
            html = `
            <div class="result-card">
                <p>No matching condition found.</p>
            </div>
            `;
        }

        data.forEach(d => {

            html += `

            <div class="result-card">

                <h3>
                    <i class="fa-solid fa-stethoscope"></i>
                    ${d.name} (${d.percent}% Match)
                </h3>

                <p>
                    <b>About:</b>
                    ${d.desc}
                </p>

                <p>
                    <b>
                    <i class="fa-solid fa-circle-question"></i>
                    Why it may happen:
                    </b>
                </p>

                <ul>
                    ${d.causes.map(c =>
                        `<li>${c}</li>`).join("")}
                </ul>

                <p>
                    <b>
                    <i class="fa-solid fa-shield-heart"></i>
                    Precautions:
                    </b>
                </p>

                <ul>
                    ${d.precautions.map(p =>
                        `<li>${p}</li>`).join("")}
                </ul>

                <p>
                    <b>
                    <i class="fa-solid fa-leaf"></i>
                    Remedies:
                    </b>
                </p>

                <ul>
                    ${d.remedy.map(r =>
                        `<li>${r}</li>`).join("")}
                </ul>

                <div class="warning">
                    <i class="fa-solid fa-triangle-exclamation"></i>

                    If symptoms become severe or continue for a long time,
                    consult a doctor immediately.
                </div>

                <div class="motivation">
                    <i class="fa-solid fa-heart"></i>

                    Take care of yourself.
                    Small healthy habits every day create a stronger future.
                </div>

            </div>
            `;
        });

        document.getElementById("results").innerHTML = html;
    })

    .catch(err => {
        console.error(err);
    });
}