#!/usr/bin/env python3

import os
import sys
import struct
from PIL import Image
import io

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SCRIPT_DIR, '.windows')
DIST_DIR = os.path.join(SCRIPT_DIR, 'dist')

cursor_map = {
    'normal select': 'default',
    'alternate select': 'right_ptr',
    'text select': 'text',
    'help select': 'help',
    'link select': 'pointer',
    'location select': 'crosshair',
    'percision select': 'crosshair',
    'precision select': 'crosshair',
    'person select': 'pointer',
    'horizontal resize': 'size_hor',
    'vertical resize': 'size_ver',
    'diagonal resize 1': 'size_bdiag',
    'diagonal resize 2': 'size_fdiag',
    'move': 'dnd-move',
    'unavailable': 'not-allowed',
    'handwriting': 'text',
    'color-test': 'crosshair',
    'busy': 'progress',
    'working in background': 'progress',
}

missing_cursors = {
    # Standard cursors from source files
    'default': 'default',
    'pointer': 'pointer',
    'text': 'text',
    'help': 'help',
    'crosshair': 'crosshair',
    'dnd-move': 'dnd-move',
    'not-allowed': 'not-allowed',
    'right_ptr': 'right_ptr',
    'size_hor': 'size_hor',
    'size_ver': 'size_ver',
    'size_bdiag': 'size_bdiag',
    'size_fdiag': 'size_fdiag',
    'progress': 'progress',
    
    # Aliases for missing cursors
    'alias': 'pointer',
    'all-scroll': 'default',
    'arrow': 'default',
    'bd_double_arrow': 'size_hor',
    'bottom_left_corner': 'size_bdiag',
    'bottom_right_corner': 'size_bdiag',
    'bottom_side': 'size_ver',
    'bottom_tee': 'bottom_side',
    'cell': 'pointer',
    'center_ptr': 'default',
    'circle': 'not-allowed',
    'closedhand': 'dnd-move',
    'col-resize': 'size_hor',
    'color-picker': 'crosshair',
    'context-menu': 'pointer',
    'copy': 'pointer',
    'cross': 'crosshair',
    'cross_reverse': 'crosshair',
    'crossed_circle': 'not-allowed',
    'diamond_cross': 'crosshair',
    'dnd-ask': 'pointer',
    'dnd-copy': 'pointer',
    'dnd-link': 'pointer',
    'dnd-no-drop': 'not-allowed',
    'dnd-none': 'dnd-move',
    'dotbox': 'pointer',
    'double_arrow': 'size_all',
    'down-arrow': 'default',
    'draft': 'text',
    'draft_large': 'text',
    'draft_small': 'text',
    'e-resize': 'size_hor',
    'ew-resize': 'size_hor',
    'fleur': 'dnd-move',
    'forbidden': 'not-allowed',
    'grab': 'pointer',
    'grabbing': 'dnd-move',
    'hand': 'pointer',
    'h_double_arrow': 'size_hor',
    'half-busy': 'progress',
    'hand1': 'pointer',
    'hand2': 'pointer',
    'ibeam': 'text',
    'icon': 'pointer',
    'left-arrow': 'default',
    'left_ptr': 'default',
    'left_ptr_help': 'help',
    'left_ptr_watch': 'progress',
    'left_side': 'default',
    'left_tee': 'left_side',
    'link': 'pointer',
    'll_angle': 'bottom_left_corner',
    'lr_angle': 'bottom_right_corner',
    'move': 'dnd-move',
    'n-resize': 'size_ver',
    'ne-resize': 'top_right_corner',
    'nesw-resize': 'size_bdiag',
    'no-drop': 'not-allowed',
    'ns-resize': 'size_ver',
    'nw-resize': 'top_left_corner',
    'nwse-resize': 'size_fdiag',
    'openhand': 'pointer',
    'pencil': 'text',
    'pirate': 'not-allowed',
    'plus': 'crosshair',
    'pointer-move': 'dnd-move',
    'pointing_hand': 'pointer',
    'question_arrow': 'help',
    'right-arrow': 'default',
    'right_ptr': 'right_ptr',
    'right_side': 'default',
    'right_tee': 'right_side',
    'row-resize': 'size_ver',
    's-resize': 'size_ver',
    'sb_down_arrow': 'size_ver',
    'sb_h_double_arrow': 'size_hor',
    'sb_left_arrow': 'size_hor',
    'sb_right_arrow': 'size_hor',
    'sb_up_arrow': 'size_ver',
    'sb_v_double_arrow': 'size_ver',
    'se-resize': 'bottom_right_corner',
    'size_all': 'dnd-move',
    'split_h': 'col-resize',
    'split_v': 'row-resize',
    'sw-resize': 'bottom_left_corner',
    'target': 'crosshair',
    'tcross': 'crosshair',
    'top_left_arrow': 'default',
    'top_left_corner': 'size_bdiag',
    'top_right_corner': 'size_bdiag',
    'top_side': 'size_ver',
    'top_tee': 'top_side',
    'ul_angle': 'top_left_corner',
    'up-arrow': 'default',
    'ur_angle': 'top_right_corner',
    'v_double_arrow': 'size_ver',
    'vertical-text': 'text',
    'w-resize': 'size_hor',
    'wait': 'progress',
    'whats_this': 'help',
    'xterm': 'text',
    'X_cursor': 'crosshair',
    'zoom-in': 'crosshair',
    'zoom-out': 'crosshair',
}


