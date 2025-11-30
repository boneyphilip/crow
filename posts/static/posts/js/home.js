/* ============================================================
   HOME PAGE — AJAX Upvote & Downvote
   ============================================================ */

console.log("home.js loaded");

// Attach click listeners to all vote buttons
document.querySelectorAll(".vote-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const postId = this.dataset.postId;
    const action = this.dataset.action; // "up" or "down"

    if (!postId || !action) {
      console.error("Missing data attributes on vote button");
      return;
    }

    // Make AJAX request
    fetch(`/ajax/vote/${postId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action: action }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          const countBox = document.getElementById(`vote-count-${postId}`);
          if (countBox) {
            countBox.textContent = data.upvotes;
          }
        } else {
          console.error("Vote error:", data.error);
        }
      })
      .catch((err) => console.error("AJAX failed:", err));
  });
});

// Helper to get CSRF cookie
function getCookie(name) {
  let cookieValue = null;
  const cookies = document.cookie.split(";");

  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
      cookieValue = decodeURIComponent(cookie.split("=")[1]);
      break;
    }
  }
  return cookieValue;
}
