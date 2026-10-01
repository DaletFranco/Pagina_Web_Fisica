// JavaScript Application logic for Flujos & PINNs Web Dashboard

document.addEventListener('DOMContentLoaded', () => {
  initMainTabs();
  initSubTabs();
  initKeyboardEvents();
});

// Main Tabs Navigation
function initMainTabs() {
  const tabBtns = document.querySelectorAll('.main-tabs .tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const activeContent = document.getElementById(targetTab);
      if (activeContent) {
        activeContent.classList.add('active');
      }

      // Re-render MathJax if present
      if (window.MathJax) {
        window.MathJax.typesetPromise();
      }
    });
  });
}

// Subtabs Navigation
function initSubTabs() {
  const subtabBtns = document.querySelectorAll('.subtab-btn');
  
  subtabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const parentTab = btn.closest('.tab-content');
      const targetSubtab = btn.getAttribute('data-subtab');

      const siblingsBtns = parentTab.querySelectorAll('.subtab-btn');
      const siblingsContents = parentTab.querySelectorAll('.subtab-content');

      siblingsBtns.forEach(b => b.classList.remove('active'));
      siblingsContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const activeSubcontent = document.getElementById(targetSubtab);
      if (activeSubcontent) {
        activeSubcontent.classList.add('active');
      }

      if (window.MathJax) {
        window.MathJax.typesetPromise();
      }
    });
  });
}

// Modal View Functions
function openModal(imageSrc, captionText) {
  const modal = document.getElementById('image-modal');
  const modalImg = document.getElementById('modal-img');
  const modalCaption = document.getElementById('modal-caption');

  if (modal && modalImg) {
    modalImg.src = imageSrc;
    if (modalCaption) modalCaption.innerText = captionText || '';
    modal.classList.add('active');
  }
}

function closeModal() {
  const modal = document.getElementById('image-modal');
  if (modal) {
    modal.classList.remove('active');
  }
}

function initKeyboardEvents() {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

// Global scope attachment for inline onclick handlers
window.openModal = openModal;
window.closeModal = closeModal;
