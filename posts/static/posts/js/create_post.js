/* ============================================================
   ELEMENT REFERENCES
============================================================= */
const addImageBtn = document.getElementById("addImageBtn");
const addVideoBtn = document.getElementById("addVideoBtn");
const addSourceBtn = document.getElementById("addSourceBtn");

const imageInput = document.getElementById("imageInput");
const videoInput = document.getElementById("videoInput");
const sourceInput = document.getElementById("sourceInput");

const previewArea = document.getElementById("previewArea");
const thumbnailContainer = document.getElementById("thumbnailContainer");
const combinedPreview = document.getElementById("combinedPreview");
const previewStatusBar = document.getElementById("previewStatusBar");

/* ============================================================
   WORD COUNT 
============================================================ */
const summaryBox = document.getElementById("summary");
const wordCounter = document.getElementById("wordCount");

summaryBox.addEventListener("input", () => {
  const text = summaryBox.value.trim();

  // Count words by splitting on spaces
  const words = text.length === 0 ? 0 : text.split(/\s+/).length;

  wordCounter.textContent = `Word count: ${words}`;
});

/* ============================================================
   OPEN FILE PICKERS
============================================================= */
addImageBtn.onclick = () => imageInput.click();
addVideoBtn.onclick = () => videoInput.click();
addSourceBtn.onclick = () => sourceInput.click();

/* ============================================================
   IMAGE UPLOAD — THUMBNAIL
============================================================= */
imageInput.addEventListener("change", function () {
  previewArea.style.display = "block";

  [...this.files].forEach((file) => {
    const reader = new FileReader();

    reader.onload = function (e) {
      const thumb = document.createElement("div");
      thumb.classList.add("thumbnail");

      const img = document.createElement("img");
      img.src = e.target.result;

      const removeBtn = document.createElement("button");
      removeBtn.classList.add("remove-btn");
      removeBtn.innerHTML = "×";
      removeBtn.onclick = () => {
        thumb.remove();
        updateStatus();
      };

      thumb.appendChild(img);
      thumb.appendChild(removeBtn);
      thumbnailContainer.appendChild(thumb);
    };

    reader.readAsDataURL(file);
  });

  updateStatus();
});

/* ============================================================
   VIDEO UPLOAD — SMALL THUMBNAIL + REMOVE BUTTON
============================================================= */
videoInput.addEventListener("change", function () {
  previewArea.style.display = "block";

  [...this.files].forEach((file) => {
    const box = document.createElement("div");
    box.classList.add("thumbnail");

    const video = document.createElement("video");
    video.src = URL.createObjectURL(file);
    video.controls = true;
    video.muted = true;

    const removeBtn = document.createElement("button");
    removeBtn.classList.add("remove-btn");
    removeBtn.innerHTML = "×";
    removeBtn.onclick = () => {
      box.remove();
      updateStatus();
    };

    box.appendChild(video);
    box.appendChild(removeBtn);
    combinedPreview.appendChild(box);
  });

  updateStatus();
});

/* ============================================================
   DOCUMENT UPLOAD — ICON + SHORT FILE NAME + REMOVE BTN
============================================================= */
sourceInput.addEventListener("change", function () {
  previewArea.style.display = "block";

  [...this.files].forEach((file) => {
    const card = document.createElement("div");
    card.classList.add("doc-card");

    const wrapper = document.createElement("div");
    wrapper.classList.add("doc-wrapper");

    const icon = document.createElement("div");
    icon.classList.add("doc-preview-icon");
    icon.textContent = "📄";

    const removeBtn = document.createElement("button");
    removeBtn.classList.add("remove-btn");
    removeBtn.innerHTML = "×";
    removeBtn.onclick = () => {
      card.remove();
      updateStatus();
    };

    wrapper.appendChild(icon);
    wrapper.appendChild(removeBtn);

    const ext = file.name.split(".").pop();
    const base = file.name.replace("." + ext, "");
    const shortBase = base.length > 10 ? base.substring(0, 10) + "…" : base;

    const label = document.createElement("div");
    label.classList.add("doc-label");
    label.textContent = `${shortBase}.${ext}`;

    card.appendChild(wrapper);
    card.appendChild(label);
    combinedPreview.appendChild(card);
  });

  updateStatus();
});

/* ============================================================
   STATUS BAR UPDATE
============================================================= */
function updateStatus() {
  const imgCount = thumbnailContainer.children.length;
  const vidCount = combinedPreview.querySelectorAll("video").length;
  const docCount = combinedPreview.querySelectorAll(".doc-wrapper").length;

  previewStatusBar.textContent = `Images: ${imgCount} | Video: ${vidCount} | Sources: ${docCount}`;
}

/* ============================================================
   CATEGORY LIVE SEARCH (FULLY FIXED)
============================================================ */

const CATEGORY_API = "/categories/search/?q=";

const input = document.getElementById("categoryInput");
const bubbleBox = document.getElementById("categoryBubbleBox");

input.addEventListener("input", async function () {
  const query = this.value.trim();
  bubbleBox.innerHTML = "";

  if (query.length === 0) return;

  // Fetch backend categories
  const res = await fetch(CATEGORY_API + query);
  const data = await res.json();
  // data.results = ["Cars", "Car Photos", "Cargo"] etc.

  /* ---------------------------------------------
        Show existing matched category bubbles
    --------------------------------------------- */
  data.results.slice(0, 5).forEach((cat) => {
    const b = document.createElement("div");
    b.classList.add("category-bubble");
    b.textContent = cat;

    b.onclick = () => {
      input.value = cat;
      bubbleBox.innerHTML = "";
    };

    bubbleBox.appendChild(b);
  });

  /* ---------------------------------------------------
         Check if the typed category exists EXACTLY
           (case-insensitive)
    --------------------------------------------------- */
  const existsExact = data.results.some(
    (cat) => cat.toLowerCase().trim() === query.toLowerCase().trim()
  );

  /* ---------------------------------------------------
         Show "+ Create ..." ONLY if category does not exist
    --------------------------------------------------- */
  if (!existsExact) {
    const createBubble = document.createElement("div");
    createBubble.classList.add("category-bubble", "category-create");
    createBubble.textContent = `+ Create "${query}"`;

    createBubble.onclick = () => {
      input.value = query;
      bubbleBox.innerHTML = "";
    };

    bubbleBox.appendChild(createBubble);
  }
});
