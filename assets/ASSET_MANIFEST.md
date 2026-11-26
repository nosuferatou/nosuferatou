# Third-Party Game Asset Manifest & Licenses

All external pixel-art game assets incorporated into the GitHub Aquarium are verified under public domain or permissive open-source licenses (CC0 1.0 Universal).

---

## 1. Underwater Diving Pack
- **Author**: Luis Zuno (@ansimuz)
- **Source**: [OpenGameArt.org](https://opengameart.org/content/underwater-diving-pack) & [ansimuz.itch.io](https://ansimuz.itch.io/underwater-diving)
- **License**: Creative Commons Zero v1.0 Universal (CC0)
- **Notice**: Public domain and free to use on personal or commercial projects.
- **Files Used**:
  - `sub_bg.png` (Deep ocean gradient background)
  - `sub_mid.png` (Distant submerged coral ridge midground)
  - `coral_1.png` - `coral_5.png` (Handcrafted pixel-art rock formations and large coral reefs)
  - `plant_1.png`, `plant_2.png`, `plant_3_*.png` (Aquatic flora, kelp fronds, sea anemones)
  - `big_fish_*.png`, `dart_fish_*.png`, `def_fish_1.png` (Detailed species sprites & secondary schooling fish)
  - `jelly_fish_*.png` (Pixel-art translucent jellyfish)

---

## 2. Fish Pack
- **Author**: Kenney (Kenney.nl)
- **Source**: [OpenGameArt.org](https://opengameart.org/content/fish-pack-0) & [Kenney.nl](https://kenney.nl/assets/fish-pack)
- **License**: Creative Commons Zero v1.0 Universal (CC0)
- **Notice**: Public domain, free for any project, commercial or personal.
- **Files Used**:
  - `kenney_fish_blue.png`, `kenney_fish_orange.png`, `kenney_fish_green.png`, `kenney_fish_brown.png`, `kenney_fish_red.png`
  - `kenney_bubble_a.png`, `kenney_bubble_b.png`
  - `kenney_rock_a.png`, `kenney_rock_b.png`
  - `kenney_seaweed_green_a.png`, `kenney_seaweed_orange_a.png`

---

## 3. Hero Fish Artwork
- **Artwork**: Original hand-authored sprites in `scripts/pixel_species.py`; no third-party hero-fish art used.
- **Visual reference**: Weenifer, [Le Fisheee Tuurn Around](https://www.artstation.com/artwork/g0nlZQ). Reference only; no source pixels or artwork copied.
- **Rendering**: Pillow nearest-neighbor scaling, crisp silhouette, restrained softened outer glow.

## 4. Pixel-Art Harmonization & Color Grading
- Sprites render with Python Pillow and nearest-neighbor point filtering (`Image.Resampling.NEAREST`) to preserve crisp pixels and the existing deep-ocean palette.
