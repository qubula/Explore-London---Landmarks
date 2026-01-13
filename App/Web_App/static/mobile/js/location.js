let autocomplete;
let startAutocomplete;

// Clear saved locations on page load for fresh start
localStorage.removeItem('alfie_start');
localStorage.removeItem('alfie_destination');

function initAutocomplete() {
    // Setup destination input autocomplete
    const input = document.getElementById('destination-input');
    const options = {
        fields: ['formatted_address', 'geometry', 'name'],
        strictBounds: false,
        types: ['establishment', 'geocode'],
        componentRestrictions: { country: 'uk' } // Restrict to UK for now
    };

    autocomplete = new google.maps.places.Autocomplete(input, options);

    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();

        if (!place.geometry || !place.geometry.location) {
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        selectDestination(place);
    });

    // Setup start location input autocomplete
    const startInput = document.getElementById('start-input');
    startAutocomplete = new google.maps.places.Autocomplete(startInput, options);

    startAutocomplete.addListener('place_changed', () => {
        const place = startAutocomplete.getPlace();

        if (!place.geometry || !place.geometry.location) {
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        // Save start location
        const startLocation = {
            name: place.name,
            address: place.formatted_address,
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng()
        };
        localStorage.setItem('alfie_start', JSON.stringify(startLocation));
    });

    // Always get fresh current location on page load
    getCurrentLocationAsStart();
}

function getCurrentLocationAsStart() {
    const startInput = document.getElementById('start-input');

    if (navigator.geolocation) {
        startInput.placeholder = "Getting your location...";

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                // Reverse geocode to get address
                const geocoder = new google.maps.Geocoder();
                geocoder.geocode({ location: pos }, (results, status) => {
                    if (status === 'OK' && results[0]) {
                        const startLocation = {
                            name: "Current Location",
                            address: results[0].formatted_address,
                            lat: pos.lat,
                            lng: pos.lng
                        };
                        localStorage.setItem('alfie_start', JSON.stringify(startLocation));
                        startInput.value = results[0].formatted_address;
                    } else {
                        // Fallback to coordinates if geocoding fails
                        const startLocation = {
                            name: "Current Location",
                            address: "Lat: " + pos.lat.toFixed(4) + ", Lng: " + pos.lng.toFixed(4),
                            lat: pos.lat,
                            lng: pos.lng
                        };
                        localStorage.setItem('alfie_start', JSON.stringify(startLocation));
                        startInput.value = startLocation.address;
                    }
                });
            },
            (error) => {
                console.error("Error getting location:", error);
                startInput.placeholder = "Enter start location";
            }
        );
    } else {
        startInput.placeholder = "Enter start location";
    }
}

function selectDestination(place) {
    console.log("Selected:", place);

    // Store in localStorage
    const destination = {
        name: place.name,
        address: place.formatted_address,
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
    };
    localStorage.setItem('alfie_destination', JSON.stringify(destination));

    // Animate and Navigate
    const card = document.querySelector('.search-section');
    card.classList.add('pulse');

    setTimeout(() => {
        // Navigate to Route Mode selection
        window.location.href = '/mobile/route-mode';
    }, 400);
}

// Current Location Button removed - start location now automatically uses current location

// Popular Suggestions Handler
document.querySelectorAll('.suggestion-item').forEach(item => {
    item.addEventListener('click', () => {
        const name = item.dataset.place;
        // In a real app, we'd probably geocode this or have pre-stored coords
        // For the prototype, we can use the input to trigger autocomplete search or just set text
        const input = document.getElementById('destination-input');
        input.value = name;
        input.focus();
        // Triggering autocomplete programmatically is tricky, usually better to just prepopulate input
    });
});

// Clear input handler
const input = document.getElementById('destination-input');
const clearBtn = document.getElementById('clear-input');

input.addEventListener('input', () => {
    if (input.value.length > 0) {
        clearBtn.classList.remove('hidden');
    } else {
        clearBtn.classList.add('hidden');
    }
});

clearBtn.addEventListener('click', () => {
    input.value = '';
    clearBtn.classList.add('hidden');
    input.focus();
});
