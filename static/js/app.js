document.addEventListener('DOMContentLoaded', () => {
  const csrfToken = () => {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  };

  document.querySelectorAll('[data-autosave-form]').forEach((form) => {
    const statusTarget = document.querySelector(form.dataset.statusTarget);
    let timeoutId;

    const save = () => {
      const formData = new FormData(form);
      if (statusTarget) {
        statusTarget.textContent = 'Saving...';
      }
      fetch(form.action, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken() },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (statusTarget) {
            statusTarget.textContent = data.ok ? 'Saved.' : 'Save failed.';
          }
        })
        .catch(() => {
          if (statusTarget) {
            statusTarget.textContent = 'Save failed.';
          }
        });
    };

    form.addEventListener('input', () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(save, 600);
    });
    form.addEventListener('change', save);
  });
});
