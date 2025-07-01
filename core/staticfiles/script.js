document.addEventListener('DOMContentLoaded', function() {
    // Language Toggle Functionality
    const langToggleBtn = document.getElementById('langToggle');
    let isEnglish = true;
    
    langToggleBtn.addEventListener('click', function() {
        isEnglish = !isEnglish;
        
        if (isEnglish) {
            langToggleBtn.textContent = 'English | मराठी';
            document.querySelectorAll('.english').forEach(el => {
                el.style.display = 'block';
            });
            document.querySelectorAll('.marathi').forEach(el => {
                el.style.display = 'block';
                el.style.fontSize = '0.9rem';
                el.style.color = '#666';
            });
        } else {
            langToggleBtn.textContent = 'मराठी | English';
            document.querySelectorAll('.english').forEach(el => {
                el.style.display = 'none';
            });
            document.querySelectorAll('.marathi').forEach(el => {
                el.style.display = 'block';
                el.style.fontSize = '1rem';
                el.style.color = '#333';
            });
        }
    });
    
    // Search Functionality
    const searchInput = document.querySelector('.search-bar input');
    const searchBtn = document.querySelector('.search-btn');
    const schemeCards = document.querySelectorAll('.scheme-card');
    const filterDropdowns = document.querySelectorAll('.filter-dropdown');
    
    // Simple search function
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedType = filterDropdowns[0].value;
        const selectedSector = filterDropdowns[1].value;
        
        schemeCards.forEach(card => {
            const title = card.querySelector('.scheme-title').textContent.toLowerCase();
            const titleMarathi = card.querySelector('.scheme-title-marathi').textContent.toLowerCase();
            const summary = card.querySelector('.scheme-summary').textContent.toLowerCase();
            const sector = card.querySelector('.scheme-badge').textContent.toLowerCase();
            
            // Check if card matches search criteria
            const matchesSearch = searchTerm === '' || 
                                 title.includes(searchTerm) || 
                                 titleMarathi.includes(searchTerm) || 
                                 summary.includes(searchTerm);
            
            const matchesSector = selectedSector === '' || sector.toLowerCase() === selectedSector;
            
            // For demo purposes, we're using a simplified approach for scheme type
            // In a real application, you would have actual data attributes for this
            const matchesType = selectedType === '' || 
                               (selectedType === 'loan' && summary.includes('interest')) ||
                               (selectedType === 'skill' && title.includes('skill')) ||
                               (selectedType === 'funding' && summary.includes('funding'));
            
            if (matchesSearch && matchesSector && matchesType) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Add event listeners
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    filterDropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', performSearch);
    });
    
    // View Details Button Functionality
    const viewDetailsButtons = document.querySelectorAll('.view-details');
    
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const schemeName = this.closest('.scheme-card').querySelector('.scheme-title').textContent;
            alert(`You clicked to view details for: ${schemeName}\nThis would navigate to the scheme details page in a complete implementation.`);
        });
    });
});