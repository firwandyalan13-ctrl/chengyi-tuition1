document.querySelectorAll('[data-en]').forEach((el) => {
  if (!el.dataset.zh) el.dataset.zh = el.innerHTML;
});

function setLang(l) {
  document.querySelectorAll('[data-zh]').forEach((el) => {
    el.innerHTML = el.dataset[l] || el.dataset.zh;
  });
  document.querySelectorAll('.lang button').forEach((b) => {
    b.classList.toggle('on', b.dataset.l === l);
  });
  document.documentElement.lang = l === 'zh' ? 'zh-CN' : l;
}

document.querySelectorAll('.lang button').forEach((b) => {
  b.addEventListener('click', () => setLang(b.dataset.l));
});

const bookForm = document.getElementById('bookForm');
if (bookForm) {
  bookForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(bookForm);
    const msg = `您好！我想预约试听。\n学生姓名：${d.get('name')}\n电话：${d.get('phone')}\n年级：${d.get('grade') || '-'}\n内容：${d.get('msg') || '-'}`;
    window.open(`https://wa.me/${d.get('branch')}?text=${encodeURIComponent(msg)}`, '_blank');
  });
}

const navToggle = document.querySelector('.nav-toggle');
const mobileNav = document.getElementById('mobile-nav');

function closeMobileNav() {
  if (!mobileNav || !navToggle) return;
  mobileNav.hidden = true;
  navToggle.setAttribute('aria-expanded', 'false');
  navToggle.setAttribute('aria-label', '打开菜单');
}

function openMobileNav() {
  if (!mobileNav || !navToggle) return;
  mobileNav.hidden = false;
  navToggle.setAttribute('aria-expanded', 'true');
  navToggle.setAttribute('aria-label', '关闭菜单');
  const firstLink = mobileNav.querySelector('a');
  if (firstLink) firstLink.focus();
}

if (navToggle && mobileNav) {
  navToggle.addEventListener('click', () => {
    if (mobileNav.hidden) openMobileNav();
    else closeMobileNav();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !mobileNav.hidden) {
      closeMobileNav();
      navToggle.focus();
    }
  });
  mobileNav.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', closeMobileNav);
  });
}
