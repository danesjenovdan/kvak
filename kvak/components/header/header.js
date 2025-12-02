document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.querySelector(".header-component .nav-toggle");
  const navMenu = document.querySelector(".header-component .nav-menu");

  navToggle.addEventListener("click", function () {
    navMenu.classList.toggle("open");
  });
});
