# Alfie Mobile App - Design System

**Accent Color:** `#f5e236` (Yellow)
**Style:** Bold, Clean, Map-First

## 1. Colors

### Primary
- **Accent Yellow:** `#f5e236` (Primary Buttons, Active States, Highlights)
- **Accent Hover:** `#E5D225` (Darker yellow for interaction)
- **Text on Accent:** `#000000` (Always use black text on yellow for contrast)

### Neutrals
- **Background:** `#F5F5F5` (Light Grey/White smoke) or User's Map style.
- **Card Background:** `#FFFFFF` (White)
- **Text Main:** `#1A1A1A` (Near Black)
- **Text Secondary:** `#6B7280` (Dark Grey)
- **Text Muted:** `#9CA3AF` (Light Grey)
- **Border/Divider:** `#E5E7EB` (Very Light Grey)

## 2. Typography

**Font:** Satoshi (Variable)

### Hierarchy
- **Display/Headings:** Bold (700), Tight spacing. Black.
- **Body:** Regular (400) or Medium (500). Dark Grey.
- **Labels/Buttons:** Semibold (600). Black (on yellow) or Dark Grey (on white).

| Style | Weight | Size | Use |
| :--- | :--- | :--- | :--- |
| **Heading 1** | 700 (Bold) | 24-28px | Main titles, ETA |
| **Heading 2** | 600 (Semi) | 20px | Section headers |
| **Body** | 400 (Reg) | 16px | Main content |
| **Small** | 500 (Med) | 14px | Subtitles, Hints |
| **Button** | 600 (Semi) | 16-18px | CTAs |

## 3. Components

### Buttons
**Primary (Yellow Pill)**
- Background: `#f5e236`
- Text: Black `#000000` (Bold 600)
- Radius: Full pill shape (`9999px`)
- Padding: 16px 32px
- Shadow: Soft, subtle (e.g., `0 4px 12px rgba(245, 226, 54, 0.4)`)

**Secondary / Ghost**
- Background: Transparent or White
- Border: 1px Solid `#E5E7EB` (optional)
- Text: Black
- Radius: 12px

### Cards
- **Background:** White
- **Radius:** 24px (Large rounded corners)
- **Shadow:** Standard drop shadow (`0 4px 20px rgba(0,0,0,0.08)`)
- **Padding:** 20-24px

### Active States (Toggles/Input Focus)
- **Active Color:** `#f5e236`
- **Focus Ring:** 3px ring of `#f5e236` with 30% opacity

## 4. Layout & Spacing
- **Map Coverage:** High (~80%). Maps are the hero.
- **Cards:** Floating bottom sheets or overlays.
- **Padding:** Minimum 16px edges. Internal card padding 24px.
- **Safe Areas:** Respect iOS Home indicator and Notch.
