
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("cloud-tab-search").addEventListener("input", filterTabLinks)
}, false);

function filterTabLinks(event) {
  let s = event.target.value;
  document.querySelectorAll(".cloud-tab a").forEach(el => {
    el.parentElement.classList.toggle("hidden", !(el.href.includes(s) || el.textContent.includes(s)))
  });
}