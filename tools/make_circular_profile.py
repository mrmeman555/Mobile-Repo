#!/usr/bin/env python3
"""
Make Circular Profile Image

This script removes the white background from an image and crops it
to a perfect circle, ideal for Reddit profile pictures.

Usage:
    python make_circular_profile.py input_image.png [output_image.png]
    
    # To keep black background and only remove white:
    python make_circular_profile.py input_image.png --keep-black
"""

from PIL import Image, ImageDraw, ImageFilter
import sys
import os
import numpy as np


def remove_white_background(image, threshold=240):
    """
    Remove white/near-white background and make it transparent.
    
    Args:
        image: PIL Image object
        threshold: Pixel values above this (for all R,G,B) are considered white
    
    Returns:
        PIL Image with transparent background
    """
    # Convert to RGBA if not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Get pixel data
    pixels = image.load()
    width, height = image.size
    
    # Make white pixels transparent
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            # If pixel is white or near-white, make it transparent
            if r > threshold and g > threshold and b > threshold:
                pixels[x, y] = (r, g, b, 0)  # Set alpha to 0
    
    return image


def remove_white_background_smart(image, threshold=240):
    """
    Smart removal of white background - only removes the outer white area,
    preserving any internal colors including black parts of the design.
    Uses flood fill from corners/edges.
    
    Args:
        image: PIL Image object
        threshold: Pixel values above this (for all R,G,B) are considered white
    
    Returns:
        PIL Image with transparent background
    """
    # Convert to RGBA if not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    pixels = image.load()
    
    # Create a visited set for flood fill
    to_make_transparent = set()
    visited = set()
    queue = []
    
    # Start from all edge pixels that are white
    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))
    
    # Flood fill from edges
    while queue:
        x, y = queue.pop(0)
        
        if (x, y) in visited:
            continue
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
            
        visited.add((x, y))
        
        r, g, b, a = pixels[x, y]
        
        # If pixel is white/near-white, mark for transparency and continue flood
        if r > threshold and g > threshold and b > threshold:
            to_make_transparent.add((x, y))
            # Add neighbors
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))
    
    # Make the outer white pixels transparent
    for x, y in to_make_transparent:
        r, g, b, a = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
    
    return image


def find_content_bounds(image):
    """
    Find the bounding box of non-transparent content.
    
    Returns:
        Tuple of (left, top, right, bottom)
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    pixels = image.load()
    width, height = image.size
    
    min_x, min_y = width, height
    max_x, max_y = 0, 0
    
    for y in range(height):
        for x in range(width):
            if pixels[x, y][3] > 0:  # If pixel is not fully transparent
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    return (min_x, min_y, max_x + 1, max_y + 1)


def crop_to_circle(image, output_size=400):
    """
    Crop the image to a perfect circle.
    
    Args:
        image: PIL Image with transparent background
        output_size: Size of the output square image (default 400x400, good for Reddit)
    
    Returns:
        PIL Image cropped to a circle
    """
    # Find the content bounds
    bounds = find_content_bounds(image)
    
    # Crop to content
    content = image.crop(bounds)
    content_width, content_height = content.size
    
    # Calculate the size needed for a square crop (use the larger dimension)
    size = max(content_width, content_height)
    
    # Create a new square image with transparent background
    square = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Paste the content centered
    x_offset = (size - content_width) // 2
    y_offset = (size - content_height) // 2
    square.paste(content, (x_offset, y_offset))
    
    # Resize to output size
    square = square.resize((output_size, output_size), Image.Resampling.LANCZOS)
    
    # Create circular mask
    mask = Image.new('L', (output_size, output_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, output_size, output_size), fill=255)
    
    # Apply circular mask
    result = Image.new('RGBA', (output_size, output_size), (0, 0, 0, 0))
    result.paste(square, (0, 0))
    
    # Create final image with circular transparency
    final = Image.new('RGBA', (output_size, output_size), (0, 0, 0, 0))
    final.paste(result, mask=mask)
    
    return final


def process_image(input_path, output_path=None, size=400, white_threshold=240, smart_removal=True):
    """
    Main function to process an image into a circular profile picture.
    
    Args:
        input_path: Path to input image
        output_path: Path for output image (optional, defaults to input_circular.png)
        size: Output image size (default 400x400)
        white_threshold: Threshold for white detection (default 240)
        smart_removal: If True, only removes outer white area (preserves black in design)
                      If False, removes ALL white pixels
    
    Returns:
        Path to output image
    """
    # Generate output path if not provided
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_circular.png"
    
    # Load image
    print(f"Loading image: {input_path}")
    image = Image.open(input_path)
    print(f"Original size: {image.size}")
    
    # Remove white background
    if smart_removal:
        print("Removing outer white background (preserving design)...")
        image = remove_white_background_smart(image, threshold=white_threshold)
    else:
        print("Removing all white pixels...")
        image = remove_white_background(image, threshold=white_threshold)
    
    # Crop to circle
    print(f"Cropping to {size}x{size} circle...")
    result = crop_to_circle(image, output_size=size)
    
    # Save result
    result.save(output_path, 'PNG')
    print(f"Saved circular profile image to: {output_path}")
    
    return output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExample usage:")
        print("  python make_circular_profile.py spiral_image.png")
        print("  python make_circular_profile.py spiral_image.png output.png")
        print("  python make_circular_profile.py spiral_image.png --remove-all-white")
        print("\nOptions:")
        print("  --remove-all-white  Remove ALL white pixels (not just outer background)")
        print("                      Use this if your design doesn't have black parts")
        print("\nProgrammatic usage:")
        print("  from make_circular_profile import process_image")
        print("  process_image('input.png', 'output.png', size=500, white_threshold=230)")
        sys.exit(1)
    
    input_path = sys.argv[1]
    smart_removal = True
    output_path = None
    
    # Parse arguments
    args = sys.argv[2:]
    for arg in args:
        if arg == '--remove-all-white':
            smart_removal = False
        elif not arg.startswith('--'):
            output_path = arg
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    process_image(input_path, output_path, smart_removal=smart_removal)


if __name__ == "__main__":
    main()
