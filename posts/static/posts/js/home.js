/* ==========================================
   HOME PAGE — Main JavaScript
   ========================================== */

console.log("[HOME] JS Loaded Successfully");
console.log("[HOME] Vote script ready");

// Handle clicks on upvote and downvote
document.addEventListener("click", function (e) {
  if (e.target.classList.contains("upvote-btn")) {
    console.log("Upvote clicked:", e.target.dataset.post);
    // Django URL: /posts/<id>/upvote/
    window.location.href = `/posts/${e.target.dataset.post}/upvote/`;
  }

  if (e.target.classList.contains("downvote-btn")) {
    console.log("Downvote clicked:", e.target.dataset.post);
    // Django URL: /posts/<id>/downvote/
    window.location.href = `/posts/${e.target.dataset.post}/downvote/`;
  }
});
