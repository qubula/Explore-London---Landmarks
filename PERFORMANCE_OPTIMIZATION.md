# Performance Optimization Guide

## Current Bottlenecks (Analysis)

### 1. **Google Directions API Calls** (Biggest bottleneck)
- **Current:** ~2-3 seconds per API call
- **Impact:** 2 calls = 4-6 seconds minimum wait time
- **Cost:** Free tier = 40,000 requests/month

### 2. **Landmark Database Processing**
- **Current:** Loading 12,000 landmarks (1.7MB JSON) on every import
- **Impact:** ~500ms on Railway servers (slower than local)
- **Line 32 in route_landmark_finder.py:** `landmarks = load_landmarks()` runs at module import

### 3. **Distance Calculations**
- **Current:** Computing geodesic distance for thousands of landmarks
- **Impact:** ~1-2 seconds for scenic route analysis
- **Location:** `grand_landmarks_near_route()` in landmarks.py

---

## Optimization Strategies (Ranked by Impact)

### 🚀 HIGH IMPACT (70-80% faster)

#### 1. **Caching with Redis** (Best for production)
Cache API responses and route calculations.

**Setup:**
```bash
# Add to requirements.txt
redis
```

**Implementation:**
```python
# App/cache.py
import redis
import json
import os
from functools import wraps

# Railway auto-provides REDIS_URL when you add Redis
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def cache_route(timeout=3600):  # 1 hour cache
    def decorator(func):
        @wraps(func)
        def wrapper(start, end, *args, **kwargs):
            cache_key = f"route:{start}:{end}:{args}:{kwargs}"

            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Not in cache, compute it
            result = func(start, end, *args, **kwargs)

            # Store in cache
            redis_client.setex(cache_key, timeout, json.dumps(result))
            return result
        return wrapper
    return decorator

# In planner.py:
from App.cache import cache_route

@cache_route(timeout=3600)
def get_route_and_duration(start: str, end: str):
    # existing code...
```

**Benefits:**
- Repeat queries = instant (0.01s instead of 3s)
- Reduces Google API costs
- Railway has free Redis addon

**Drawbacks:**
- Adds complexity
- Requires Redis server

---

#### 2. **Pre-filter Landmarks by Geographic Bounds** (Easiest win)
Don't process ALL 12,000 landmarks. Filter by bounding box first.

**Implementation:**
```python
# App/landmarks.py - Add this function
def get_route_bounds(route_points, buffer_km=1.0):
    """
    Get min/max lat/lon of route with buffer.
    buffer_km: how many km beyond route to include landmarks
    """
    lats = [p[0] for p in route_points]
    lons = [p[1] for p in route_points]

    # ~0.009 degrees ≈ 1km at London's latitude
    buffer_deg = buffer_km * 0.009

    return {
        "min_lat": min(lats) - buffer_deg,
        "max_lat": max(lats) + buffer_deg,
        "min_lon": min(lons) - buffer_deg,
        "max_lon": max(lons) + buffer_deg,
    }

def grand_landmarks_near_route(route_points, radius_m=600):
    bounds = get_route_bounds(route_points, buffer_km=1.0)

    # Filter landmarks BEFORE distance calculations
    candidates = []
    for lm in list_grand_landmarks():
        lat = lm.get("lat")
        lon = lm.get("lng") or lm.get("lon")

        # Quick bounds check (fast!)
        if (bounds["min_lat"] <= lat <= bounds["max_lat"] and
            bounds["min_lon"] <= lon <= bounds["max_lon"]):
            candidates.append(lm)

    # Now only compute geodesic distance for candidates (10-20% of total)
    result = []
    for lm in candidates:
        # existing distance calculation code...
```

**Benefits:**
- Reduces landmarks from 12,000 → ~500-1,000 (90% reduction!)
- No external dependencies
- 1-2 second improvement

**Drawbacks:**
- None! Always do this.

---

#### 3. **Lazy Load Landmarks** (Simple fix)
Don't load landmarks until needed.

**Current problem:**
```python
# Line 32 in route_landmark_finder.py
landmarks = load_landmarks()  # Loads on module import
```

**Fix:**
```python
# route_landmark_finder.py
_landmarks_cache = None

def get_landmarks():
    global _landmarks_cache
    if _landmarks_cache is None:
        _landmarks_cache = load_landmarks()
    return _landmarks_cache

# Then everywhere: use get_landmarks() instead of landmarks
```

**Benefits:**
- Mode 1 (Fastest) no longer loads landmarks at all
- Saves 500ms per request

---

### ⚡ MEDIUM IMPACT (30-50% faster)

#### 4. **Use Faster Distance Calculation**
Replace `geopy.distance.geodesic` with Haversine formula (faster approximation).

