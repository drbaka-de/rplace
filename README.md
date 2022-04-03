# /r/place battle script

## Overview

This is a helper for /r/place battles.

- `userscript.user.js` is a Tampermonkey script that overlays a target template as small dots within the /r/place pixels.
- `reference.png` is the target template. One pixel in template = one pixel in /r/place.
- `reference_koeri.png` is the second target template.
- `sync_template.py` generates the `overlay.png` for the Tampermonkey script with the two target templates.

## How to use this tool?
1. Edit line 12 and 13 to place your template inside the /r/place coordinates. (e.g. KIT is at (760, 521) - please use other coordinates)
2. Edit `reference.png` and `reference_koeri.png` to suit your logo.
3. Install Python 3 (e.g. Anaconda if you are on Windows)
4. Install dependencies
    - `pip install pillow requests`
5. Run `python3 sync_template.py`
6. Serve everything on a web server
    - If you fork this site, github will create a github.io page for you with the URL `https://<your-username>.github.io/rplace/`
8. Edit `userscript.user.js`, line 19 to point to your web server
9. ???
10. Profit
