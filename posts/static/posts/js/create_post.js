/* ============================================================
   ELEMENT REFERENCES
============================================================ */
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
  const words = text.length === 0 ? 0 : text.split(/\s+/).length;
  wordCounter.textContent = `Word count: ${words}`;
});

/* ============================================================
   TOAST POPUP
============================================================ */
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");

  setTimeout(() => {
    t.classList.remove("show");
  }, 1800);
}

/* ============================================================
   OPEN FILE PICKERS
============================================================ */
addImageBtn.onclick = () => imageInput.click();
addVideoBtn.onclick = () => videoInput.click();
addSourceBtn.onclick = () => sourceInput.click();

/* ============================================================
   UPLOAD LIMITS
============================================================ */
const MAX_IMAGES = 5;
const MAX_VIDEOS = 1;
const MAX_DOCS = 5;

/* ============================================================
   IMAGE UPLOAD (with limit)
============================================================ */
imageInput.addEventListener("change", function () {
  const current = thumbnailContainer.children.length;
  const incoming = this.files.length;

  if (current + incoming > MAX_IMAGES) {
    showToast(`You can upload max ${MAX_IMAGES} images.`);
    this.value = "";
    return;
  }

  previewArea.style.display = "block";

  [...this.files].forEach((file) => {
    const reader = new FileReader();

    reader.onload = (e) => {
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
   VIDEO UPLOAD (with limit)
============================================================ */
videoInput.addEventListener("change", function () {
  const already = combinedPreview.querySelectorAll("video").length;

  if (already >= MAX_VIDEOS) {
    showToast("Only 1 video allowed.");
    this.value = "";
    return;
  }

  previewArea.style.display = "block";

  const file = this.files[0];
  if (!file) return;

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

  updateStatus();
});

/* ============================================================
   DOCUMENT UPLOAD (with limit)
============================================================ */
sourceInput.addEventListener("change", function () {
  const current = combinedPreview.querySelectorAll(".doc-card").length;
  const incoming = this.files.length;

  if (current + incoming > MAX_DOCS) {
    showToast(`Max ${MAX_DOCS} documents allowed.`);
    this.value = "";
    return;
  }

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
    const short = base.length > 10 ? base.substring(0, 10) + "…" : base;

    const label = document.createElement("div");
    label.classList.add("doc-label");
    label.textContent = `${short}.${ext}`;

    card.appendChild(wrapper);
    card.appendChild(label);
    combinedPreview.appendChild(card);
  });

  updateStatus();
});

/* ============================================================
   STATUS BAR UPDATE
============================================================ */
function updateStatus() {
  const imgCount = thumbnailContainer.children.length;
  const vidCount = combinedPreview.querySelectorAll("video").length;
  const docCount = combinedPreview.querySelectorAll(".doc-card").length;

  previewStatusBar.textContent = `Images: ${imgCount} | Video: ${vidCount} | Sources: ${docCount}`;
}

/* ============================================================
   CATEGORY LIVE SEARCH  (unchanged)
============================================================ */
const CATEGORY_API = "/categories/search/?q=";

const input = document.getElementById("categoryInput");
const bubbleBox = document.getElementById("categoryBubbleBox");

input.addEventListener("input", async function () {
  const query = this.value.trim();
  bubbleBox.innerHTML = "";

  if (!query) return;

  const res = await fetch(CATEGORY_API + query);
  const data = await res.json();

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

  const existsExact = data.results.some(
    (cat) => cat.toLowerCase() === query.toLowerCase()
  );

  if (!existsExact) {
    const create = document.createElement("div");
    create.classList.add("category-bubble", "category-create");
    create.textContent = `+ Create "${query}"`;
    create.onclick = () => {
      input.value = query;
      bubbleBox.innerHTML = "";
    };
    bubbleBox.appendChild(create);
  }
});
