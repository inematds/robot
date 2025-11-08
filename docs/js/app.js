/* ========================================
   ROBOTICA DO ZERO AO EXPERT
   Main JavaScript File
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {

    /* ========================================
       MOBILE MENU TOGGLE
       ======================================== */

    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            // TODO: Implement mobile menu toggle
            console.log('Mobile menu clicked');
        });
    }

    /* ========================================
       SMOOTH SCROLL
       ======================================== */

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    /* ========================================
       TOPIC EXPANSION SYSTEM (ATIA Compact Topics)
       Based on FEP Pattern with ultra-compact spacing
       ======================================== */

    // Toggle topic explanations using event delegation
    document.addEventListener('click', function(e) {
        if (e.target.closest('.topic-button')) {
            const button = e.target.closest('.topic-button');
            const topicItem = button.closest('.topic-item');
            const explanation = topicItem.querySelector('.topic-explanation');

            if (explanation) {
                // Toggle (mostra/esconde) a explicação
                explanation.classList.toggle('hidden');

                // COMPORTAMENTO ACCORDION: Fecha outras explicações abertas no mesmo card
                const chapterCard = topicItem.closest('.chapter-card');
                if (chapterCard) {
                    chapterCard.querySelectorAll('.topic-explanation').forEach(exp => {
                        if (exp !== explanation) {
                            exp.classList.add('hidden');
                        }
                    });
                }

                // Add visual feedback
                if (!explanation.classList.contains('hidden')) {
                    button.classList.add('bg-gray-200');
                } else {
                    button.classList.remove('bg-gray-200');
                }
            }
        }
    });

    /* ========================================
       SCROLL TO TOP BUTTON
       ======================================== */

    // Create scroll to top button
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '↑';
    scrollButton.className = 'fixed bottom-6 right-6 bg-robo-primary text-white w-12 h-12 rounded-full shadow-lg hover:bg-blue-600 transition-all opacity-0 pointer-events-none';
    scrollButton.style.cssText = 'z-index: 1000; font-size: 24px; font-weight: bold;';
    document.body.appendChild(scrollButton);

    // Show/hide scroll button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollButton.style.opacity = '1';
            scrollButton.style.pointerEvents = 'auto';
        } else {
            scrollButton.style.opacity = '0';
            scrollButton.style.pointerEvents = 'none';
        }
    });

    // Scroll to top on click
    scrollButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    /* ========================================
       CONSOLE LOG
       ======================================== */

    console.log('🤖 Robótica do Zero ao Expert - JavaScript carregado!');
    console.log('📚 Sistema Compact Topics ATIA ativo');
});

/* ========================================
   MODULE TOGGLE FUNCTION (for Nivel pages)
   ======================================== */

function toggleModule(moduleNumber) {
    const module = document.getElementById('module-' + moduleNumber);
    const arrow = document.getElementById('arrow-' + moduleNumber);

    if (module && arrow) {
        // Toggle visibility
        module.classList.toggle('hidden');

        // Rotate arrow
        if (module.classList.contains('hidden')) {
            arrow.style.transform = 'rotate(0deg)';
        } else {
            arrow.style.transform = 'rotate(180deg)';
        }
    }
}
