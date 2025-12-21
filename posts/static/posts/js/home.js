/* ==========================================================
   HOME PAGE — Voting + Gallery + Unified Lightbox
   FINAL, STABLE & SUBMISSION-READY
========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[HOME] Loaded");

  /* ==========================================================
     CSRF HELPER
  ========================================================== */
  function getCookie(name) {
    let value = null;
    document.cookie.split(";").forEach((c) => {
      c = c.trim();
      if (c.startsWith(name + "=")) {
        value = c.substring(name.length + 1);
      }
    });
    return value;
  }

  /* ==========================================================
     VOTING SYSTEM (AJAX)
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
        if (data.success) {
          const count = document.getElementById(`vote-count-${postId}`);
          if (count) count.textContent = data.score;

          // Find buttons inside the same post card
          const postCard = btn.closest(".post-card");
          if (!postCard) return;

          const upBtn = postCard.querySelector(".vote-btn.upvote");
          const downBtn = postCard.querySelector(".vote-btn.downvote");

          if (!upBtn || !downBtn) return;

          // Reset UI state
          upBtn.classList.remove("active");
          downBtn.classList.remove("active");

          // Apply correct active state from server response
          // data.user_vote: 1 = upvote, -1 = downvote, 0 = no vote
          if (data.user_vote === 1) {
            upBtn.classList.add("active");
          } else if (data.user_vote === -1) {
            downBtn.classList.add("active");
          }
        }
      })
      .catch(() => console.warn("Vote request failed"));
  });

  /* ==========================================================
     REDDIT-STYLE GALLERY SLIDER (INLINE VIEW)
  ========================================================== */
  document.querySelectorAll(".media-gallery").forEach((gallery) => {
    const track = gallery.querySelector(".gallery-track");
    const slides = gallery.querySelectorAll(".gallery-item");
    const dots = gallery.querySelectorAll(".gallery-dots span");
    const prev = gallery.querySelector(".gallery-prev");
    const next = gallery.querySelector(".gallery-next");

    let index = 0;
    const total = slides.length;

    function update() {
      track.style.transform = `translateX(-${index * 100}%)`;
      dots.forEach((d, i) => d.classList.toggle("active", i === index));
    }

    next?.addEventListener("click", (e) => {
      e.stopPropagation();
      index = (index + 1) % total;
      update();
    });

    prev?.addEventListener("click", (e) => {
      e.stopPropagation();
      index = (index - 1 + total) % total;
      update();
    });

    dots.forEach((dot, i) => {
      dot.addEventListener("click", (e) => {
        e.stopPropagation();
        index = i;
        update();
      });
    });

    update();
  });

  /* ==========================================================
     LIGHTBOX ELEMENTS
  ========================================================== */
  const lightbox = document.getElementById("lightbox");
  const imgBox = document.getElementById("lightbox-img");
  const vidBox = document.getElementById("lightbox-video");
  const docBox = document.getElementById("lightbox-doc");
  const docName = document.getElementById("doc-name");
  const docDownload = document.getElementById("doc-download");
  const closeBtn = document.getElementById("lightbox-close");
  const prevBtn = document.getElementById("lightbox-prev");
  const nextBtn = document.getElementById("lightbox-next");

  let mediaList = [];
  let currentIndex = 0;

  /* ==========================================================
     LIGHTBOX HELPERS
  ========================================================== */
  function resetLightbox() {
    imgBox.classList.remove("active");
    vidBox.classList.remove("active");
    docBox.classList.add("hidden");

    imgBox.src = "";
    vidBox.pause();
    vidBox.src = "";
  }

  function openLightbox(index) {
    if (!mediaList.length) return;

    currentIndex = index;
    const item = mediaList[currentIndex];
    resetLightbox();

    if (item.type === "image") {
      imgBox.src = item.src;
      imgBox.classList.add("active");
    }

    if (item.type === "video") {
      vidBox.src = item.src;
      vidBox.classList.add("active");
      vidBox.load();
    }

    if (item.type === "doc") {
      docName.textContent = item.name || "Document";
      docDownload.href = item.src;
      docBox.classList.remove("hidden");
    }

    lightbox.classList.remove("hidden");
  }

  function closeLightbox() {
    resetLightbox();
    lightbox.classList.add("hidden");
    mediaList = [];
    currentIndex = 0;
  }

  function showNext() {
    openLightbox((currentIndex + 1) % mediaList.length);
  }

  function showPrev() {
    openLightbox((currentIndex - 1 + mediaList.length) % mediaList.length);
  }

  /* ==========================================================
     LIGHTBOX CONTROLS
  ========================================================== */
  closeBtn?.addEventListener("click", closeLightbox);
  nextBtn?.addEventListener("click", showNext);
  prevBtn?.addEventListener("click", showPrev);

  // Close when clicking outside content
  lightbox?.addEventListener("click", (e) => {
    if (e.target === lightbox) closeLightbox();
  });

  // Keyboard controls
  document.addEventListener("keydown", (e) => {
    if (lightbox.classList.contains("hidden")) return;

    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") showNext();
    if (e.key === "ArrowLeft") showPrev();
  });

  /* ==========================================================
     MEDIA CLICK HANDLER (EVENT DELEGATION)
     - Single image / video / document
     - Gallery image / video / document
     - Scoped to the clicked post only
  ========================================================== */
  document.addEventListener("click", (e) => {
    const mediaEl = e.target.closest(
      ".media-single-img, .media-single-video, .doc-attachment, .gallery-item img, .gallery-item video, .doc-slide"
    );
    if (!mediaEl) return;

    e.preventDefault();
    e.stopPropagation();

    const postCard = mediaEl.closest(".post-card");
    if (!postCard) return;

    const elements = postCard.querySelectorAll(
      ".media-single-img, .media-single-video, .doc-attachment, .gallery-item img, .gallery-item video, .doc-slide"
    );

    mediaList = Array.from(elements).map((el) => {
      if (el.tagName === "IMG") {
        return { type: "image", src: el.src };
      }
      if (el.tagName === "VIDEO") {
        return {
          type: "video",
          src: el.querySelector("source").src,
        };
      }
      return {
        type: "doc",
        src: el.dataset.src,
        name: el.dataset.name,
      };
    });

    const index = Array.from(elements).indexOf(mediaEl);
    openLightbox(index);
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
      // Mobile / supported browsers
      if (navigator.share) {
        await navigator.share({
          title: "Check this post on Crow",
          url: postUrl,
        });
      } else {
        // Desktop fallback
        await navigator.clipboard.writeText(postUrl);
        alert("Link copied to clipboard!");
      }
    } catch (err) {
      console.warn("Share cancelled or failed", err);
    }
  });
});
