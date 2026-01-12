// Google Maps API Error Detection
window.gm_authFailure = function() {
    alert('❌ GOOGLE MAPS ERROR: Invalid API key or billing issue.\n\nPlease check:\n1. Google Cloud Console billing\n2. API key restrictions\n3. Maps JavaScript API is enabled');
    console.error('Google Maps authentication failed - likely billing or API key issue');
};

// Detect other Google Maps errors
window.addEventListener('load', function() {
    setTimeout(function() {
        if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
            alert('❌ GOOGLE MAPS ERROR: Failed to load Google Maps API.\n\nPossible causes:\n1. Network issue\n2. API key invalid\n3. Billing not active');
            console.error('Google Maps API failed to load');
        }
    }, 5000);
});

// Prevent reload loops by catching errors
window.addEventListener('error', function(e) {
    console.error('Global error caught:', e.error || e.message);
    // Show error to user if it's related to Google Maps
    if (e.message && e.message.includes('google')) {
        alert('Error loading Google Maps: ' + e.message);
    }
    // Don't reload - just log the error
    e.preventDefault();
    return true;
});

// State
let selectedDetails = {
    destination: null,
    mode: null,
    tourType: null,
    currentLocation: null
};

let map;
let landmarks = [];
let watchId;
let userMarker;
let visited = [];

// Init
document.addEventListener('DOMContentLoaded', () => {
    // Load state from localStorage
    try {
        selectedDetails.destination = JSON.parse(localStorage.getItem('alfie_destination'));
        selectedDetails.mode = localStorage.getItem('alfie_route_mode');
        selectedDetails.tourType = localStorage.getItem('alfie_tour_type');

        console.log('Tour page loaded with:', {
            destination: selectedDetails.destination,
            mode: selectedDetails.mode,
            tourType: selectedDetails.tourType
        });

        if (!selectedDetails.destination) {
            console.error("No destination found in localStorage");
            alert("No destination found. Please start from the beginning.");
            // Prevent reload loop - only redirect once
            if (!sessionStorage.getItem('tour_redirect_attempted')) {
                sessionStorage.setItem('tour_redirect_attempted', 'true');
                window.location.href = '/mobile';
            }
            return;
        }

        // Clear redirect flag if we have valid data
        sessionStorage.removeItem('tour_redirect_attempted');

    } catch (e) {
        console.error("Error parsing storage", e);
        alert("Error loading tour data: " + e.message);
        return;
    }

    // Start GPS tracking
    startGPS();
});

// Helper function to safely convert values to numbers
function toNum(v) {
    return v === null || v === undefined ? null : Number(v);
}

