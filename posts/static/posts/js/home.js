document.addEventListener("DOMContentLoaded", () => {
  console.log("Home.js loaded — voting system ready!");

  // All vote buttons
  const voteButtons = document.querySelectorAll(".vote-btn");

  voteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const postId = this.getAttribute("data-post-id");
      const action = this.getAttribute("data-action");

      console.log("Vote clicked:", postId, action);

      // POST request to backend
      fetch(`/ajax/vote/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `action=${action}`,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Server responded:", data);

          if (data.error) {
            console.error("Vote error:", data.error);
            return;
          }

          // Update vote count on UI
          const voteCountElement = document.getElementById(
            `vote-count-${postId}`
          );
          voteCountElement.textContent = data.score;
        })
        .catch((error) => console.error("Fetch error:", error));
    });
  });
});

// CSRF TOKEN HELPER (IMPORTANT)
function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
      cookie = cookie.trim();

      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
