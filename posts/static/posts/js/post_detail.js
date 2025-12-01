/* ==========================================================
   POST DETAIL PAGE — JS for Reply Form Toggle
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // Select all reply buttons
  const replyButtons = document.querySelectorAll(".reply-toggle");

  replyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      // Get the comment ID (from data-id="{{ comment.id }}")
      const commentId = btn.getAttribute("data-id");

      // Find the corresponding reply form
      const replyForm = document.getElementById(`reply-form-${commentId}`);

      if (!replyForm) return;

      // Toggle visible / hidden
      if (
        replyForm.style.display === "none" ||
        replyForm.style.display === ""
      ) {
        replyForm.style.display = "block";
        btn.textContent = "Cancel"; // change button text
      } else {
        replyForm.style.display = "none";
        btn.textContent = "Reply"; // revert text
      }
    });
  });
});

/* ==========================================================
   POST DETAIL — AJAX Voting (Upvote + Downvote)
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[DETAIL] Voting script loaded");

  const voteButtons = document.querySelectorAll(".vote-btn");

  voteButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const postId = btn.getAttribute("data-post-id");
      const action = btn.getAttribute("data-action");

      console.log("[DETAIL] Vote clicked:", postId, action);

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
          console.log("[DETAIL] Server responded:", data);

          if (!data.success) return;

          // Update UI
          document.getElementById("detail-vote-count").textContent =
            data.upvotes;
        })
        .catch((err) => console.error("Vote error:", err));
    });
  });
});

// CSRF helper
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
