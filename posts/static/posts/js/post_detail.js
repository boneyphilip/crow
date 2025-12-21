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
   POST DETAIL — AJAX Voting (same response as home)
========================================================== */
  document.body.addEventListener("click", (e) => {
    const btn = e.target.closest(".vote-btn");
    if (!btn) return;

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

        // Update score (prevents blank issue)
        const countEl = document.getElementById(`vote-count-${postId}`);
        if (countEl && data.score !== undefined && data.score !== null) {
          countEl.textContent = data.score;
        }

        // Update active state
        const postCard = btn.closest(".post-card") || document;
        const upBtn = postCard.querySelector(".vote-btn.upvote");
        const downBtn = postCard.querySelector(".vote-btn.downvote");

        if (upBtn) upBtn.classList.remove("active");
        if (downBtn) downBtn.classList.remove("active");

        if (data.user_vote === 1 && upBtn) upBtn.classList.add("active");
        if (data.user_vote === -1 && downBtn) downBtn.classList.add("active");
      })
      .catch((err) => console.error("Vote error:", err));
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

/* ==========================================================
   LIGHTBOX VIEWER
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

  /* Open Lightbox */
  function openLightbox(i) {
    index = i;
    const item = mediaList[index];

    if (item.type === "image") {
      vidBox.classList.add("hidden");
      imgBox.classList.remove("hidden");
      imgBox.src = item.src;
    } else if (item.type === "video") {
      imgBox.classList.add("hidden");
      vidBox.classList.remove("hidden");
      vidBox.src = item.src;
    }

    lightbox.classList.remove("hidden");
  }

  /* Close */
  function closeLightbox() {
    lightbox.classList.add("hidden");
    vidBox.pause();
  }

  /* Navigation */
  function next() {
    index = (index + 1) % mediaList.length;
    openLightbox(index);
  }

  function prev() {
    index = (index - 1 + mediaList.length) % mediaList.length;
    openLightbox(index);
  }

  /* Bind events */
  closeBtn.addEventListener("click", closeLightbox);
  nextBtn.addEventListener("click", next);
  prevBtn.addEventListener("click", prev);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") next();
    if (e.key === "ArrowLeft") prev();
  });

  /* Attach click events to all media */
  document
    .querySelectorAll(
      ".media-single-img, .media-single-video, .gallery-item img, .gallery-item video"
    )
    .forEach((el, i, arr) => {
      // Build media array
      mediaList = Array.from(arr).map((m) => ({
        src: m.tagName === "IMG" ? m.src : m.querySelector("source")?.src,
        type: m.tagName === "IMG" ? "image" : "video",
      }));

      el.addEventListener("click", () => openLightbox(i));
    });
});

/* ==========================================================
   SHARE BUTTON (COPY LINK / NATIVE SHARE)
========================================================== */
document.body.addEventListener("click", async (e) => {
  const shareBtn = e.target.closest(".share-btn");
  if (!shareBtn) return;

  const postCard = shareBtn.closest(".post-card");
  if (!postCard) return;

  const postId = postCard.dataset.postId;
  const postUrl = `${window.location.origin}/post/${postId}/`;

  try {
    if (navigator.share) {
      await navigator.share({ title: "Crow Post", url: postUrl });
      return;
    }

    // Clipboard fallback (works on localhost usually)
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(postUrl);
      alert("Link copied to clipboard!");
      return;
    }

    // Old fallback
    const temp = document.createElement("textarea");
    temp.value = postUrl;
    document.body.appendChild(temp);
    temp.select();
    document.execCommand("copy");
    document.body.removeChild(temp);
    alert("Link copied to clipboard!");
  } catch (err) {
    console.warn("Share failed:", err);
  }
});
