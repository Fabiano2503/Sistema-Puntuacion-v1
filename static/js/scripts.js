// static/js/app.js

function showView(viewName) {
  document.querySelectorAll('.view').forEach(view => {
    view.classList.remove('active');
  });

  document.getElementById(viewName).classList.add('active');

  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
  });
  event.target.classList.add('active');
}

function updatePoints() {
  const activityType = document.getElementById('activityType');
  const selectedOption = activityType.options[activityType.selectedIndex];
  const points = selectedOption ? selectedOption.getAttribute('data-points') || 0 : 0;
  document.getElementById('estimatedPoints').textContent = `Puntos: ${points}`;
}

document.addEventListener('DOMContentLoaded', function () {
  if (document.getElementById('activityType')) {
    document.getElementById('activityType').addEventListener('change', updatePoints);
    updatePoints();
  }
});
