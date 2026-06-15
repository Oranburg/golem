// Theme toggle (matching equally-poor: sun/moon SVG icons in nav)
function toggleTheme() {
  var current = document.documentElement.getAttribute('data-theme');
  var next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateToggleLabel(next);
}

function updateToggleLabel(theme) {
  var btns = document.querySelectorAll('.theme-toggle');
  btns.forEach(function (btn) {
    btn.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode');
  });
}

// Initialize toggle label on load
(function () {
  var theme = document.documentElement.getAttribute('data-theme') || 'dark';
  updateToggleLabel(theme);
})();

// Highlight the current nav link based on the page path
(function () {
  var path = window.location.pathname;
  var links = document.querySelectorAll('.site-nav a');
  links.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href === '/' ? path === '/' : path.indexOf(href) === 0) {
      link.setAttribute('aria-current', 'page');
    }
  });
})();

// Article abstract expand/collapse
function toggleAbstract(element, ev) {
  var e = ev || window.event;
  if (e && e.target && e.target.tagName === 'A') return;
  element.classList.toggle('expanded');
  var indicator = element.querySelector('.expand-indicator');
  if (indicator) {
    indicator.textContent = element.classList.contains('expanded') ? '\u2212' : '+';
  }
}

function handleArticleKey(event, element) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    toggleAbstract(element);
  }
}
