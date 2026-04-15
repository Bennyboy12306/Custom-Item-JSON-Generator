import os
import json
import argparse
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def get_namespace():
    """Get namespace from user input"""
    namespace = input("Enter your namespace: ").strip()
    if not namespace:
        print(f"{Colors.RED}Error: Namespace cannot be empty")
        exit(1)
    return namespace

def find_textures(namespace):
    """Find all PNG files in the textures/item directory recursively"""
    textures_path = Path(f"assets/{namespace}/textures/item")
    
    if not textures_path.exists():
        print(f"{Colors.RED}Error: Path '{textures_path}' does not exist")
        exit(1)
    
    textures = []
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(textures_path):
        for file in files:
            if file.endswith('.png'):
                # Get the relative path from textures/item/
                full_path = Path(root)
                relative_path = full_path.relative_to(textures_path)
                textures.append({
                    'filename': file,
                    'name': file.replace('.png', ''),
                    'relative_path': relative_path,
                    'full_path': full_path
                })
    
    return textures

def create_model_json(namespace, texture_info):
    """Create model JSON content"""
    # Build the texture path
    if texture_info['relative_path'] == Path('.'):
        texture_path = f"{namespace}:item/{texture_info['name']}"
        subfolder_path = ""
    else:
        subfolder_path = str(texture_info['relative_path']).replace(os.sep, '/')
        texture_path = f"{namespace}:item/{subfolder_path}/{texture_info['name']}"
    
    return {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": texture_path
        }
    }

def create_item_json(namespace, texture_info):
    """Create item JSON content"""
    # Build the model path
    if texture_info['relative_path'] == Path('.'):
        model_path = f"{namespace}:item/{texture_info['name']}"
    else:
        subfolder_path = str(texture_info['relative_path']).replace(os.sep, '/')
        model_path = f"{namespace}:item/{subfolder_path}/{texture_info['name']}"
    
    return {
        "model": {
            "type": "minecraft:model",
            "model": model_path
        }
    }

def generate_jsons(namespace, textures, verbose=False):
    """Generates all JSON files for the resource pack"""
    
    if not textures:
        print(f"{Colors.RED} Error: No textures found!")
        return
    
    models_created = 0
    items_created = 0
    models_skipped = 0
    items_skipped = 0
    
    for texture in textures:
        # Create model JSON
        model_dir = Path(f"assets/{namespace}/models/item") / texture['relative_path']
        model_dir.mkdir(parents=True, exist_ok=True)
        
        model_file = model_dir / f"{texture['name']}.json"

        # Skip if model file already exists
        if model_file.exists():
            if verbose:
                print(f"{Colors.YELLOW}Skipped (exists): {model_file}")
            models_skipped += 1
        else:
            model_content = create_model_json(namespace, texture)
            with open(model_file, 'w') as f:
                json.dump(model_content, f, indent=2)
            models_created += 1
            if verbose:
                print(f"{Colors.GREEN}Created: {model_file}")
        
        # Create item JSON (only in /assets/<namespace>/items/)
        items_dir = Path(f"assets/{namespace}/items")
        items_dir.mkdir(parents=True, exist_ok=True)
        
        item_file = items_dir / f"{texture['name']}.json"

        if item_file.exists():
            if verbose:
                print(f"{Colors.YELLOW}Skipped (exists): {item_file}")
            items_skipped += 1
        else:
            item_content = create_item_json(namespace, texture)
            with open(item_file, 'w') as f:
                json.dump(item_content, f, indent=2)
            items_created += 1
            if verbose:
                print(f"{Colors.GREEN}Created: {item_file}")
    
    if models_created > 0 or items_created > 0:
        print(f"{Colors.GREEN}Successfully created {models_created} model files and {items_created} item files!")
    if models_skipped > 0 or items_skipped > 0:
        print(f"{Colors.YELLOW}Skipped {models_skipped} model file(s) and {items_skipped} item files that already exist")

def main():
    parser = argparse.ArgumentParser(description="Custom Item JSON Generator")
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Enable verbose output')
    args = parser.parse_args()
    
    verbose = args.verbose

    print("=== Custom Item JSON Generator ===\n")
    
    namespace = get_namespace()
    if verbose:
        print(f"\nSearching for textures in: assets/{namespace}/textures/item/\n")
    
    textures = find_textures(namespace)
    
    if textures:
        
        print(f"Found {len(textures)} texture(s)")
        if verbose:
            for texture in textures:
                print(f"  - {texture['filename']} ({texture['relative_path']})")
        print()
        generate_jsons(namespace, textures, verbose)
    else:
        print(f"{Colors.RED}No PNG textures found in the textures/item directory!")
    
    print(f"{Colors.RESET}")

if __name__ == "__main__":
    main()
