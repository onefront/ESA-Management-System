document.addEventListener("DOMContentLoaded", function () {

    const recipientGroup = document.getElementById("recipientGroup");
    const dynamicFilter = document.getElementById("dynamicFilter");
    const previewBtn = document.getElementById("previewBtn");

    // ============================
    // Recipient Group Change
    // ============================

    recipientGroup.addEventListener("change", function () {

        const value = this.value;

        dynamicFilter.innerHTML = "";

        if (value === "programme") {

            dynamicFilter.innerHTML = `
                <label class="form-label">Select Programme</label>
                <select class="form-select">
                    <option value="">-- Select Programme --</option>
                    ${programmes.map(p => `
                        <option value="${p.id}">
                            ${p.programme_name}
                        </option>
                    `).join("")}
                </select>
            `;

        }

        else if (value === "department") {

            dynamicFilter.innerHTML = `
                <label class="form-label">Select Department</label>
                <select class="form-select">
                    <option value="">-- Select Department --</option>
                    ${departments.map(d => `
                        <option value="${d.id}">
                            ${d.department_name}
                        </option>
                    `).join("")}
                </select>
            `;

        }

        else if (value === "faculty") {

            dynamicFilter.innerHTML = `
                <label class="form-label">Select Faculty</label>
                <select class="form-select">
                    <option value="">-- Select Faculty --</option>
                    ${faculties.map(f => `
                        <option value="${f.id}">
                            ${f.faculty_name}
                        </option>
                    `).join("")}
                </select>
            `;

        }

        else if (value === "level") {

            dynamicFilter.innerHTML = `
                <label class="form-label">Select Level</label>
                <select class="form-select">
                    <option value="">-- Select Level --</option>
                    <option value="100">Level 100</option>
                    <option value="200">Level 200</option>
                    <option value="300">Level 300</option>
                    <option value="400">Level 400</option>
                </select>
            `;

        }

        else if (value === "selected") {

            dynamicFilter.innerHTML = `
                <label class="form-label">Search Members</label>

                <input
                    type="text"
                    id="memberSearch"
                    class="form-control mb-3"
                    placeholder="Search by name or Student ID">

                <div
                    id="memberResults"
                    class="border rounded p-2"
                    style="max-height:300px;overflow-y:auto;">

                    Loading members...

                </div>

                <div class="mt-2">
                    <strong>
                        Selected Members:
                        <span id="selectedCount">0</span>
                    </strong>
                </div>
            `;

            loadMembers("");

            document
                .getElementById("memberSearch")
                .addEventListener("keyup", function () {

                    loadMembers(this.value);

                });

        }

    });

    // ============================
    // Preview
    // ============================

    previewBtn.addEventListener("click", function () {

        const title =
            document.getElementById("smsTitle").value;

        const message =
            document.getElementById("smsMessage").value;

        const recipient =
            document.getElementById("recipientGroup").value;

        let recipients = recipient;

        if (recipient === "selected") {

            recipients =
                document.querySelectorAll(".memberCheck:checked").length +
                " Selected Member(s)";

        }

        document.getElementById("previewTitle").textContent =
            title || "(No title)";

        document.getElementById("previewRecipients").textContent =
            recipients;

        document.getElementById("previewCharacters").textContent =
            message.length;

        document.getElementById("previewMessage").textContent =
            message || "(No message entered)";

        new bootstrap.Modal(
            document.getElementById("previewModal")
        ).show();

    });

});


// ============================
// Load Members
// ============================

async function loadMembers(search) {

    const results =
        document.getElementById("memberResults");

    const response =
        await fetch(
            "/sms/search-members?q=" +
            encodeURIComponent(search)
        );

    const members =
        await response.json();

    results.innerHTML = "";

    members.forEach(member => {

        results.innerHTML += `
            <div class="form-check">

                <input
                    class="form-check-input memberCheck"
                    type="checkbox"
                    value="${member.id}">

                <label class="form-check-label">

                    <strong>${member.name}</strong><br>

                    <small>

                        ${member.student_id}

                        |

                        ${member.programme}

                        |

                        Level ${member.level}

                    </small>

                </label>

            </div>
        `;

    });

    document
        .querySelectorAll(".memberCheck")
        .forEach(box => {

            box.addEventListener("change", function () {

                document.getElementById("selectedCount").innerText =
                    document.querySelectorAll(".memberCheck:checked").length;

            });

        });

}


// =====================================
// Send SMS
// =====================================

document.addEventListener("click", async function (e) {
console.log("Clicked:", e.target.id);
    if (e.target.id !== "sendSMSBtn") return;

console.log("Send SMS button detected");

    const title = document.getElementById("smsTitle").value;

    const message = document.getElementById("smsMessage").value;

    const recipientGroup =
        document.getElementById("recipientGroup").value;

    const selectedMembers = [];

    document.querySelectorAll(".memberCheck:checked")
        .forEach(box => {

            selectedMembers.push(box.value);

        });

    const response = await fetch("/sms/send", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            title,

            message,

            recipient_group: recipientGroup,

            selected_members: selectedMembers

        })

    });

    const result = await response.json();

    alert(result.message);

});