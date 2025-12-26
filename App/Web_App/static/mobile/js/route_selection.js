// Check if destination is set, otherwise redirect back
document.addEventListener('DOMContentLoaded', () => {
    const destination = localStorage.getItem('alfie_destination');
    if (!destination) {
        window.location.href = '/mobile/destination';
    } else {
        console.log("Planning route to:", JSON.parse(destination).name);
        // Here we would ideally fetch real ETA estimates from the backend
        // based on current location and destination.
        // For now, we use placeholders in HTML, but we could update them here.
    }
});

let selectedMode = null;

function selectMode(mode) {
    selectedMode = mode;
    
    // Update UI
    document.querySelectorAll('.mode-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Find the clicked card logic (could be improved with event delegation or direct ref)
    // For simplicity, we just look for the onclick attribute or assume structure
    // Actually, the easiest way with the current HTML is to find the one with the correct onclick handler
    // But since we passed the string, let's just use data attributes next time. 
    // For now, let's iterate and check.
    
    // Better: add IDs or data-mode to HTML
    // Let's assume the order: 0 is fastest, 1 is scenic. 
    // Or better, let's update ID in the HTML. 
    // Wait, I can just use `event.currentTarget` if I passed event, but I didn't.
    // Let's just select by index for now based on 'mode' string.
    
    const cards = document.querySelectorAll('.mode-card');
    if (mode === 'fastest') {
        cards[0].classList.add('selected');
    } else {
        cards[1].classList.add('selected');
    }

    // Enable Continue Button
    const btn = document.getElementById('continue-btn');
    btn.classList.remove('disabled');
    btn.disabled = false;
    btn.innerHTML = mode === 'scenic' ? 'Choose Tour Type' : 'Start Journey';
}

function proceedToNext() {
    if (!selectedMode) return;

    // Save selection
    localStorage.setItem('alfie_route_mode', selectedMode);

    if (selectedMode === 'scenic') {
        // Go to Tour Type Selection
        window.location.href = '/mobile/tour-type';
    } else {
        // Go directly to active tour (fastest mode doesn't need tour type)
        localStorage.setItem('alfie_tour_type', 'all'); // Default for fastest
        window.location.href = '/mobile/tour';
    }
}