def convert_cur(input_file, output_file):
    """Convert Windows .cur file to PNG with proper transparency."""
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Parse ICONDIR header
    reserved, icon_type, count = struct.unpack('<HHH', data[0:6])
    
    # Parse ICONDIRENTRY (use first cursor)
    entry = struct.unpack('<BBBBHHII', data[6:22])
    width, height, colors, reserved, planes, bpp, size, offset = entry
    
    # Handle 0 = 256
    width = width if width != 0 else 256
    height = height if height != 0 else 256
    
    # Parse BITMAPINFOHEADER
    bmp_header = struct.unpack('<IIIHHIIIIII', data[offset:offset+40])
    biSize, biWidth, biHeight, biPlanes, biBitCount = bmp_header[:5]
    
    # BMP height includes both XOR and AND mask - actual image is half
    actual_height = biHeight // 2
    
    # Pixel data starts after header
    pixel_offset = offset + 40
    
    if biBitCount == 32:
        # 32-bit: BGRA with alpha
        pixel_data = data[pixel_offset:pixel_offset + biWidth * actual_height * 4]
        
        # Flip vertically (BMP is bottom-up)
        flipped = bytearray(len(pixel_data))
        for y in range(actual_height):
            src_row = y * biWidth * 4
            dst_row = (actual_height - 1 - y) * biWidth * 4
            flipped[dst_row:dst_row + biWidth * 4] = pixel_data[src_row:src_row + biWidth * 4]
        
        # Convert BGRA to RGBA
        rgba = bytearray(len(flipped))
        for i in range(0, len(flipped), 4):
            rgba[i] = flipped[i + 2]      # R
            rgba[i + 1] = flipped[i + 1]  # G
            rgba[i + 2] = flipped[i]       # B
            rgba[i + 3] = flipped[i + 3]  # A
        
        img = Image.frombytes('RGBA', (biWidth, actual_height), bytes(rgba))
    elif biBitCount == 24:
        # 24-bit: BGR, no alpha
        pixel_data = data[pixel_offset:pixel_offset + biWidth * actual_height * 3]
        
        # Flip vertically
        flipped = bytearray(len(pixel_data))
        for y in range(actual_height):
            src_row = y * biWidth * 3
            dst_row = (actual_height - 1 - y) * biWidth * 3
            flipped[dst_row:dst_row + biWidth * 3] = pixel_data[src_row:src_row + biWidth * 3]
        
        # Convert BGR to RGB
        rgb = bytearray(len(flipped))
        for i in range(0, len(flipped), 3):
            rgb[i] = flipped[i + 2]      # R
            rgb[i + 1] = flipped[i + 1]  # G
            rgb[i + 2] = flipped[i]       # B
        
        img = Image.frombytes('RGB', (biWidth, actual_height), bytes(rgb))
        img = img.convert('RGBA')
    else:
        # Fallback to PIL
        img = Image.open(input_file)
        img = img.convert('RGBA')
    
    # Resize to 32x32
    if img.size != (32, 32):
        img = img.resize((32, 32), Image.LANCZOS)
    
    img.save(output_file, 'PNG')


