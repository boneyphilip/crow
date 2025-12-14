/* ==========================================================
   POST DETAIL — Reply Form Toggle
========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* --- Reply toggle --- */
  document.body.addEventListener("click", (e) => {
    if (!e.target.classList.contains("reply-toggle")) return;

    const id = e.target.dataset.id;
    const box = document.getElementById(`reply-box-${id}`);
    if (!box) return;

    const isHidden = box.classList.contains("hidden");
    box.classList.toggle("hidden");

    e.target.textContent = isHidden ? "Cancel" : "Reply";
  });

  /* ==========================================================
     POST DETAIL — AJAX Voting
  ========================================================== */

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

  /* ==========================================================
     REDDIT-STYLE MEDIA SLIDER (MULTI MEDIA)
  ========================================================== */

  document.querySelectorAll(".media-gallery").forEach((gallery) => {
    const track = gallery.querySelector(".gallery-track");
    const slides = gallery.querySelectorAll(".gallery-item");
    const prevBtn = gallery.querySelector(".gallery-prev");
    const nextBtn = gallery.querySelector(".gallery-next");
    const dots = gallery.querySelectorAll(".gallery-dots span");

    let index = 0;
    const total = slides.length;

    function update() {
      track.style.transform = `translateX(-${index * 100}%)`;

      dots.forEach((dot, i) => {
        dot.classList.toggle("active", i === index);
      });
    }

    nextBtn?.addEventListener("click", () => {
      index = (index + 1) % total;
      update();
    });

    prevBtn?.addEventListener("click", () => {
      index = (index - 1 + total) % total;
      update();
    });

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        index = i;
        update();
      });
    });
  });
});

/* ==========================================================
   CSRF Helper
========================================================== */
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
