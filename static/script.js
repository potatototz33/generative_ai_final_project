const form = document.querySelector("#event-form");
const button = document.querySelector("#search-button");
const status = document.querySelector("#status");
const resultsList = document.querySelector("#results-list");
document.querySelector("#day").min = new Date().toISOString().slice(0, 10);
const eventImages = ["🌱", "📣", "✊", "🫶", "🌈", "🗳️"];

document.querySelectorAll(".suggestion").forEach((suggestion) => {
  suggestion.addEventListener("click", () => {
    document.querySelector("#event_type").value = suggestion.dataset.event;
    document.querySelector("#event_type").focus();
  });
});
function showEvents(events) {
  resultsList.replaceChildren(...events.map((event, index) => {
    const card = document.createElement("article"); card.className = "event-bubble";
    const safeUrl = event.source_url && /^https?:\/\//i.test(event.source_url) ? event.source_url : "";
    const image = document.createElement("div"); image.className = "event-image"; image.setAttribute("aria-hidden", "true"); image.textContent = eventImages[index % eventImages.length];
    const number = document.createElement("span"); number.className = "event-number"; number.textContent = `SPUD PICK #${index + 1}`;
    const title = document.createElement("h3"); title.textContent = event.name;
    const meta = document.createElement("p"); meta.className = "event-meta";
    meta.append(`📍 ${event.location}`, document.createElement("br"), `🗓 ${event.date} · ${event.time}`);
    const description = document.createElement("p"); description.textContent = event.description;
    card.append(image, number, title, meta, description);
    if (safeUrl) {
      const link = document.createElement("a"); link.className = "source-link"; link.href = safeUrl;
      link.target = "_blank"; link.rel = "noopener noreferrer"; link.textContent = "Verify details ↗"; card.append(link);
    }
    return card;
  }));
}
form.addEventListener("submit", async (event) => {
  event.preventDefault(); const payload = Object.fromEntries(new FormData(form));
  button.disabled = true; button.querySelector("span").textContent = "Digging for gatherings…";
  status.className = "status loading"; status.textContent = "Our cheerful robot is checking current event details…"; resultsList.replaceChildren();
  try {
    const response = await fetch("/api/events", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload) });
    const data = await response.json(); if (!response.ok) throw new Error(data.detail || "The search could not be completed.");
    showEvents(data.events); status.className = "status"; status.textContent = data.search_note || `Here are ${data.events.length} places to get involved.`;
  } catch (error) { status.className = "status error"; status.textContent = error.message; }
  finally { button.disabled = false; button.querySelector("span").textContent = "Find my people"; }
});
