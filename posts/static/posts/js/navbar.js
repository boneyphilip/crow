document.addEventListener("DOMContentLoaded", () => {
  const profileBtn = document.querySelector(".profile-btn");
  const menu = document.querySelector(".profile-menu");

  profileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    menu.classList.toggle("hidden");
  });

  // Close dropdown when clicked outside
  document.addEventListener("click", () => {
    menu.classList.add("hidden");
  });
});
