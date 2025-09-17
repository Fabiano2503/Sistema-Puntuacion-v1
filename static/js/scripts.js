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
  // Para showView y updatePoints
  if (document.getElementById('activityType')) {
    document.getElementById('activityType').addEventListener('change', updatePoints);
    updatePoints();
  }

  // Control de dropdown del perfil
  const avatarToggle = document.getElementById("avatarToggle");
  const profileDropdown = document.getElementById("profileDropdown");

  if (avatarToggle && profileDropdown) {
    avatarToggle.addEventListener("click", () => {
      profileDropdown.classList.toggle("hidden");
    });

    document.addEventListener("click", (event) => {
      if (!avatarToggle.contains(event.target) && !profileDropdown.contains(event.target)) {
        profileDropdown.classList.add("hidden");
      }
    });
  }

  // Subida de imagen con preview y confirmación
  const imageInput = document.getElementById("profileImageInput");
  const imageForm = document.getElementById("profileImageForm");
  const confirmButtonContainer = document.getElementById("confirmButtonContainer");
  const confirmUploadBtn = document.getElementById("confirmUploadBtn");

  let selectedFile = null;

  if (imageInput && imageForm && confirmButtonContainer && confirmUploadBtn) {
    imageInput.addEventListener("change", function () {
      if (imageInput.files && imageInput.files[0]) {
        selectedFile = imageInput.files[0];

        // Mostrar preview local
        const reader = new FileReader();
        reader.onload = function (e) {
          document.querySelectorAll(".avatar").forEach(img => {
            img.src = e.target.result;
          });
          // Mostrar botón para confirmar
          confirmButtonContainer.style.display = "block";
        };
        reader.readAsDataURL(selectedFile);
      }
    });

    confirmUploadBtn.addEventListener("click", function () {
      if (!selectedFile) return alert("No hay imagen seleccionada");

      const formData = new FormData();
      formData.append('image_url', selectedFile);

      fetch(imageForm.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (data.success && data.image_url) {
            document.querySelectorAll(".avatar").forEach(img => {
              img.src = data.image_url + "?v=" + new Date().getTime();
            });
            // Ocultar botón confirm después de subir
            confirmButtonContainer.style.display = "none";
            // Limpiar selección
            imageInput.value = "";
            selectedFile = null;
          } else {
            alert("Error al subir la imagen");
            console.error(data.errors);
          }
        })
        .catch(err => {
          console.error("Error al enviar la imagen", err);
        });
    });
  }
});
