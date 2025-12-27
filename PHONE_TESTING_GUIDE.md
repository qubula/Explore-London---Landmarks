# Phone Testing Setup Guide

## Quick Start (2 Steps)

### 1. Start the Server
```bash
cd /Users/kuba_jarzebski/Documents/Portfolio/Unit\ 9\ -\ Personal\ Project/App/Tour\ Guide/OpenAI_API_Version/V3/V4
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Important:** Use `--host 0.0.0.0` to allow connections from your phone!

### 2. Access from Phone

**Your Mac's IP Address:** `192.168.1.196`

**Open on your phone:**
```
http://192.168.1.196:8000/mobile
```

---

## Testing Configuration

### Current Setup (For Home Testing)
- ✅ **Start Location:** Fixed to "Charing Cross, London"
- ✅ **GPS Disabled:** Uses test location instead
- ✅ **Phone Access:** Server allows network connections

**This means:**
- You can test from anywhere (home, office, etc.)
- Don't need to be in London
- Don't need GPS/location permissions
- Routes will calculate from Charing Cross to your chosen destination

### Test Destinations to Try
1. **Buckingham Palace** - ~10 min from Charing Cross
2. **Tower of London** - ~20 min from Charing Cross
3. **British Museum** - ~8 min from Charing Cross
4. **King's Cross Station** - ~15 min from Charing Cross

---

## Troubleshooting

### Phone Can't Connect?

**1. Check WiFi**
- Mac and phone MUST be on the same WiFi network
- Check Mac WiFi: System Preferences → Network
- Check Phone WiFi: Settings → WiFi

**2. Check Firewall**
- Mac Firewall may block connections
- System Preferences → Security & Privacy → Firewall
- Either disable temporarily OR add exception for Python

**3. Verify IP Address**
If `192.168.1.196` doesn't work, find correct IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**4. Try Different Port**
If port 8000 is blocked:
```bash
uvicorn server:app --host 0.0.0.0 --port 8080 --reload
```
Then visit: `http://192.168.1.196:8080/mobile`

---

## QR Code (Optional)

Generate QR code to scan from phone:

### Option 1: Online Generator
1. Go to https://qr.io/
2. Enter: `http://192.168.1.196:8000/mobile`
3. Scan with phone camera

### Option 2: Terminal (if you have qrencode)
```bash
brew install qrencode
echo "http://192.168.1.196:8000/mobile" | qrencode -t UTF8
```

---

## For Production (When Ready)

### Enable GPS Location
Edit `App/Web_App/static/mobile/js/tour_logic.js`:

**Change line 157 from:**
```javascript
let origin = TEST_START_LOCATION;
```

**To:**
```javascript
let origin = selectedDetails.currentLocation || TEST_START_LOCATION;
```

**And line 179 from:**
```javascript
start: TEST_START_LOCATION,
```

**To:**
```javascript
start: selectedDetails.currentLocation ? `${selectedDetails.currentLocation.lat},${selectedDetails.currentLocation.lng}` : TEST_START_LOCATION,
```

---

## Testing Checklist

### Landing Page
- [ ] Loads correctly on phone
- [ ] "Personalise ride" button works
- [ ] Yellow accent color visible
- [ ] No weird layout issues

### Destination Input
- [ ] Google Places autocomplete works
- [ ] Can type and select suggestions
- [ ] "Buckingham Palace" suggestion clickable
- [ ] Proceeds to route mode selection

### Route Mode
- [ ] Can select "Fastest"
- [ ] Can select "PassingBy"
- [ ] "Continue" button enables
- [ ] Yellow tag on PassingBy visible

### Tour Type (PassingBy Only)
- [ ] Grid layout looks good
- [ ] Can select tour type
- [ ] Bottom sheet slides up
- [ ] "Start Tour" button works

### Active Tour
- [ ] Map loads (may take a few seconds)
- [ ] Route renders from Charing Cross to destination
- [ ] Yellow polyline visible
- [ ] Landmark cards appear (swipeable)
- [ ] Can flip cards (tap to see description)
- [ ] Music and close buttons visible

---

## Known Issues

### Map Won't Load
- **Cause:** Missing Google Maps API key
- **Fix:** Check `.env` file has `GOOGLE_DIRECTIONS_KEY`

### No Landmarks Show
- **Cause:** API call failed
- **Check:** Server console for errors
- **Check:** Browser console (phone) for network errors

### Cards Don't Swipe
- **Cause:** Swiper.js not loading
- **Check:** Network tab, verify CDN is accessible

### "No destination found" Error
- **Cause:** localStorage not persisting
- **Fix:** Ensure browser allows localStorage
- **Fix:** Don't use private/incognito mode

---

## Sample Test Flow

1. **Start:** Open `http://192.168.1.196:8000/mobile` on phone
2. **Tap:** "Personalise ride"
3. **Select:** "Buckingham Palace" from suggestions
4. **Choose:** "PassingBy" mode
5. **Select:** "Royal" tour type
6. **Tap:** "Start Tour"
7. **Wait:** Map should load with route from Charing Cross → Buckingham Palace
8. **Swipe:** Through landmark cards
9. **Tap:** Card to flip and read description

**Expected Time:** ~2 minutes for full flow

---

## Server Access

**Your Network:**
- Mac IP: `192.168.1.196`
- Server Port: `8000`
- Full URL: `http://192.168.1.196:8000/mobile`

**Share with Others on Same WiFi:**
Anyone on your home WiFi can access the same URL from their phone!

---

**Status:** Ready for phone testing ✅
**Start Location:** Charing Cross, London (fixed for testing)
**GPS:** Disabled (for home testing)
