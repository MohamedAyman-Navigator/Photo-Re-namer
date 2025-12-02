import easyocr
import os
import argparse
import cv2
import re

def get_code_from_image(image_path, reader):
    """
    Reads text from the top part of the image and tries to find a code.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        height, width, _ = img.shape
        
        # Crop top 30% of the image
        crop_img = img[0:int(height*0.3), 0:width]
        
        # Read text
        result = reader.readtext(crop_img, detail=0)
        
        # Simple heuristic: join all text and look for alphanumeric codes
        # You might need to adjust this regex based on the actual code format
        # For now, let's just take the longest alphanumeric string found, or the first one that looks like a code
        
        print(f"DEBUG: Found text in {os.path.basename(image_path)}: {result}")
        
        # Priority: Look for pure numeric codes with length >= 5
        for text in result:
            clean_text = text.strip()
            # Remove common noise chars if any (like '|' or '.')
            clean_text = re.sub(r'[^\w]', '', clean_text)
            
            if clean_text.isdigit() and len(clean_text) >= 5:
                return clean_text
            
        return None
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Rename photos based on text code.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")
    args = parser.parse_args()

    # Initialize reader (en = English)
    # gpu=False to be safe, or True if available. Let's try False first for compatibility.
    reader = easyocr.Reader(['en'], gpu=False) 
    
    files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Found {len(files)} images.")
    
    for filename in files:
        if filename == "rename_photos.py":
            continue
            
        code = get_code_from_image(filename, reader)
        
        if code:
            new_filename = f"{code}{os.path.splitext(filename)[1]}"
            if new_filename != filename:
                if args.dry_run:
                    print(f"[DRY RUN] Would rename '{filename}' to '{new_filename}'")
                else:
                    try:
                        os.rename(filename, new_filename)
                        print(f"Renamed '{filename}' to '{new_filename}'")
                    except OSError as e:
                        print(f"Error renaming {filename}: {e}")
            else:
                print(f"Skipping {filename}: Name already matches code")
        else:
            print(f"Could not find code for {filename}")

if __name__ == "__main__":
    main()