def parse_ani(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    if not data.startswith(b'RIFF'):
        return []

    frames = []
    pos = 12

    while pos < len(data) - 8:
        chunk_id = data[pos:pos+4]
        chunk_size = struct.unpack('<I', data[pos+4:pos+8])[0]

        if chunk_id == b'LIST':
            list_type = data[pos+8:pos+12]
            if list_type == b'fram':
                frame_pos = pos + 12
                end_pos = pos + 8 + chunk_size
                while frame_pos < end_pos - 8:
                    frame_id = data[frame_pos:frame_pos+4]
                    frame_size = struct.unpack('<I', data[frame_pos+4:frame_pos+8])[0]

                    if frame_id == b'icon':
                        ico_data = data[frame_pos+8:frame_pos+8+frame_size]
                        
                        # Parse ICO header
                        reserved, icon_type, count = struct.unpack('<HHH', ico_data[0:6])
                        
                        # Parse first entry
                        entry = struct.unpack('<BBBBHHII', ico_data[6:22])
                        width, height, colors, reserved, planes, bpp, size, offset = entry
                        
                        # Handle 0 = 256
                        width = width if width != 0 else 256
                        height = height if height != 0 else 256
                        
                        # Parse BMP header
                        bmp_offset = offset
                        bmp = struct.unpack('<IIIHHIIIIII', ico_data[bmp_offset:bmp_offset+40])
                        biWidth, biHeight = bmp[1], bmp[2]
                        biBitCount = bmp[4]
                        
                        actual_height = biHeight // 2
                        pixel_offset = bmp_offset + 40
                        
                        if biBitCount == 32:
                            pixel_data = ico_data[pixel_offset:pixel_offset + width * actual_height * 4]
                            
                            # Flip vertically (BMP is bottom-up)
                            flipped = bytearray(len(pixel_data))
                            for y in range(actual_height):
                                src = y * width * 4
                                dst = (actual_height - 1 - y) * width * 4
                                flipped[dst:dst + width * 4] = pixel_data[src:src + width * 4]
                            
                            # BGRA to RGBA
                            rgba = bytearray(len(flipped))
                            for i in range(0, len(flipped), 4):
                                rgba[i] = flipped[i + 2]
                                rgba[i + 1] = flipped[i + 1]
                                rgba[i + 2] = flipped[i]
                                rgba[i + 3] = flipped[i + 3]
                            
                            img = Image.frombytes('RGBA', (width, actual_height), bytes(rgba))
                            frames.append(img)
                        
                    frame_pos += 8 + frame_size
                    if frame_size == 0:
                        break
        pos += 8 + chunk_size
        if chunk_size == 0:
            pos += 1

    return frames


def get_hotspot(frame):
    """Extract hotspot from cursor frame. Default to center-top for arrows."""
    # For most arrow cursors, hotspot is at the tip
    # Default to 4, 4 which is typical for arrow cursors
    return 4, 4


def build_variant(variant):
    variant_dir = os.path.join(SRC_DIR, variant)
    output_dir = os.path.join(DIST_DIR, f'zune-cursors-{variant}', 'cursors')

    if not os.path.exists(variant_dir):
        print(f"Error: {variant_dir} does not exist")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"Building {variant}...")

    for cur_file in os.listdir(variant_dir):
        if not cur_file.endswith('.cur') and not cur_file.endswith('.ani'):
            continue

        input_path = os.path.join(variant_dir, cur_file)
        base_name = os.path.splitext(cur_file)[0]

        linux_name = None
        for win_name, ln_name in cursor_map.items():
            if win_name.lower() in base_name.lower():
                linux_name = ln_name
                break

        if not linux_name:
            print(f"  Warning: No mapping for {cur_file}")
            continue

        if cur_file.endswith('.cur'):
            # Convert to PNG first
            temp_png = os.path.join(output_dir, f'{linux_name}_temp.png')
            print(f"  Converting {cur_file} -> {linux_name}")
            convert_cur(input_path, temp_png)
            
            # Determine hotspot (for arrow cursors, typically 4,4)
            hx, hy = 4, 4
            
            # Compile with xcursorgen
            cursor_path = os.path.join(output_dir, linux_name)
            try:
                import subprocess
                # Create config file for xcursorgen
                config = f"32 {hx} {hy} {linux_name}_temp.png 0\n"
                config_path = os.path.join(output_dir, f'{linux_name}.in')
                with open(config_path, 'w') as f:
                    f.write(config)
                
                subprocess.run(
                    ['xcursorgen', os.path.basename(config_path), os.path.basename(cursor_path)],
                    cwd=output_dir,
                    check=True
                )
                # Clean up temp files
                os.remove(config_path)
                os.remove(temp_png)
                print(f"    -> Compiled {linux_name}")
            except Exception as e:
                print(f"    -> Failed to compile: {e}, keeping PNG")
                # Rename temp to final if compilation failed
                final_png = os.path.join(output_dir, f'{linux_name}.png')
                if os.path.exists(final_png):
                    os.remove(final_png)
                os.rename(temp_png, final_png)

        elif cur_file.endswith('.ani'):
            print(f"  Converting {cur_file} -> {linux_name} (animated)")
            frames = parse_ani(input_path)
            if frames:
                # Get frame delay from ANI header (default to 40ms)
                frame_delay = 40
                
                # Save all frames as PNG
                for i, frame in enumerate(frames):
                    if frame.mode == 'P':
                        frame = frame.convert('RGBA')
                    if frame.size != (32, 32):
                        frame = frame.resize((32, 32), Image.LANCZOS)
                    output_path = os.path.join(output_dir, f'{linux_name}_{i:02d}.png')
                    frame.save(output_path, 'PNG')
                
                # Create config file for xcursorgen
                hotspot_x, hotspot_y = get_hotspot(frames[0])
                config_path = os.path.join(output_dir, f'{linux_name}.in')
                with open(config_path, 'w') as f:
                    for i in range(len(frames)):
                        f.write(f"32 {hotspot_x} {hotspot_y} {linux_name}_{i:02d}.png {frame_delay}\n")
                
                # Compile with xcursorgen
                cursor_path = os.path.join(output_dir, linux_name)
                try:
                    import subprocess
                    subprocess.run(
                        ['xcursorgen', os.path.basename(config_path), os.path.basename(cursor_path)],
                        cwd=output_dir,
                        check=True
                    )
                    # Clean up config file and frame PNGs
                    os.remove(config_path)
                    for i in range(len(frames)):
                        os.remove(os.path.join(output_dir, f'{linux_name}_{i:02d}.png'))
                    print(f"    -> Created animated cursor with {len(frames)} frames")
                except FileNotFoundError:
                    print(f"    -> xcursorgen not found, using static image")
                except subprocess.CalledProcessError as e:
                    print(f"    -> xcursorgen failed (return code {e.returncode}), using static image")
            else:
                print(f"  Warning: Could not extract frames from {cur_file}")


