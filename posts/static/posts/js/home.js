/* ==========================================================
   HOME PAGE — AJAX Voting
========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[HOME] Voting + Gallery JS loaded");

  /* -------------------------------
      VOTING LOGIC
  -------------------------------- */
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

  /* -------------------------------
      REDDIT-STYLE MEDIA SLIDER
  -------------------------------- */
  document.querySelectorAll(".media-gallery").forEach((gallery) => {
    const track = gallery.querySelector(".gallery-track");
    const slides = gallery.querySelectorAll(".gallery-item");
    const prevBtn = gallery.querySelector(".gallery-prev");
    const nextBtn = gallery.querySelector(".gallery-next");
    const dots = gallery.querySelectorAll(".gallery-dots span");

    let currentIndex = 0;
    const total = slides.length;

    function updateGallery() {
      track.style.transform = `translateX(-${currentIndex * 100}%)`;

      dots.forEach((dot, i) => {
        dot.classList.toggle("active", i === currentIndex);
      });
    }

    /* Next button */
    nextBtn.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % total;
      updateGallery();
    });

    /* Previous button */
    prevBtn.addEventListener("click", () => {
      currentIndex = (currentIndex - 1 + total) % total;
      updateGallery();
    });

    /* Dot navigation */
    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        currentIndex = i;
        updateGallery();
      });
    });
  });
});

/* CSRF helper */
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
