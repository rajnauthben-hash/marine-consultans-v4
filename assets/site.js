(() => {
  const showToast = (title, body) => {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    const toast = document.createElement('div');
    toast.className = 'toast rounded-lg';
    toast.innerHTML = `<strong>${title}</strong><span>${body}</span>`;
    document.body.appendChild(toast);
    window.setTimeout(() => toast.remove(), 4200);
  };

  const toggle = document.querySelector('[data-mobile-toggle]');
  const mobileMenu = document.querySelector('[data-mobile-menu]');
  if (toggle && mobileMenu) {
    toggle.addEventListener('click', () => {
      const isHidden = mobileMenu.hasAttribute('hidden');
      if (isHidden) mobileMenu.removeAttribute('hidden');
      else mobileMenu.setAttribute('hidden', '');
      toggle.setAttribute('aria-expanded', String(isHidden));
    });
  }

  document.querySelectorAll('[data-toast-title]').forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      showToast(
        button.getAttribute('data-toast-title') || 'Action captured',
        button.getAttribute('data-toast-body') || 'This placeholder action is ready for real business input.'
      );
    });
  });

  document.querySelectorAll('form[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      showToast(
        form.getAttribute('data-success-title') || 'Form submitted',
        form.getAttribute('data-success-body') || 'This local demo captures the expected submission state without a backend endpoint.'
      );
      form.reset();
    });
  });

  document.querySelectorAll('[data-filter-root]').forEach((root) => {
    const input = root.querySelector('[data-filter-search]');
    const buttons = Array.from(root.querySelectorAll('[data-filter-button]'));
    const items = Array.from(root.querySelectorAll('[data-filter-item]'));
    let activeFilter = 'all';

    const applyFilter = () => {
      const query = (input?.value || '').trim().toLowerCase();
      items.forEach((item) => {
        const text = (item.getAttribute('data-filter-item') || '').toLowerCase();
        const groups = (item.getAttribute('data-filter-groups') || '').toLowerCase().split(',');
        const matchesQuery = !query || text.includes(query);
        const matchesGroup = activeFilter === 'all' || groups.some((group) => group.trim() === activeFilter);
        item.classList.toggle('is-hidden', !(matchesQuery && matchesGroup));
      });
    };

    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        activeFilter = button.getAttribute('data-filter-button') || 'all';
        buttons.forEach((entry) => entry.classList.remove('filter-chip-active'));
        button.classList.add('filter-chip-active');
        applyFilter();
      });
    });

    input?.addEventListener('input', applyFilter);
    applyFilter();
  });
})();
