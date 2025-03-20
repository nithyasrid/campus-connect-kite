function submitConfession() {
    let input = document.getElementById("confessionInput");
    let confessionText = input.value.trim();

    if (confessionText === "") {
        alert("Please write something before submitting!");
        return;
    }

    let confessionList = document.getElementById("confessionList");

    // Create a new confession card
    let confessionCard = document.createElement("div");
    confessionCard.classList.add("card", "bg-light", "text-dark", "mt-3", "p-3");
    confessionCard.innerHTML = `<p>${confessionText}</p>`;

    // Append to list
    confessionList.prepend(confessionCard);
    input.value = ""; // Clear input
}
