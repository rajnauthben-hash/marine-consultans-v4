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
        button.getAttribute('data-toast-title') || 'Action ready',
        button.getAttribute('data-toast-body') || 'This action is ready for the final business content or document link.'
      );
    });
  });

  const humanizeField = (value) =>
    value
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (match) => match.toUpperCase());

  document.querySelectorAll('form[data-email-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const to = form.getAttribute('data-email-to') || '';
      const subject = form.getAttribute('data-email-subject') || 'Marine Consultants website inquiry';
      const entries = Array.from(new FormData(form).entries()).map(([key, value]) => `${humanizeField(key)}: ${String(value || '').trim() || 'N/A'}`);
      const body = [
        'Inquiry prepared from the Marine Consultants website.',
        '',
        ...entries,
        '',
        `Page: ${window.location.href}`,
      ].join('\n');
      showToast(
        form.getAttribute('data-success-title') || 'Form submitted',
        form.getAttribute('data-success-body') || 'Your email client should open with a prepared inquiry draft.'
      );
      if (to) {
        const mailto = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        window.setTimeout(() => {
          window.location.href = mailto;
        }, 120);
      }
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
