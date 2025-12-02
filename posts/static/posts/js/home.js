/* ==========================================================
   HOME PAGE — AJAX Voting
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[HOME] Voting JS loaded");

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

        const countEl = document.getElementById(`vote-count-${postId}`);
        if (countEl) countEl.textContent = data.upvotes;
      })
      .catch((err) => console.error(err));
  });
});

function getCookie(name) {
  let value = null;
  document.cookie.split(";").forEach((cookie) => {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
      value = decodeURIComponent(cookie.slice(name.length + 1));
    }
  });
  return value;
}
