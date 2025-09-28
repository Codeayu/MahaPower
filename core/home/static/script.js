document.addEventListener('DOMContentLoaded', function() {
    
    // Enhanced Search Functionality with Live Search
    const searchInputEn = document.getElementById('scheme-search');
    const searchInputMr = document.getElementById('scheme-search-mr');
    let searchTimeout;
    
    function performLiveSearch(searchTerm) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const schemeCards = document.querySelectorAll('.scheme-card');
            const term = searchTerm.toLowerCase();
            
            schemeCards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const summary = card.querySelector('p').textContent.toLowerCase();
                const sector = card.querySelector('span').textContent.toLowerCase();
                
                if (term === '' || title.includes(term) || summary.includes(term) || sector.includes(term)) {
                    card.style.display = 'block';
                    card.classList.add('animate-fade-in');
                } else {
                    card.style.display = 'none';
                }
            });
        }, 300);
    }
    
    if (searchInputEn) {
        searchInputEn.addEventListener('input', function() {
            performLiveSearch(this.value);
        });
    }
    
    if (searchInputMr) {
        searchInputMr.addEventListener('input', function() {
            performLiveSearch(this.value);
        });
    }
    
    // Scheme Category Filter Functionality
    const filterButtons = document.querySelectorAll('.scheme-filter-btn');
    const schemeCards = document.querySelectorAll('.scheme-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Update active button with smooth animation
            filterButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.style.transform = 'scale(1)';
            });
            this.classList.add('active');
            this.style.transform = 'scale(1.05)';
            
            // Filter and animate scheme cards
            schemeCards.forEach((card, index) => {
                const cardCategory = card.getAttribute('data-category');
                if (category === 'all' || cardCategory === category || cardCategory?.includes(category)) {
                    setTimeout(() => {
                        card.style.display = 'block';
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            card.style.transition = 'all 0.5s ease';
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 50);
                    }, index * 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(-20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
    
    // Interactive Quick Action Buttons
    const quickActionButtons = document.querySelectorAll('button[class*="bg-white/20"]');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 100);
            }, 100);
            
            // Simulate filtering based on button text
            if (buttonText.includes('Recent') || buttonText.includes('नुकतेच')) {
                console.log('Filtering recently added schemes...');
            } else if (buttonText.includes('Popular') || buttonText.includes('लोकप्रिय')) {
                console.log('Filtering popular schemes...');
            } else if (buttonText.includes('Subsidy') || buttonText.includes('सबसिडी')) {
                console.log('Filtering high subsidy schemes...');
            }
        });
    });
    
    // Bookmark functionality for scheme cards
    const bookmarkButtons = document.querySelectorAll('.scheme-card button[class*="border-2"]');
    bookmarkButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const icon = this.querySelector('i');
            const isBookmarked = icon.classList.contains('fas');
            
            if (isBookmarked) {
                icon.classList.remove('fas');
                icon.classList.add('far');
                this.classList.remove('bg-[#000080]', 'text-white');
                this.classList.add('bg-white', 'text-[#000080]');
                
                // Show notification
                showNotification('Bookmark removed', 'bookmark-remove');
            } else {
                icon.classList.remove('far');
                icon.classList.add('fas');
                this.classList.remove('bg-white', 'text-[#000080]');
                this.classList.add('bg-[#000080]', 'text-white');
                
                // Show notification
                showNotification('Added to bookmarks', 'bookmark-add');
            }
            
            // Add animation effect
            this.style.transform = 'scale(1.2)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
        });
    });
    
    // Smooth scroll for navigation links
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
    
    // Add scroll-triggered animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observe all cards and feature sections
    document.querySelectorAll('.scheme-card, .feature-card, .group').forEach(el => {
        observer.observe(el);
    });
    
    // Statistics counter animation
    const statsCounters = document.querySelectorAll('[class*="text-2xl md:text-3xl font-bold text-yellow-200"]');
    statsCounters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/[^\d]/g, ''));
        if (target) {
            animateCounter(counter, target);
        }
    });
    
    // Enhanced Mobile Menu (if needed)
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Animate menu items
            const menuItems = mobileMenu.querySelectorAll('a');
            menuItems.forEach((item, index) => {
                setTimeout(() => {
                    item.style.transform = 'translateX(0)';
                    item.style.opacity = '1';
                }, index * 100);
            });
        });
    }
    
    // Phone number click tracking
    document.querySelectorAll('a[href^="tel:"]').forEach(telLink => {
        telLink.addEventListener('click', function() {
            console.log('Phone call initiated:', this.href);
            // Analytics tracking can be added here
        });
    });
});

// Utility Functions
function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transform translate-x-full transition-transform duration-300 ${
        type === 'bookmark-add' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${type === 'bookmark-add' ? 'fa-check' : 'fa-times'} mr-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Animate out and remove
    setTimeout(() => {
        notification.style.transform = 'translateX(full)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        if (element.textContent.includes('₹')) {
            element.textContent = `₹${Math.floor(current)}${element.textContent.includes('Cr') ? 'Cr+' : 'L+'}`;
        } else if (element.textContent.includes('को')) {
            element.textContent = `₹${Math.floor(current)}को+`;
        } else {
            element.textContent = `${Math.floor(current).toLocaleString()}${element.textContent.includes('+') ? '+' : ''}`;
        }
    }, 50);
}

// Custom CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in-up {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Smooth transitions for all interactive elements */
    button, a, .scheme-card, .feature-card {
        transition: all 0.3s ease;
    }
    
    /* Enhanced hover effects */
    .scheme-card:hover {
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    /* Loading states */
    .loading {
        position: relative;
        overflow: hidden;
    }
    
    .loading::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0% { left: -100%; }
        100% { left: 100%; }
    }
`;
document.head.appendChild(style);