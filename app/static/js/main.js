document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".tab");
    const underline = document.querySelector(".underline");
    const cards = document.querySelectorAll(".cards");

    function setActiveTab(target) {
        // Remove active class from all tabs
        tabs.forEach(tab => tab.classList.remove("active"));
        
        // Add active class to the clicked tab
        target.classList.add("active");

        // Set the position and width of the underline
        const rect = target.querySelector('span').getBoundingClientRect();
        underline.style.width = `${rect.width}px`;
        underline.style.left = `${target.offsetLeft + target.clientWidth / 2 - rect.width / 2}px`;

        // Show the corresponding section and hide others
        const targetSection = target.getAttribute("data-target");
        cards.forEach(card => {
            if (card.id === targetSection) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }

    // Initialize the underline position and visible section
    const activeTab = document.querySelector(".tab.active");
    if (activeTab) {
        setActiveTab(activeTab);
    }

    // Add click event listener to all tabs
    tabs.forEach(tab => {
        tab.addEventListener("click", function() {
            setActiveTab(this);
        });
    });
});
