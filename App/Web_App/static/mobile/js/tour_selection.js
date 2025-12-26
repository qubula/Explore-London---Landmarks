const tourData = {
    'architecture': {
        title: 'Architecture',
        desc: 'Discover London\'s iconic skyline, from historic masterpieces to modern wonders.'
    },
    'historical': {
        title: 'History',
        desc: 'Step back in time and uncover the stories that built this city.'
    },
    'royal': {
        title: 'Royal London',
        desc: 'Follow the footsteps of monarchs and explore regal landmarks.'
    },
    'modern': {
        title: 'Modern City',
        desc: 'Experience the vibrant contemporary side of London.'
    },
    'museums_galleries': {
        title: 'Museums & Galleries',
        desc: 'Art galleries, museums, and cultural institutions that inspire and educate.'
    },
    'parks_gardens': {
        title: 'Parks & Gardens',
        desc: 'Green spaces, royal parks, and botanical gardens perfect for a peaceful stroll.'
    },
    'religious': {
        title: 'Religious Heritage',
        desc: 'Cathedrals, churches, abbeys, and sacred sites steeped in history.'
    },
    'victorian': {
        title: 'Victorian Era',
        desc: '19th century landmarks and Victorian architecture from London\'s golden age.'
    },
    'all': {
        title: 'Surprise Me',
        desc: 'A curated mix of the best sights along your route.'
    }
};

let selectedTour = null;

// Check tour availability on page load
async function checkTourAvailability() {
    const start = localStorage.getItem('alfie_start_location');
    const end = localStorage.getItem('alfie_end_location');
    const mode = localStorage.getItem('alfie_route_mode');

    if (!start || !end) {
        console.warn('No route information found');
        return;
    }

    try {
        const response = await fetch('/api/check-tour-availability', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start, end, mode })
        });

        const data = await response.json();

        if (data.status === 'success') {
            const availability = data.availability;

            // Hide tour cards that have no landmarks
            document.querySelectorAll('.tour-card').forEach(card => {
                const onclickAttr = card.getAttribute('onclick');
                const match = onclickAttr.match(/selectTourType\('([^']+)'\)/);

                if (match && match[1]) {
                    const tourType = match[1];
                    if (availability[tourType] === false) {
                        card.style.display = 'none';
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error checking tour availability:', error);
        // If there's an error, show all tours (fail gracefully)
    }
}

// Run availability check when page loads
document.addEventListener('DOMContentLoaded', checkTourAvailability);

function selectTourType(type) {
    const sheet = document.getElementById('tour-sheet');

    // De-selection: If clicking the same tour type again, deselect it
    if (selectedTour === type) {
        selectedTour = null;
        document.querySelectorAll('.tour-card').forEach(card => card.classList.remove('selected'));
        sheet.classList.remove('active');
        return;
    }

    selectedTour = type;

    // Highlight Card
    document.querySelectorAll('.tour-card').forEach(card => card.classList.remove('selected'));

    // Find the specific card by exact match on tour type
    const cards = document.getElementsByClassName('tour-card');
    for (let card of cards) {
        const onclickAttr = card.getAttribute('onclick');
        // Extract tour type from onclick="selectTourType('TYPE')"
        const match = onclickAttr.match(/selectTourType\('([^']+)'\)/);
        if (match && match[1] === type) {
            card.classList.add('selected');
        }
    }

    // Show Bottom Sheet
    const title = document.getElementById('sheet-title');
    const desc = document.getElementById('sheet-desc');

    title.textContent = tourData[type].title;
    desc.textContent = tourData[type].desc;

    sheet.classList.add('active');
}

function confirmTour() {
    if (!selectedTour) return;

    localStorage.setItem('alfie_tour_type', selectedTour);

    // Navigate to Active Tour
    window.location.href = '/mobile/tour';
}

function closeSheet() {
    const sheet = document.getElementById('tour-sheet');
    sheet.classList.remove('active');
    document.querySelectorAll('.tour-card').forEach(card => card.classList.remove('selected'));
    selectedTour = null;
}

// Close sheet when clicking outside is a nice touch
document.addEventListener('click', (e) => {
    const sheet = document.getElementById('tour-sheet');
    if (sheet.classList.contains('active') &&
        !sheet.contains(e.target) &&
        !e.target.closest('.tour-card')) {
        closeSheet();
    }
});
