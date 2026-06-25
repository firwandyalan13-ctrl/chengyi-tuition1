/**
 * 诚意补习学院 — 共用脚本
 * 各页按需初始化，所有 DOM 查询均做 null 防呆
 */
(function () {
  'use strict';

  function $(id) {
    return document.getElementById(id);
  }

  /* ── Navbar 滚动效果 ── */
  const navbar = $('navbar');
  if (navbar) {
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
      const currentScroll = window.scrollY;
      if (currentScroll > lastScroll && currentScroll > 200) {
        navbar.style.transform = 'translateY(-100%)';
      } else {
        navbar.style.transform = 'translateY(0)';
      }
      lastScroll = currentScroll;
    }, { passive: true });
  }

  /* ── Back to Top ── */
  const backToTop = $('back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      backToTop.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── 汉堡选单 ── */
  const hamburger = $('hamburger');
  const mobileMenu = $('mobile-menu');
  const hamIcon = $('ham-icon');

  window.closeMobile = function () {
    if (!mobileMenu || !hamIcon) return;
    mobileMenu.classList.remove('open');
    hamIcon.className = 'fa-solid fa-bars';
    document.body.style.overflow = '';
  };

  if (hamburger && mobileMenu && hamIcon) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      hamIcon.className = mobileMenu.classList.contains('open')
        ? 'fa-solid fa-xmark'
        : 'fa-solid fa-bars';
      document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
    });
  }

  /* ── Scroll fade-up ── */
  const fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('visible');
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    fadeEls.forEach(el => observer.observe(el));
  }

  /* ── 数字计数动画（仅 about 页） ── */
  const counters = document.querySelectorAll('.counter');
  if (counters.length) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting || entry.target.dataset.counted) return;
        entry.target.dataset.counted = 'true';
        const target = parseFloat(entry.target.dataset.target);
        const isFloat = target % 1 !== 0;
        const duration = 1500;
        const startTime = performance.now();

        function animate(currentTime) {
          const progress = Math.min((currentTime - startTime) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const current = target * eased;
          entry.target.textContent = isFloat ? current.toFixed(1) : Math.floor(current);
          if (progress < 1) requestAnimationFrame(animate);
          else entry.target.textContent = isFloat ? target.toFixed(1) : target;
        }
        requestAnimationFrame(animate);
      });
    }, { threshold: 0.5 });
    counters.forEach(el => counterObserver.observe(el));
  }

  /* ── 分校 WhatsApp Modal ── */
  window.showBranchModal = function () {
    const modal = $('branch-modal');
    if (!modal) return;
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  window.closeBranchModal = function () {
    const modal = $('branch-modal');
    if (!modal) return;
    modal.classList.remove('open');
    document.body.style.overflow = '';
  };

  const branchModal = $('branch-modal');
  if (branchModal) {
    branchModal.addEventListener('click', function (e) {
      if (e.target === this) closeBranchModal();
    });
  }

  /* ── 联系表单 → WhatsApp（依所选分校，仅 contact 页） ── */
  const BRANCH_WA = {
    mentakab: '60177717900',
    setapak: '60173663800',
    wangsa: '60122467900',
  };

  window.handleSubmit = function (e) {
    e.preventDefault();
    const form = $('contact-form');
    const success = $('form-success');
    if (!form) return;

    const branch = $('contact-branch')?.value || 'wangsa';
    const wa = BRANCH_WA[branch] || BRANCH_WA.wangsa;
    const name = $('contact-name')?.value || '';
    const phone = $('contact-phone')?.value || '';
    const grade = $('contact-grade')?.value || '';
    const msg = $('contact-message')?.value || '';
    const gradeLine = grade ? `\n年级：${grade}` : '';
    const text = encodeURIComponent(
      `您好！我来自诚意补习学院官网。\n分校：${branch}\n姓名：${name}\n电话：${phone}${gradeLine}\n咨询内容：${msg}`
    );
    window.open(`https://wa.me/${wa}?text=${text}`, '_blank');
    form.reset();
    if (success) {
      success.classList.remove('hidden');
      setTimeout(() => success.classList.add('hidden'), 5000);
    }
  };

  /* ── 当前页高亮 nav-link ── */
  const PAGE_NAV_MAP = {
    'index.html': 'home',
    '': 'home',
    'about.html': 'about',
    'courses.html': 'courses',
    'contact.html': 'contact',
  };
  const currentFile = window.location.pathname.split('/').pop() || 'index.html';
  const activeNav = PAGE_NAV_MAP[currentFile] || '';
  document.querySelectorAll('.nav-link[data-nav]').forEach(link => {
    link.classList.toggle('active-link', link.dataset.nav === activeNav);
  });

  /* ── 三语切换 + localStorage 记忆 ── */
  let currentLang = 'zh';
  const langMap = { zh: 'zh-Hans', ms: 'ms', en: 'en' };

  function applyLanguage(lang) {
    currentLang = lang;
    document.querySelectorAll('.lang-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.lang === lang);
    });
    document.querySelectorAll('.tr').forEach(el => {
      const text = el.getAttribute('data-' + lang);
      if (text) el.textContent = text;
    });
    document.documentElement.lang = langMap[lang] || lang;
    localStorage.setItem('chengyi-lang', lang);
  }

  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;
      if (lang && lang !== currentLang) applyLanguage(lang);
    });
  });

  const savedLang = localStorage.getItem('chengyi-lang');
  if (savedLang) applyLanguage(savedLang);

  /* ── 动态年份 ── */
  const yearEl = $('current-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ── 图片 lazy-load 错误处理 ── */
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    img.addEventListener('error', () => {
      img.alt = '图片加载失败';
      img.style.opacity = '0.3';
    });
  });

  /* ── 课程手风琴（仅 courses 页） ── */
  window.toggleCourse = function (btn) {
    if (!btn) return;
    const accordion = btn.closest('.course-accordion');
    if (!accordion) return;
    const body = accordion.querySelector('.course-accordion-body');
    if (!body) return;

    const isOpen = accordion.classList.contains('active');

    document.querySelectorAll('.course-accordion.active').forEach(other => {
      if (other !== accordion) {
        other.classList.remove('active');
        const otherBody = other.querySelector('.course-accordion-body');
        if (otherBody) otherBody.style.maxHeight = '0';
      }
    });

    if (isOpen) {
      accordion.classList.remove('active');
      body.style.maxHeight = '0';
    } else {
      accordion.classList.add('active');
      body.style.maxHeight = body.scrollHeight + 'px';
    }
  };
})();
