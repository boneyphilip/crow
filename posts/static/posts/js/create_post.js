/* =============================================================
   CREATE POST PAGE — JAVASCRIPT
=============================================================== */

document.addEventListener("DOMContentLoaded", function () {
  const LOG = "[CREATE_POST]";

  console.group(LOG + " Init");
  console.log("JS Loaded successfully.");
  console.groupEnd();

  /* -------------------------------
     WORD COUNTER
  --------------------------------*/
  const summary = document.getElementById("summary");
  const countBox = document.getElementById("wordCount");

  if (summary) {
    summary.addEventListener("input", () => {
      const words = summary.value.trim().split(/\s+/).filter(Boolean).length;
      countBox.textContent = "Word count: " + words;
    });
  }

  /* -------------------------------
     PREVIEW SYSTEM
  --------------------------------*/
  let imgCount = 0,
    vidCount = 0,
    srcCount = 0;

  const previewArea = document.getElementById("previewArea");
  const previewStatus = document.getElementById("previewStatusBar");
  const imageInput = document.getElementById("imageInput");
  const videoInput = document.getElementById("videoInput");
  const sourceInput = document.getElementById("sourceInput");
  const thumbnailContainer = document.getElementById("thumbnailContainer");
  const combinedPreview = document.getElementById("combinedPreview");

  function showPreviewBox() {
    previewArea.style.display = "block";
  }

  function updateStatus() {
    previewStatus.textContent = `Images: ${imgCount} | Video: ${vidCount} | Sources: ${srcCount}`;
  }

  function hideIfNoFiles() {
    if (imgCount === 0 && vidCount === 0 && srcCount === 0) {
      previewArea.style.display = "none";
    }
  }

  /* -------------------------------
     ADD IMAGES
  --------------------------------*/
  const addImgBtn = document.getElementById("addImageBtn");
  if (addImgBtn && imageInput) {
    addImgBtn.onclick = () => imageInput.click();

    imageInput.addEventListener("change", () => {
      if (!imageInput.files.length) return;

      showPreviewBox();

      Array.from(imageInput.files).forEach((file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const box = document.createElement("div");
          box.className = "thumbnail";

          box.innerHTML = `
              <img src="${e.target.result}">
              <div class="thumb-number">${imgCount + 1}</div>
              <button class="remove-btn">&times;</button>
          `;

          thumbnailContainer.appendChild(box);
          imgCount++;
          updateStatus();

          box.querySelector(".remove-btn").onclick = () => {
            box.remove();
            imgCount--;
            renumberImages();
            updateStatus();
            hideIfNoFiles();
          };
        };
        reader.readAsDataURL(file);
      });
    });
  }

  function renumberImages() {
    document.querySelectorAll(".thumb-number").forEach((n, i) => {
      n.textContent = i + 1;
    });
  }

  /* -------------------------------
     ADD VIDEO
  --------------------------------*/
  const addVideo = document.getElementById("addVideoBtn");
  if (addVideo && videoInput) {
    addVideo.onclick = () => videoInput.click();

    videoInput.addEventListener("change", () => {
      if (!videoInput.files.length) return;

      if (vidCount >= 1) {
        alert("Only 1 video allowed.");

        return;
      }

      showPreviewBox();

      const file = videoInput.files[0];

      const row = document.createElement("div");
      row.className = "row-item";

      row.innerHTML = `
        <svg class="row-icon" viewBox="0 0 24 24">
          <path d="M17 10.5V7a2 2 0 0 0-2-2H5A2 2 0 0 0 3 7v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3.5l4 4v-11l-4 4z"/>
        </svg>
        <span class="row-filename">${file.name}</span>
        <button class="remove-row-btn">&times;</button>
      `;

      combinedPreview.appendChild(row);
      vidCount = 1;
      updateStatus();

      row.querySelector(".remove-row-btn").onclick = () => {
        row.remove();
        vidCount = 0;
        updateStatus();
        hideIfNoFiles();
      };
    });
  }

  /* -------------------------------
     ADD SOURCE FILES
  --------------------------------*/
  const addSource = document.getElementById("addSourceBtn");
  if (addSource && sourceInput) {
    addSource.onclick = () => sourceInput.click();

    sourceInput.addEventListener("change", () => {
      if (!sourceInput.files.length) return;

      showPreviewBox();

      Array.from(sourceInput.files).forEach((file) => {
        const row = document.createElement("div");
        row.className = "row-item";

        row.innerHTML = `
          <svg class="row-icon" viewBox="0 0 24 24">
            <path d="M6 2h9l5 5v15a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"/>
          </svg>
          <span class="row-filename">${file.name}</span>
          <button class="remove-row-btn">&times;</button>
        `;

        combinedPreview.appendChild(row);
        srcCount++;
        updateStatus();

        row.querySelector(".remove-row-btn").onclick = () => {
          row.remove();
          srcCount--;
          updateStatus();
          hideIfNoFiles();
        };
      });
    });
  }

  /* -------------------------------
     CATEGORY AUTO-SUGGEST
  --------------------------------*/
  const catInput = document.getElementById("categoryInput");
  const suggestionBox = document.getElementById("categorySuggestions");

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

  if (catInput) {
    catInput.addEventListener("keyup", () => {
      const query = catInput.value.trim();

      if (!query) {
        suggestionBox.classList.remove("show");
        suggestionBox.innerHTML = "";
        return;
      }

      fetch(`/categories/search/?q=${encodeURIComponent(query)}`)
        .then((res) => res.json())
        .then((data) => {
          const results = data.results;
          const exists = data.exists;
          const typed = data.typed;

          let html = "";

          results.forEach((item) => {
            html += `<div class="suggestion-item">${item}</div>`;
          });

          if (!exists) {
            html += `<div class="suggestion-create">➕ Create "${typed}"</div>`;
          }

          suggestionBox.innerHTML = html;
          suggestionBox.classList.add("show");

          document.querySelectorAll(".suggestion-item").forEach((item) => {
            item.onclick = () => {
              catInput.value = item.textContent;
              suggestionBox.classList.remove("show");
            };
          });

          const createBtn = document.querySelector(".suggestion-create");
          if (createBtn) {
            createBtn.onclick = () => {
              fetch("/categories/create/", {
                method: "POST",
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                  "X-CSRFToken": getCookie("csrftoken"),
                },
                body: `name=${encodeURIComponent(typed)}`,
              })
                .then((r) => r.json())
                .then((d) => {
                  catInput.value = d.name;
                  suggestionBox.classList.remove("show");
                });
            };
          }
        });
    });
  }

  document.addEventListener("click", (e) => {
    if (
      !e.target.closest("#categoryInput") &&
      !e.target.closest("#categorySuggestions")
    ) {
      suggestionBox.classList.remove("show");
    }
  });
});
