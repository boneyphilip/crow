/* ==========================================================
   POST DETAIL — Reply Form Toggle
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  document.body.addEventListener("click", (e) => {
    if (!e.target.classList.contains("reply-toggle")) return;

    const btn = e.target;
    const id = btn.dataset.id;

    const form = document.getElementById(`reply-form-${id}`);
    if (!form) return;

    const isHidden = form.style.display === "" || form.style.display === "none";

    form.style.display = isHidden ? "block" : "none";
    btn.textContent = isHidden ? "Cancel" : "Reply";
  });
});

/* ==========================================================
   POST DETAIL — AJAX Voting
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[DETAIL] Vote JS loaded");

  document.body.addEventListener("click", (e) => {
    if (!e.target.classList.contains("vote-btn")) return;

    const btn = e.target;
    const postId = btn.dataset.postId;
    const action = btn.dataset.action;

    fetch(`/ajax/vote/${postId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.success) return;

        const el = document.getElementById("detail-vote-count");
        if (el) el.textContent = data.upvotes;
      })
      .catch((err) => console.error("Vote error:", err));
  });
});

/* ==========================================================
   CSRF Cookie Helper (REQUIRED)
   ========================================================== */
function getCookie(name) {
  let cookieValue = null;
  document.cookie.split(";").forEach((cookie) => {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    }
  });
  return cookieValue;
}
