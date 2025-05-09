document.addEventListener("DOMContentLoaded", () => {
  // Sidebar toggle for mobile
  const burgerBtn = document.getElementById("burgerBtn");
  const sidebar = document.getElementById("sidebar");
  const categoryText = document.getElementById("categoryText");
  const categoryList = document.getElementById("categoryList");

  if (burgerBtn && sidebar) {
    burgerBtn.addEventListener("click", () => {
      sidebar.classList.toggle("hidden");
    });
  }

  if (categoryText && categoryList) {
    categoryText.addEventListener("click", (e) => {
      e.stopPropagation();
      const isBurgerHidden = window.getComputedStyle(burgerBtn).display === "none";
      if (isBurgerHidden) {
        categoryList.classList.toggle("hidden");
      }
    });

    document.addEventListener("click", (e) => {
      if (!e.target.closest(".category-dropdown")) {
        categoryList.classList.add("hidden");
      }
    });
  }

  // Add to cart button alert
  document.querySelectorAll(".add-btn").forEach(button => {
    button.addEventListener("click", () => {
      alert("Added to cart!");
      // You can add real cart logic here
    });
  });

  // Newsletter form submission
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
      e.preventDefault();
      alert('Thank you for subscribing!');
    });
  }
});
