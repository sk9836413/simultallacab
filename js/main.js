// ===== Apna number yahan badlein (sirf 10 digit, bina +91 ke) =====
const PHONE = "8210942813";
const WHATSAPP = PHONE; // WhatsApp number alag ho to yahan likhein
// ==================================================================

const WA_GREETING = "नमस्ते, मुझे Simultala Cab Service से गाड़ी बुक करनी है।";

const telHref = `tel:+91${PHONE}`;
const waLink = (text) => `https://wa.me/91${WHATSAPP}?text=${encodeURIComponent(text)}`;
const pretty = `${PHONE.slice(0, 5)} ${PHONE.slice(5)}`;

document.querySelectorAll("[data-call]").forEach((a) => { a.href = telHref; });
document.querySelectorAll("[data-wa]").forEach((a) => {
  const topic = a.dataset.msg;
  a.href = waLink(topic ? `${WA_GREETING}\n${topic} के बारे में जानकारी और कीमत बताएँ।` : WA_GREETING);
});
document.querySelectorAll("[data-phone-text]").forEach((el) => { el.textContent = pretty; });

const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

// Booking form (home page only) -> opens WhatsApp with the trip details filled in
const form = document.getElementById("book-form");
if (form) {
  const error = form.querySelector(".form__error");
  const dateInput = form.elements.date;
  dateInput.min = new Date().toISOString().slice(0, 10);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const required = ["from", "to", "date"].map((n) => form.elements[n]);
    let ok = true;
    required.forEach((field) => {
      const empty = !field.value.trim();
      field.setAttribute("aria-invalid", empty ? "true" : "false");
      if (empty) ok = false;
    });
    error.hidden = ok;
    if (!ok) {
      required.find((f) => !f.value.trim()).focus();
      return;
    }

    const d = form.elements;
    const date = new Date(d.date.value).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
    const message = [
      WA_GREETING,
      `पिकअप: ${d.from.value.trim()}`,
      `ड्रॉप: ${d.to.value.trim()}`,
      `तारीख: ${date}`,
      `गाड़ी: ${d.car.value}`,
      `होटल: ${d.hotel.value}`,
      "कृपया किराया बताएँ।",
    ].join("\n");
    window.open(waLink(message), "_blank", "noopener");
  });
}
