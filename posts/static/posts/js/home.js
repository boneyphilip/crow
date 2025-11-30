/* ==========================================================
   AJAX Upvote + Downvote for Home Page
   ========================================================== */

console.log("[HOME] JS Loaded");

document.addEventListener("DOMContentLoaded", () => {
  const csrftoken = getCookie("csrftoken");

  // ---- Add event listeners to all vote buttons ----
  document.querySelectorAll(".vote-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const postId = this.dataset.postId;
      const action = this.dataset.action; // "up" or "down"
      const countBox = document.getElementById(`vote-count-${postId}`);

      fetch(`/ajax/vote/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: new URLSearchParams({
          action: action,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          countBox.textContent = data.upvotes;
        })
        .catch((err) => console.error("Vote error:", err));
    });
  });
});

/* ------------------------------------------
    Helper: Get CSRF token from cookies
--------------------------------------------*/
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
