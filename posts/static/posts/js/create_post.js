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
   OPEN FILE PICKERS
============================================================ */
addImageBtn.onclick = () => imageInput.click();
addVideoBtn.onclick = () => videoInput.click();
addSourceBtn.onclick = () => sourceInput.click();

/* ============================================================
   IMAGE UPLOAD — THUMBNAIL
============================================================ */
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
============================================================ */
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
============================================================ */
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

    // ---- Filename shortening with extension ----
    const ext = file.name.split(".").pop();
    const baseName = file.name.replace("." + ext, "");

    const shortName =
      baseName.length > 10 ? baseName.substring(0, 10) + "…" : baseName;

    const label = document.createElement("div");
    label.classList.add("doc-label");
    label.textContent = `${shortName}.${ext}`;

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
  const docCount = combinedPreview.querySelectorAll(".doc-wrapper").length;

  previewStatusBar.textContent = `Images: ${imgCount} | Video: ${vidCount} | Sources: ${docCount}`;
}
