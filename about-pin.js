/**
 * About 页 — GSAP ScrollTrigger pin + 横向 scrub
 * 向下滚动时固定区块，内容左右切换
 */
(function () {
  'use strict';

  const section = document.getElementById('about-scroll-section');
  const track = document.getElementById('about-slider');
  if (!section || !track) return;

  const slides = track.querySelectorAll('.about-slide');
  const dots = document.querySelectorAll('.about-slider-dot');
  const prevBtn = document.getElementById('about-prev');
  const nextBtn = document.getElementById('about-next');
  const labelEl = document.getElementById('about-slide-label');
  let currentSlide = 0;
  let aboutST = null;

  function $(id) {
    return document.getElementById(id);
  }

  function getSlideLabel(slide) {
    const lang = localStorage.getItem('chengyi-lang') || 'zh';
    const key = 'slideLabel' + (lang === 'zh' ? 'Zh' : lang === 'ms' ? 'Ms' : 'En');
    return slide.dataset[key] || slide.dataset.slideLabelZh || '';
  }

  function revealSlideContent(slide) {
    if (!slide) return;
    slide.querySelectorAll('.fade-up').forEach(el => el.classList.add('visible'));
    slide.querySelectorAll('.counter').forEach(counter => {
      if (counter.dataset.counted) return;
      counter.dataset.counted = 'true';
      const target = parseFloat(counter.dataset.target);
      const isFloat = target % 1 !== 0;
      const duration = 1500;
      const startTime = performance.now();
      function animate(currentTime) {
        const progress = Math.min((currentTime - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;
        counter.textContent = isFloat ? current.toFixed(1) : Math.floor(current);
        if (progress < 1) requestAnimationFrame(animate);
        else counter.textContent = isFloat ? target.toFixed(1) : target;
      }
      requestAnimationFrame(animate);
    });
  }

  function updateSlideUI(index) {
    if (!slides.length) return;
    currentSlide = Math.max(0, Math.min(index, slides.length - 1));
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === currentSlide);
      dot.setAttribute('aria-selected', i === currentSlide ? 'true' : 'false');
    });
    if (prevBtn) prevBtn.disabled = currentSlide === 0;
    if (nextBtn) nextBtn.disabled = currentSlide === slides.length - 1;
    const slide = slides[currentSlide];
    if (labelEl && slide) {
      const labelSpan = labelEl.querySelector('.tr');
      const text = getSlideLabel(slide);
      if (labelSpan) {
        labelSpan.textContent = text;
        labelSpan.setAttribute('data-zh', slide.dataset.slideLabelZh || text);
        labelSpan.setAttribute('data-ms', slide.dataset.slideLabelMs || text);
        labelSpan.setAttribute('data-en', slide.dataset.slideLabelEn || text);
      } else {
        labelEl.textContent = text;
      }
    }
    revealSlideContent(slide);
  }

  function getScrollDistance() {
    return Math.max(track.scrollWidth - window.innerWidth, 0);
  }

  function scrollToSlide(index) {
    const i = Math.max(0, Math.min(index, slides.length - 1));
    if (aboutST) {
      const progress = slides.length <= 1 ? 0 : i / (slides.length - 1);
      const y = aboutST.start + progress * (aboutST.end - aboutST.start);
      window.scrollTo({ top: y, behavior: 'smooth' });
    } else {
      const viewport = section.querySelector('.about-slider-viewport');
      if (viewport) {
        viewport.scrollTo({ left: i * viewport.clientWidth, behavior: 'smooth' });
      }
    }
  }

  dots.forEach(dot => {
    dot.addEventListener('click', () => scrollToSlide(parseInt(dot.dataset.slide, 10)));
  });
  if (prevBtn) prevBtn.addEventListener('click', () => scrollToSlide(currentSlide - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => scrollToSlide(currentSlide + 1));

  function initFallbackSlider() {
    section.classList.add('about-fallback');
    const viewport = section.querySelector('.about-slider-viewport');
    if (!viewport) return;
    viewport.addEventListener('scroll', () => {
      const index = Math.round(viewport.scrollLeft / viewport.clientWidth);
      if (index !== currentSlide) updateSlideUI(index);
    }, { passive: true });
    window.addEventListener('resize', () => {
      viewport.scrollTo({ left: currentSlide * viewport.clientWidth, behavior: 'auto' });
    });
    updateSlideUI(0);
  }

  function initGsapPin() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
      initFallbackSlider();
      return;
    }

    gsap.registerPlugin(ScrollTrigger);

    const pinWrap = document.getElementById('about-pin-wrap');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reducedMotion) {
      initFallbackSlider();
      return;
    }

    gsap.set(track, { x: 0 });

    const tween = gsap.to(track, {
      x: () => -getScrollDistance(),
      ease: 'none',
      scrollTrigger: {
        trigger: section,
        pin: pinWrap,
        scrub: 0.6,
        start: 'top top',
        end: () => '+=' + getScrollDistance(),
        invalidateOnRefresh: true,
        anticipatePin: 1,
        onUpdate: (self) => {
          const index = slides.length <= 1
            ? 0
            : Math.round(self.progress * (slides.length - 1));
          if (index !== currentSlide) updateSlideUI(index);
        },
        onEnter: () => updateSlideUI(0),
      },
    });

    aboutST = tween.scrollTrigger;

    ScrollTrigger.addEventListener('refreshInit', () => {
      gsap.set(track, { x: 0 });
    });

    window.addEventListener('resize', () => ScrollTrigger.refresh());

    updateSlideUI(0);
    ScrollTrigger.refresh();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGsapPin);
  } else {
    initGsapPin();
  }
})();
