# zune-cursors

Custom cursors for linux desktop.

## dependencies

**There are no dependencies for installing the cursors, only building them.**

Dependencies for converting the .cur and .ani files within the `.windows` directory:

```bash
sudo apt install x11-apps python3-pil
```

## building

```bash
./build.py             # Build both variants
./build.py original    # Build only original variant
./build.py modified    # Build only modified variant
```

## installation

```bash
# User install (to ~/.icons/)
./install.sh

# Or specific variant
./install.sh original
./install.sh modified

# System-wide install (requires root)
sudo ./install.sh -s
```

To activate, open GNOME Tweaks or run:
```bash
gsettings set org.gnome.desktop.interface cursor-theme 'zune-cursors-original'
```

## cursor mappings

### Source Cursors (from Windows .cur/.ani files)

These are converted directly from the Windows source files:

| Source File | Linux Cursor |
|-------------|--------------|
| normal select.cur | default (left_ptr) |
| alternate select.cur | right_ptr |
| text select.cur | text |
| help select.cur | help |
| link select.cur | pointer |
| location select.cur | crosshair |
| horizontal resize.cur | size_hor |
| vertical resize.cur | size_ver |
| diagonal resize 1.cur | size_bdiag |
| diagonal resize 2.cur | size_fdiag |
| move.cur | dnd-move |
| unavailable.cur | not-allowed |
| busy.ani | progress (animated) |
| working in background.ani | progress (animated) |

### Aliases (missing cursors)

The following cursors are missing from the source and are aliased to the closest available cursor:

| Alias | Maps To |
|-------|---------|
| alias, arrow, left_ptr, top_left_arrow | default |
| pointer, link, copy, grab, hand, cell, context-menu, dnd-ask, dnd-link, dotbox, pointing_hand | pointer |
| text, ibeam, pencil, draft, draft_large, draft_small, vertical-text, xterm | text |
| crosshair, cross, cross_reverse, diamond_cross, color-picker, target, tcross, X_cursor, zoom-in, zoom-out, plus | crosshair |
| help, left_ptr_help, question_arrow, whats_this | help |
| dnd-move, fleur, move, size_all, pointer-move, grabbing | dnd-move |
| not-allowed, circle, crossed_circle, dnd-no-drop, no-drop, pirate, forbidden | not-allowed |
| right_ptr | right_ptr |
| size_hor, col-resize, bd_double_arrow, e-resize, ew-resize, h_double_arrow, sb_h_double_arrow, sb_left_arrow, sb_right_arrow, w-resize | size_hor |
| size_ver, n-resize, ns-resize, row-resize, s-resize, sb_down_arrow, sb_up_arrow, sb_v_double_arrow, v_double_arrow | size_ver |
| size_bdiag, bottom_left_corner, nw-resize, nesw-resize, top_left_corner, ul_angle, ll_angle | size_bdiag |
| size_fdiag, bottom_right_corner, ne-resize, nwse-resize, top_right_corner, ur_angle, lr_angle | size_fdiag |
| progress, wait, half-busy, left_ptr_watch, watch | progress |
| bottom_side, bottom_tee, top_side, top_tee | bottom_side/top_side |
| left_side, left_tee | left_side |
| right_side, right_tee | right_side |
| split_h | col-resize |
| split_v | row-resize |
| center_ptr | default |
| openhand, closedhand | dnd-move |

## copyright and license

Copyright (c) 2026 Mark Edward under the MIT license.
