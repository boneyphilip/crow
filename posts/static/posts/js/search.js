document.addEventListener("DOMContentLoaded", () => {
  const bar = document.getElementById("searchBar");
  const box = document.getElementById("searchResults");

  if (!bar) return;

  bar.addEventListener("input", () => {
    const q = bar.value.trim();

    if (!q) {
      box.innerHTML = "";
      box.style.display = "none";
      return;
    }

    fetch(`/search/ajax/?q=${encodeURIComponent(q)}`)
      .then((r) => r.json())
      .then((data) => {
        const results = data.results;

        if (!results.length) {
          box.innerHTML = "<div class='sr-empty'>No results</div>";
          box.style.display = "block";
          return;
        }

        box.innerHTML = results
          .map(
            (item) => `
                    <div class="sr-item" onclick="location.href='/post/${
                      item.id
                    }/'">
                        <img src="${
                          item.thumb || "/static/posts/images/noimg.png"
                        }">
                        <div>
                            <div class="sr-title">${item.title}</div>
                            <div class="sr-author">@${item.author}</div>
                        </div>
                    </div>
                `
          )
          .join("");

        box.style.display = "block";
      });
  });

  // hide dropdown when clicking outside
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".search-wrapper")) {
      box.style.display = "none";
    }
  });
});
