/* ==========================================================
   HOME PAGE — AJAX Voting + Reddit-Style Media Slider
========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[HOME] Voting + Gallery JS Loaded");

  /* ==========================================================
     VOTING LOGIC
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
     REDDIT STYLE SLIDER (Images + Videos + Documents)
  ========================================================== */
  document.querySelectorAll(".media-gallery").forEach((gallery) => {
    const track = gallery.querySelector(".gallery-track");
    const slides = gallery.querySelectorAll(".gallery-item");
    const dots = gallery.querySelectorAll(".gallery-dots span");

    const prevBtn = gallery.querySelector(".gallery-prev");
    const nextBtn = gallery.querySelector(".gallery-next");

    let currentIndex = 0;
    const totalSlides = slides.length;
    let sliding = false;

    /* Disable arrows if only 1 slide */
    if (totalSlides <= 1) {
      prevBtn.style.display = "none";
      nextBtn.style.display = "none";
      dots.forEach((d) => (d.style.display = "none"));
      return;
    }

    /* Update slider UI */
    function updateSlider() {
      track.style.transform = `translateX(-${currentIndex * 100}%)`;

      dots.forEach((dot, i) =>
        dot.classList.toggle("active", i === currentIndex)
      );
    }

    /* Prevent spam-clicking */
    function safeSlide(callback) {
      if (sliding) return;
      sliding = true;
      callback();
      setTimeout(() => (sliding = false), 300);
    }

    /* Next */
    nextBtn.addEventListener("click", () => {
      safeSlide(() => {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlider();
      });
    });

    /* Previous */
    prevBtn.addEventListener("click", () => {
      safeSlide(() => {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlider();
      });
    });

    /* Dot navigation */
    dots.forEach((dot, i) =>
      dot.addEventListener("click", () => {
        currentIndex = i;
        updateSlider();
      })
    );

    /* ==========================================================
       SWIPE SUPPORT (Mobile friendly)
    ========================================================== */
    let startX = 0;
    let isDragging = false;

    gallery.addEventListener("touchstart", (e) => {
      startX = e.touches[0].clientX;
      isDragging = true;
    });

    gallery.addEventListener("touchmove", (e) => {
      if (!isDragging) return;

      const diff = e.touches[0].clientX - startX;

      if (Math.abs(diff) > 60) {
        isDragging = false;
        if (diff < 0) nextBtn.click();
        else prevBtn.click();
      }
    });

    gallery.addEventListener("touchend", () => {
      isDragging = false;
    });

    /* Call once on load */
    updateSlider();
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

/* ==========================================================
   LIGHTBOX — Only load media from clicked post 
========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  const lightbox = document.getElementById("lightbox");
  const imgBox = document.getElementById("lightbox-img");
  const vidBox = document.getElementById("lightbox-video");
  const closeBtn = document.getElementById("lightbox-close");
  const prevBtn = document.getElementById("lightbox-prev");
  const nextBtn = document.getElementById("lightbox-next");

  let mediaList = [];
  let index = 0;

  function openLightbox(i) {
    index = i;
    const item = mediaList[index];

    imgBox.classList.remove("active");
    vidBox.classList.remove("active");

    if (item.type === "image") {
      imgBox.src = item.src;
      imgBox.classList.add("active");
    } else {
      vidBox.src = item.src;
      vidBox.classList.add("active");
    }

    lightbox.classList.remove("hidden");
  }

  function closeLightbox() {
    lightbox.classList.add("hidden");
    vidBox.pause();
  }

  function next() {
    index = (index + 1) % mediaList.length;
    openLightbox(index);
  }

  function prev() {
    index = (index - 1 + mediaList.length) % mediaList.length;
    openLightbox(index);
  }

  closeBtn.addEventListener("click", closeLightbox);
  nextBtn.addEventListener("click", next);
  prevBtn.addEventListener("click", prev);

  /* -------------------------------
     CLICK HANDLING
  -------------------------------- */
  document.querySelectorAll(".media-gallery").forEach((gallery) => {
    const postId = gallery.dataset.postId;

    const mediaElements = gallery.querySelectorAll("img, video");

    gallery.querySelectorAll("img, video").forEach((el, i) => {
      el.style.cursor = "pointer";

      el.addEventListener("click", () => {
        // Rebuild correct mediaList only for this post
        mediaList = Array.from(mediaElements).map((m) => ({
          src: m.tagName === "IMG" ? m.src : m.querySelector("source").src,
          type: m.tagName === "IMG" ? "image" : "video",
        }));

        openLightbox(i);
      });
    });
  });
});
