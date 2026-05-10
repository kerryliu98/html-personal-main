document.addEventListener('DOMContentLoaded', () => {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Intersection Observer for fade-in elements
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const fadeOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const fadeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, fadeOptions);

    fadeElements.forEach(element => {
        fadeObserver.observe(element);
    });

    // Mobile menu toggle (placeholder for future implementation)
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if(hamburger) {
        hamburger.addEventListener('click', () => {
            // Toggle nav links visibility
            if(navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
            } else {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '70px';
                navLinks.style.right = '2rem';
                navLinks.style.background = 'var(--glass-bg)';
                navLinks.style.backdropFilter = 'blur(12px)';
                navLinks.style.padding = '2rem';
                navLinks.style.borderRadius = '12px';
                navLinks.style.border = '1px solid var(--glass-border)';
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Close mobile menu if open
                if(window.innerWidth <= 768 && navLinks.style.display === 'flex') {
                    navLinks.style.display = 'none';
                }

                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Typing effect for the hero title
    const typingText = document.querySelector('.typing-text');
    const words = ['Data Developer', 'Data Engineer'];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingDelay = 150;
    
    function type() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            typingText.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
            typingDelay = 50;
        } else {
            typingText.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
            typingDelay = 150;
        }

        if (!isDeleting && charIndex === currentWord.length) {
            isDeleting = true;
            typingDelay = 2000; // Pause at end
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typingDelay = 500; // Pause before typing new word
        }

        setTimeout(type, typingDelay);
    }

    // Start typing effect after a short delay
    if(typingText) {
        setTimeout(type, 1000);
    }
});