// Haversine distance calculation (copied from track.html)
function distanceMeters(lat1, lon1, lat2, lon2) {
    if (lat1 == null || lon1 == null || lat2 == null || lon2 == null) return Infinity;
    const R = 6371000; // Earth radius in meters
    const toRad = d => d * Math.PI / 180;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function initMap() {
    console.log('initMap() called');
    const mapEl = document.getElementById('tour-map');

    if (!mapEl) {
        console.error('Map element #tour-map not found in DOM!');
        alert('Error: Map element not found. Please refresh the page.');
        return;
    }

    console.log('Map element found, initializing Google Maps...');

    // Default center (London)
    const center = { lat: 51.5074, lng: -0.1278 };

    map = new google.maps.Map(mapEl, {
        center: center,
        zoom: 12,  // More zoomed out - shows wider area context
        disableDefaultUI: true,
        styles: [
            // Hide all POI and transit
            {
                "featureType": "poi",
                "stylers": [{ "visibility": "off" }]
            },
            {
                "featureType": "transit",
                "stylers": [{ "visibility": "off" }]
            },
            // Dark water
            {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [
                    { "color": "#1a1a1a" }  // Very dark, almost black
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels",
                "stylers": [{ "visibility": "off" }]
            },
            // Dark landscape to match charcoal background
            {
                "featureType": "landscape",
                "elementType": "geometry",
                "stylers": [
                    { "color": "#2a2a2a" }  // Same as background - seamless blend
                ]
            },
            // Roads - dark with subtle contrast
            {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [
                    { "color": "#3a3a3a" },  // Slightly lighter than background
                    { "weight": 0.8 }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.fill",
                "stylers": [
                    { "color": "#888888" },  // Muted gray labels
                    { "lightness": 25 }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.stroke",
                "stylers": [
                    { "visibility": "off" }
                ]
            },
            // Hide highway shields and route icons
            {
                "featureType": "road",
                "elementType": "labels.icon",
                "stylers": [{ "visibility": "off" }]
            },
            // Hide minor road labels
            {
                "featureType": "road.local",
                "elementType": "labels",
                "stylers": [{ "visibility": "off" }]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels",
                "stylers": [{ "visibility": "simplified" }]
            },
            // Administrative boundaries - very subtle
            {
                "featureType": "administrative",
                "elementType": "geometry.stroke",
                "stylers": [
                    { "color": "#444444" },
                    { "weight": 0.3 }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "labels",
                "stylers": [{ "visibility": "off" }]
            },
            // Parks - darker green-gray
            {
                "featureType": "landscape.natural",
                "elementType": "geometry",
                "stylers": [
                    { "color": "#252525" }  // Slightly darker than main background
                ]
            },
            // Buildings - subtle dark gray
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry",
                "stylers": [
                    { "color": "#303030" }
                ]
            }
        ]
    });

    // Calculate and display route
    calculateRoute();
}

function startGPS() {
    if (navigator.geolocation) {
        watchId = navigator.geolocation.watchPosition(
            handlePosition,
            (err) => console.error("GPS error:", err),
            { enableHighAccuracy: true, maximumAge: 3000, timeout: 20000 }
        );
    }
}

function handlePosition(pos) {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;

    // Update current location
    selectedDetails.currentLocation = { lat, lng: lon };

    // Update or create user marker
    updateUserMarker({ lat, lng: lon });

    // Center map on user's position (only first time)
    if (map && !userMarker) {
        map.setCenter({ lat, lng: lon });
    }

    // Check distance to each landmark and trigger if nearby
    let nextUnvisitedIdx = -1;
    let nextUnvisitedDist = Infinity;

    landmarks.forEach((lm, idx) => {
        const lmLat = toNum(lm.lat ?? lm.latitude ?? lm.lat_dd ?? lm["lat"]);
        const lmLon = toNum(lm.lng ?? lm.lon ?? lm.longitude ?? lm.lon_dd ?? lm["lon"]);
        const d = distanceMeters(lat, lon, lmLat, lmLon);

        // Track the next unvisited landmark
        if (!visited[idx] && d < nextUnvisitedDist) {
            nextUnvisitedIdx = idx;
            nextUnvisitedDist = d;
        }

        // Use landmark-specific trigger radius
        const triggerRadius = lm.radius_m ?? 120; // default 120m

        if (!visited[idx] && d <= triggerRadius) {
            visited[idx] = true;
            const script = lm.script ?? "(no script)";
            console.log(`Triggered landmark ${idx + 1}: ${lm.name} at ${d.toFixed(0)}m`);

            // Update UI to show landmark triggered
            updateLandmarkDisplay(idx, d, true);
        } else {
            updateLandmarkDisplay(idx, d, false);
        }
    });

}

function updateUserMarker(pos) {
    if (!map) return;

    if (!userMarker) {
        userMarker = new google.maps.Marker({
            position: pos,
            map: map,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 10,  // Slightly larger for visibility
                fillColor: "#2196F3",  // Bright blue
                fillOpacity: 1,
                strokeColor: "#ffffff",
                strokeWeight: 3,  // Thicker white border
            },
            title: "Your Location",
            zIndex: 1000  // Ensure it's on top
        });
    } else {
        userMarker.setPosition(pos);
    }
}

async function calculateRoute() {
    const dest = selectedDetails.destination;

    // Get start location from localStorage
    const savedStart = localStorage.getItem('alfie_start');
    let origin;

    if (savedStart) {
        const startLocation = JSON.parse(savedStart);
        origin = startLocation.address || startLocation.name;
    } else {
        origin = "Charing Cross, London";
    }

    // Update UI to show calculating
    document.getElementById('next-stop-name').innerText = 'Calculating route...';

    // Fetch route data from backend
    try {
        const response = await fetch('/api/plan-route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start: origin,
                end: dest.address || dest.name,
                mode: selectedDetails.mode === 'scenic' ? '2' : '1',
                tour_type: selectedDetails.tourType
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === 'success') {
            const result = data.result;
            landmarks = result.landmarks;
            visited = new Array(landmarks.length).fill(false);

            // Draw route using backend's pre-calculated route_points
            if (result.route_points && result.route_points.length > 0) {
                const path = result.route_points.map(point => ({
                    lat: point[0],
                    lng: point[1]
                }));

                // Draw polyline
                const routeLine = new google.maps.Polyline({
                    path: path,
                    geodesic: true,
                    strokeColor: '#FAF8F3',
                    strokeOpacity: 0.9,
                    strokeWeight: 5,
                    map: map
                });

                // Add start marker with custom white pin SVG
                new google.maps.Marker({
                    position: path[0],
                    map: map,
                    title: 'Start',
                    icon: {
                        url: '/static/mobile/images/markers/start-pin.svg',
                        scaledSize: new google.maps.Size(16, 28.5),  // Half size: 16x28.5
                        anchor: new google.maps.Point(8, 28.5)  // Anchor at bottom center of pin
                    },
                    zIndex: 100
                });

                // Add end marker with custom gray pin SVG
                new google.maps.Marker({
                    position: path[path.length - 1],
                    map: map,
                    title: 'Destination',
                    icon: {
                        url: '/static/mobile/images/markers/end-pin.svg',
                        scaledSize: new google.maps.Size(16, 28.5),  // Half size: 16x28.5
                        anchor: new google.maps.Point(8, 28.5)  // Anchor at bottom center of pin
                    },
                    zIndex: 100
                });

                // Fit map to route bounds with padding for breathing room
                const bounds = new google.maps.LatLngBounds();
                path.forEach(point => bounds.extend(point));
                map.fitBounds(bounds, {
                    top: 50,
                    right: 50,
                    bottom: 50,
                    left: 50
                });

                // Update journey ETA
                const etaMinutes = Math.round(result.chosen_eta);
                document.getElementById('journey-eta').innerText = `${etaMinutes} min`;

                // Update next stop info
                document.getElementById('next-stop-name').innerText = landmarks[0] ? landmarks[0].name : dest.name;
            }

            // Render landmark cards
            renderLandmarkCards(landmarks);

        } else {
            console.error("Route planning failed", data);
            document.getElementById('next-stop-name').innerText = 'Error planning route';
            alert("Could not plan route: " + (data.message || 'Unknown error'));
        }
    } catch (error) {
        console.error("API Error:", error);
        document.getElementById('next-stop-name').innerText = 'Error: ' + error.message;
        alert("Failed to connect to server.");
    }
}

let swiper; // Global swiper instance

function renderLandmarkCards(landmarks) {
    const cardsContainer = document.getElementById('landmark-cards');
    if (!cardsContainer) return;

    cardsContainer.innerHTML = '';

    landmarks.forEach((lm, index) => {
        const triggerRadius = lm.radius_m ?? 120;
        const imageUrl = lm.image_url;
        const script = lm.script || "No description available.";

        // Create swiper slide
        const slide = document.createElement('div');
        slide.className = 'swiper-slide';
        slide.id = 'lm_' + index;

        // Randomly select a stamp (1-6)
        const stampNumber = Math.floor(Math.random() * 6) + 1;
        const stampUrl = `/static/mobile/images/Stamp${stampNumber}.png`;

        // Build card HTML
        slide.innerHTML = `
            <div class="landmark-card" onclick="flipCard(this)">
                <!-- FRONT -->
                <div class="card-front">
                    <div class="postcard-label">POST CARD</div>

                    <div class="postage-stamp" style="background-image: url('${stampUrl}');"></div>

                    <div class="postmark"></div>

                    <div class="card-image-container">
                        ${imageUrl
                            ? `<img src="${imageUrl.replace('500px', '800px')}" alt="${lm.name}" class="card-image" onerror="this.outerHTML='<div class=\\'card-placeholder\\'>🏛️</div>'">`
                            : `<div class="card-placeholder">🏛️</div>`
                        }
                    </div>
                    <div class="card-info">
                        <div class="card-title">${lm.name}</div>
                        <div class="card-subtitle">London, England</div>
                        <div class="card-meta">
                            <div class="card-distance">
                                <span>📍</span>
                                <span class="distance-value">Calculating...</span>
                            </div>
                            <div class="card-status">
                                <span class="status-dot"></span>
                                <span class="status-text">Upcoming</span>
                            </div>
                        </div>
                    </div>
                    <div class="flip-hint">
                        <span>✉️</span>
                        <span>Tap to read message</span>
                    </div>
                </div>

                <!-- BACK -->
                <div class="card-back">
                    <div class="card-back-content">
                        <div class="message-area">
                            <p>${script}</p>
                        </div>

                        <div class="address-area">
                            <div class="address-header">POSTCARD</div>
                            <div class="address-lines">
                                <div class="address-line"></div>
                                <div class="address-line"></div>
                                <div class="address-line"></div>
                            </div>
                            <div class="location-stamp">
                                LONDON<br/>
                                ENGLAND
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        cardsContainer.appendChild(slide);
    });

    // Initialize Swiper after cards are rendered
    if (swiper) {
        swiper.destroy();
    }

    swiper = new Swiper('.landmark-swiper', {
        effect: 'cards',
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: 'auto',
        speed: 400,
        cardsEffect: {
            perSlideOffset: 8,
            perSlideRotate: 2,
            rotate: true,
            slideShadows: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            type: 'bullets',
        },
        // Performance optimizations
        preventInteractionOnTransition: true,
        touchRatio: 1,
        touchAngle: 45,
        longSwipesRatio: 0.5,
        longSwipesMs: 300,
    });
}

function flipCard(cardElement) {
    cardElement.classList.toggle('flipped');
}

// Make flipCard global
window.flipCard = flipCard;

function updateLandmarkDisplay(idx, distance, triggered) {
    const lmEl = document.getElementById('lm_' + idx);
    if (!lmEl) return;

    // Update distance on card
    const distValue = lmEl.querySelector('.distance-value');
    if (distValue) {
        if (distance === Infinity) {
            distValue.textContent = 'Calculating...';
        } else if (distance < 1000) {
            distValue.textContent = `${distance.toFixed(0)}m away`;
        } else {
            distValue.textContent = `${(distance / 1000).toFixed(1)}km away`;
        }
    }

    // Update status
    const statusDot = lmEl.querySelector('.status-dot');
    const statusText = lmEl.querySelector('.status-text');

    if (triggered) {
        if (statusDot) statusDot.classList.add('triggered');
        if (statusText) statusText.textContent = 'Visited';
    }
}

function endTour() {
    if (confirm("End the tour?")) {
        if (watchId) {
            navigator.geolocation.clearWatch(watchId);
        }
        window.location.href = '/mobile';
    }
}

// Make initMap global for callback
window.initMap = initMap;
window.initAutocomplete = () => { }; // Stub if needed
