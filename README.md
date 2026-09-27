# Wild Things Rescue: homepage mockups

Four homepage concepts for [Wild Things Rescue](https://wildthingsrescue.uk), Lincolnshire's largest wildlife rescue (registered charity 1190933).

| Mockup | Style | Taste skill? |
|---|---|---|
| [A: Meadow](mockups/a-meadow.html) | Warm, rounded, serif headlines | No |
| [B: Casebook](mockups/b-casebook.html) | Bold sticker style, interactive "What have you found?" helper | No |
| [C: Cinematic](mockups/c-cinematic.html) | Dark full-width hero, scroll animation | Yes |
| [D: Editorial](mockups/d-editorial.html) | Light editorial layout, stacking cards | Yes |

## Folders

- `mockups/` finished pages. Each is a single self-contained file (photos, fonts and scripts built in), so it opens offline. Open these to view.
- `src/` the editable versions. Make changes here, then rebuild.
- `src/img/` web-sized photos used by the pages.
- `generated/` full-size AI images made with Replicate (GPT Image 2.5 Flare and Sunburst).
- `tools/build.py` turns `src/` into `mockups/`.

## Rebuilding

After editing anything in `src/`:

```
pip install pillow
python3 tools/build.py
```

## Image notes

- Photos in `src/img/` (other than the ones listed below) belong to Wild Things Rescue and were taken from their current website. Keep this repo private unless they agree otherwise.
- `hero-wide.jpg` is an AI-extended version of their hedgehog photo. The whole image was redrawn, so for a live site use the original photo, widened properly.
- `centre-art.jpg` is an AI illustration, labelled "Artist's impression" wherever it appears.
- `hands.jpg` and the `st-*.webp` stickers are AI generated and don't show real patients.

## Copy to check before anyone else sees these

- The first-aid advice in A's steps and B's helper is general wildlife guidance, not from the charity. They should approve it.
- Some photo captions are invented ("Fox cub, doing well", "Hedgehog, pre-release", "Cygnet + teddy").
- D mentions collection, which comes from one Google review rather than the charity's own site.
