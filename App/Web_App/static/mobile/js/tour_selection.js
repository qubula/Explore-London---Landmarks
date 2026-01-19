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
    console.log('[Tour Availability] Starting check...');

    // Show loading overlay
    const loadingOverlay = document.getElementById('loading-overlay');

    const startData = localStorage.getItem('alfie_start');
    const endData = localStorage.getItem('alfie_destination');
    const mode = localStorage.getItem('alfie_route_mode');

    console.log('[Tour Availability Check]', {
        startData: startData ? 'exists' : 'missing',
        endData: endData ? 'exists' : 'missing',
        mode: mode
    });

    if (!startData || !endData) {
        console.warn('No route information found - cannot check availability');
        console.log('[Tour Availability] Skipping - showing all themes');

        // Hide loading overlay
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }

        // Temporary debug message for user
        const descElem = document.getElementById('tour-desc');
        if (descElem) {
            descElem.textContent = '⚠️ Debug: No route data found in storage';
            descElem.style.color = 'red';
        }
        return;
    }

    // Parse JSON stored location data
    const startLocation = JSON.parse(startData);
    const endLocation = JSON.parse(endData);

    // Extract address or name for API
    const start = startLocation.address || startLocation.name;
    const end = endLocation.address || endLocation.name;

    console.log('[Tour Availability] Checking:', { start, end, mode });

    try {
        const response = await fetch('/api/check-tour-availability', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start, end, mode })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        console.log('[Tour Availability] Response:', data);

        if (data.status === 'success') {
            const availability = data.availability;
            const landmarkCounts = data.landmark_counts || {};

            console.log('[Tour Availability] Filtering cards based on:', availability);
            console.log('[Tour Availability] Landmark counts:', landmarkCounts);

            // Hide tour cards that have no landmarks
            let hiddenCount = 0;
            let totalCards = 0;
            let visibleThemeCards = []; // Track visible theme cards (excluding "all")

            // First pass: remove any existing full-width classes and collect visible cards
            document.querySelectorAll('.tour-card').forEach(card => {
                // Remove full-width from all theme cards (not Surprise Me)
                if (!card.classList.contains('featured-tour')) {
                    card.classList.remove('full-width');
                }

                totalCards++;
                const onclickAttr = card.getAttribute('onclick');
                if (!onclickAttr) {
                    console.warn('[Tour Availability] Card has no onclick attribute', card);
                    return;
                }

                const match = onclickAttr.match(/selectTourType\('([^']+)'\)/);

                if (match && match[1]) {
                    const tourType = match[1];
                    console.log(`[Tour Availability] Checking ${tourType}:`, availability[tourType]);

                    if (availability[tourType] === false) {
                        // Hide the card completely
                        card.style.display = 'none';
                        card.classList.add('hidden-unavailable');

                        hiddenCount++;
                        console.log(`[Tour Availability] ✓ HIDING ${tourType} - no landmarks available`);
                    } else {
                        console.log(`[Tour Availability] ✓ SHOWING ${tourType} - has landmarks`);

                        // Track visible theme cards (not "all")
                        if (tourType !== 'all') {
                            visibleThemeCards.push({
                                element: card,
                                type: tourType,
                                count: landmarkCounts[tourType] || 0
                            });
                        }
                    }
                }
            });

            console.log(`[Tour Availability] Summary: Hidden ${hiddenCount} of ${totalCards} tour types`);
            console.log(`[Tour Availability] Visible theme cards: ${visibleThemeCards.length}`);

            // If odd number of visible theme cards, make the one with most landmarks full-width
            if (visibleThemeCards.length % 2 === 1) {
                // Sort by landmark count descending to find the best one
                visibleThemeCards.sort((a, b) => b.count - a.count);
                const topTheme = visibleThemeCards[0];

                if (topTheme) {
                    topTheme.element.classList.add('full-width');
                    console.log(`[Tour Availability] ✓ Making ${topTheme.type} full-width (${topTheme.count} landmarks)`);
                }
            } else {
                console.log(`[Tour Availability] ✓ Even number of cards (${visibleThemeCards.length}), no full-width needed`);
            }

            // Update page description to show filtering happened
            if (hiddenCount > 0) {
                const descElem = document.getElementById('tour-desc');
                if (descElem) {
                    descElem.textContent = 'Themes available on your route';
                }
            }

            // Hide loading overlay after successful check
            if (loadingOverlay) {
                loadingOverlay.classList.add('hidden');
            }
        }
    } catch (error) {
        console.error('[Tour Availability] Error:', error);

        // Hide loading overlay on error
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }

        // Temporary debug message for user
        const descElem = document.getElementById('tour-desc');
        if (descElem) {
            descElem.textContent = `⚠️ Debug: API error - ${error.message}`;
            descElem.style.color = 'orange';
        }
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
