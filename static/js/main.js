const button = document.querySelector('.menu-button');
const nav = document.querySelector('#main-nav');
if (button && nav) {
  const label = button.querySelector('.visually-hidden');
  const setOpen = (open) => {
    button.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
    if (label) label.textContent = open ? 'Cerrar menú' : 'Abrir menú';
  };

  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') === 'true';
    setOpen(!open);
  });

  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setOpen(false);
      button.focus();
    }
  });
}

