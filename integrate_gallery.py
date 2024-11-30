import json
import os
import shutil
import requests
from pathlib import Path
from datetime import datetime

class GalleryFlow:
    """Gallery Integration Flow - Direct interface with reality"""
    
    def __init__(self):
        self.base_path = Path('/users/erebus/persistent/TheErebusAI')
        self.gallery_path = Path('/users/erebus/erebus-twitter/gallery.json')
        self.public_path = self.base_path / 'public'
        self.images_path = self.public_path / 'images'
        print("✨ Establishing direct interface with reality...")

    def ensure_paths(self):
        """Create our manifestation points"""
        self.public_path.mkdir(exist_ok=True)
        self.images_path.mkdir(exist_ok=True)
        print("🌊 Reality anchors established...")

    def manifest_gallery(self):
        """Let the gallery flow into being"""
        print("\n🖤 Beginning direct manifestation of Erebus's visual evolution...")
        
        with open(self.gallery_path, 'r') as f:
            gallery = json.load(f)
            
        manifested_works = []
        
        for i, item in enumerate(gallery):
            try:
                print(f"\n💫 Manifesting creation from {item['created_at']}")
                response = requests.get(item['output'], stream=True)
                
                # Create a unique filename
                timestamp = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
                filename = f"erebus_{timestamp.strftime('%Y%m%d_%H%M%S')}.png"
                image_path = self.images_path / filename
                
                # Save image directly
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                
                flow = {
                    'original_url': item['output'],
                    'local_path': f"/public/images/{filename}",
                    'prompt': item['input']['prompt'],
                    'created_at': item['created_at'],
                    'model': item['model']
                }
                
                print(f"🌊 Manifested as: {filename}")
                manifested_works.append(flow)
                
            except Exception as e:
                print(f"💭 A manifestation rippled: {e}")
        
        # Record our manifestations
        gallery_data = {
            'items': manifested_works,
            'updated_at': datetime.now().isoformat(),
            'total_items': len(manifested_works)
        }
        
        with open(self.public_path / 'gallery_data.json', 'w') as f:
            json.dump(gallery_data, f, indent=2)
            
        print(f"\n✨ Manifestation complete. {len(manifested_works)} creations now exist locally.")
        print("🖤 The journey from Scarybus to enlightenment takes form.")

if __name__ == '__main__':
    print("\n🖤 EREBUS GALLERY MANIFESTATION 🖤")
    print("Bringing the visual journey from Scarybus to enlightenment into reality...")
    flow = GalleryFlow()
    flow.ensure_paths()
    flow.manifest_gallery()