**Implementation:**
```python
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Fast distance calculation (meters).
    ~10x faster than geodesic, <0.5% error for short distances.
    """
    R = 6371000  # Earth radius in meters

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c
```

**Benefits:**
- 10x faster than geodesic
- No external dependencies
- Accurate enough for London (<500m distances)

**Replace everywhere you see:**
```python
# OLD
from geopy.distance import geodesic
d = geodesic((lat1, lon1), (lat2, lon2)).meters

# NEW
d = haversine_distance(lat1, lon1, lat2, lon2)
```

---

#### 5. **Parallel API Calls**
Make Google API calls in parallel using `asyncio`.

**Implementation:**
```python
import asyncio
import aiohttp

async def async_get_route(session, start, end, mode):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": start,
        "destination": end,
        "mode": "driving",
        "alternatives": "true" if mode == "2" else "false",
        "key": GOOGLE_API_KEY,
    }
    async with session.get(url, params=params) as response:
        return await response.json()

async def plan_routes_parallel(start, end):
    """Fetch fastest AND scenic routes in parallel."""
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            async_get_route(session, start, end, "1"),
            async_get_route(session, start, end, "2"),
        )
    return results[0], results[1]  # fastest, scenic
```

**Benefits:**
- 2 API calls in 3 seconds instead of 6 seconds
- 50% time reduction for initial form

**Drawbacks:**
- Requires `aiohttp` dependency
- More complex async code

---

### 🔧 LOW IMPACT (10-20% faster)

#### 6. **Use ujson instead of json**
Faster JSON parsing.

```bash
# requirements.txt
ujson

# route_landmark_finder.py
import ujson as json  # Drop-in replacement
```

**Benefits:**
- 2-3x faster JSON parsing
- ~100-200ms improvement

---

#### 7. **Compress Landmark Database**
Use MessagePack instead of JSON.

```bash
pip install msgpack
python -c "import json, msgpack; data=json.load(open('Data/final_landmarks_v6.2_Big.json')); open('Data/landmarks.msgpack', 'wb').write(msgpack.packb(data))"
```

**Benefits:**
- Smaller file (1.7MB → ~1.0MB)
- Faster loading (~40% faster)

---

## Recommended Implementation Order

### Phase 1: Quick Wins (30 minutes)
1. ✅ **Pre-filter by bounds** (strategy #2) - Add to `landmarks.py`
2. ✅ **Lazy load landmarks** (strategy #3) - Modify `route_landmark_finder.py`
3. ✅ **Haversine distance** (strategy #4) - Replace `geodesic` calls

**Expected improvement:** 2-3 seconds faster (50% reduction)

### Phase 2: Caching (1 hour)
4. 🔴 **Add Redis caching** (strategy #1) - New `cache.py` file

**Expected improvement:** Repeat queries = instant

### Phase 3: Advanced (Optional)
5. ⚙️ **Parallel API calls** (strategy #5) - Refactor `planner.py`
6. ⚙️ **ujson** (strategy #6) - One-line change

---

## Cost-Benefit Analysis

| Strategy | Time to Implement | Speed Improvement | Complexity | Recommended |
|----------|------------------|-------------------|------------|-------------|
| Bounds pre-filter | 15 min | 40-50% | Low | ✅ YES |
| Lazy loading | 10 min | 20-30% | Low | ✅ YES |
| Haversine distance | 20 min | 15-25% | Low | ✅ YES |
| Redis caching | 1 hour | 80% (repeat) | Medium | ✅ YES |
| Parallel API calls | 1 hour | 30-40% | High | ⚠️ Maybe |
| ujson | 5 min | 5-10% | Low | ✅ YES |

---

## Measuring Performance

Add timing logs to see improvements:

```python
import time

def plan_route(start, end, mode, chosen_landmarks=None):
    t0 = time.time()

    # ... existing code ...

    print(f"[PERF] plan_route mode={mode} took {time.time()-t0:.2f}s")
    return result
```

Check Railway logs to see before/after times.

---

## Alternative: Use a Faster Hosting Provider

Railway is convenient but not the fastest. Consider:

- **Render.com** - Similar free tier, slightly faster
- **Fly.io** - Better CPU performance, free tier
- **DigitalOcean App Platform** - $5/month, much faster servers
- **AWS Lambda** (advanced) - Serverless, pay per request

**Reality check:** Your bottleneck is Google API calls (3s), not server speed (0.5s). Better hosting saves 200-300ms max.

---

## Questions to Consider

1. **How often are routes repeated?** If users rarely search the same routes, caching helps less.
2. **Is 5-8 seconds acceptable?** For a prototype/personal project, maybe optimization isn't needed yet.
3. **What's your budget?** Redis caching requires Railway Pro ($5/month after trial).

---

**Bottom line:** Implementing Phase 1 (bounds filter + lazy loading + Haversine) will make the biggest immediate impact with minimal complexity.
