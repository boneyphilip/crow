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
