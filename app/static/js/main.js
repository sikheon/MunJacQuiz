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

document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const quizId = this.getAttribute('data-id');
        const isBookmarked = this.getAttribute('data-bookmarked') === 'true';
        const cardElement = document.getElementById(`bookmark-card-${quizId}`);
        const bookmarkedSection = document.getElementById('bookmarked');

        fetch(`/toggle_bookmark/${quizId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'removed') {
                this.setAttribute('data-bookmarked', 'false');
                this.classList.remove('bookmarked');
                
                // 북마크 페이지에서 카드 제거
                if (bookmarkedSection.contains(cardElement)) {
                    cardElement.remove();
                    
                    // 모든 북마크가 제거되었는지 확인
                    if (bookmarkedSection.querySelectorAll('.card').length === 0) {
                        document.getElementById('no-bookmarks-message').style.display = 'block';
                    }
                }
            } else {
                this.setAttribute('data-bookmarked', 'true');
                this.classList.add('bookmarked');
            }
        });
    });
});