def create_symlinks(variant):
    output_dir = os.path.join(DIST_DIR, f'zune-cursors-{variant}', 'cursors')
    print(f"Creating symlinks for {variant}...")

    created = 0
    for to_name, from_name in missing_cursors.items():
        # Check for animated cursor first (no extension), then PNG
        from_path_no_ext = os.path.join(output_dir, from_name)
        from_path_png = os.path.join(output_dir, f"{from_name}.png")
        to_path = os.path.join(output_dir, to_name)
        
        # Skip if target already exists (file or symlink)
        if os.path.exists(to_path):
            continue
        # If source exists without extension (animated cursor)
        if os.path.exists(from_path_no_ext):
            os.symlink(from_name, to_path)
            created += 1
        # Otherwise try with .png extension
        elif os.path.exists(from_path_png):
            os.symlink(f"{from_name}.png", to_path)
            created += 1
    
    print(f"  Created {created} symlinks")


def create_index_theme(variant):
    output_dir = os.path.join(DIST_DIR, f'zune-cursors-{variant}')
    index_file = os.path.join(output_dir, 'index.theme')

    with open(index_file, 'w') as f:
        f.write('[Icon Theme]\n')
        f.write(f'Name=Zune Cursors - {variant}\n')
        f.write('Comment=A cursor theme inspired by Zune\n')

    print(f"Created index.theme for {variant}")


def show_usage():
    print("Usage: ./build.py [original|modified|all]")
    print("  original  - Build original variant only")
    print("  modified  - Build modified variant only")
    print("  all       - Build both variants (default)")


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if variant not in ['original', 'modified', 'all']:
        show_usage()
        sys.exit(1)

    os.makedirs(DIST_DIR, exist_ok=True)

    if variant in ['original', 'all']:
        build_variant('original')
        create_symlinks('original')
        create_index_theme('original')

    if variant in ['modified', 'all']:
        build_variant('modified')
        create_symlinks('modified')
        create_index_theme('modified')

    print(f"\nBuild complete! Cursor themes are in {DIST_DIR}/")


if __name__ == '__main__':
    main()
