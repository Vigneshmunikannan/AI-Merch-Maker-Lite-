import json
import random
from datetime import datetime
import shutil

class ProductContentGenerator:
    def __init__(self):
        # Sample product data for demonstration
        self.sample_products = [
            {
                "title": "Vintage Sunset Graphic Tee",
                "description": "A nostalgic blend of retro aesthetics and modern comfort. This eye-catching t-shirt features a vibrant sunset design that captures the essence of golden hour. Perfect for casual outings, music festivals, or adding a pop of color to your wardrobe.",
                "tags": ["vintage", "retro", "sunset", "graphic", "comfortable", "casual", "trendy"],
                "image_prompt": "vintage sunset graphic design on t-shirt, warm colors, retro style"
            },
            {
                "title": "Minimalist Coffee Quote Mug",
                "description": "Start your morning right with this sleek, minimalist coffee mug featuring an inspiring quote. Made from high-quality ceramic, this mug is perfect for coffee lovers who appreciate clean design and motivational messages.",
                "tags": ["minimalist", "coffee", "quote", "ceramic", "morning", "motivation", "clean"],
                "image_prompt": "minimalist white coffee mug with simple black text quote"
            },
            {
                "title": "Space Galaxy Phone Case",
                "description": "Protect your phone in style with this stunning galaxy-themed case. Featuring deep space imagery with nebulas and stars, this case combines protection with cosmic beauty. Compatible with most phone models.",
                "tags": ["space", "galaxy", "phone case", "cosmic", "stars", "protection", "universe"],
                "image_prompt": "phone case with galaxy space design, stars and nebulas"
            }
        ]
    
    def generate_product_content(self, theme="random"):
        """
        Generate product content. In a real implementation, this would call OpenAI API.
        For demo purposes, we'll use pre-defined samples.
        """
        print("Generating product content with AI...")
        
        # Simulate API call delay
        import time
        time.sleep(1)
        
        # Select random product or based on theme
        if theme == "random" or theme not in ["vintage", "minimalist", "space"]:
            product = random.choice(self.sample_products)
        else:
            # Find product matching theme
            matching_products = [p for p in self.sample_products if theme in p["tags"]]
            product = matching_products[0] if matching_products else self.sample_products[0]
        
        print(f"Generated product: {product['title']}")
        return product
    
    def generate_product_image(self, image_prompt):
        """
        Generate product image. In real implementation, this would call DALL-E API.
        For demo, we'll copy a sample image.
        """
        print("Generating product image with DALL-E...")
        
        # Simulate API call
        import time
        time.sleep(2)
        
        # Copy sample image (simulating generated image)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"product_{timestamp}.jpg"
        
        try:
            # Copy sample image to simulate generated image
            shutil.copy("sample_image.jpg", image_filename)
            print(f"Image generated: {image_filename}")
        except FileNotFoundError:
            # Create a placeholder if sample image doesn't exist
            print("Sample image not found, creating placeholder")
            image_filename = "placeholder_image.jpg"
        
        return image_filename
    
    def create_product_package(self, theme="random"):
        """Create complete product package"""
        print("=" * 50)
        print("STARTING PRODUCT GENERATION")
        print("=" * 50)
        
        # Generate content
        content = self.generate_product_content(theme)
        
        # Generate image
        image_file = self.generate_product_image(content["image_prompt"])
        
        # Create product data package
        product_data = {
            "id": f"prod_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": content["title"],
            "description": content["description"],
            "tags": content["tags"],
            "image_file": image_file,
            "image_prompt": content["image_prompt"],
            "created_at": datetime.now().isoformat(),
            "theme": theme,
            "price": round(19.99 + random.uniform(5, 25), 2)
        }
        
        # Save to JSON file
        output_file = f"product_data_{product_data['id']}.json"
        with open(output_file, 'w') as f:
            json.dump(product_data, f, indent=2)
        
        print(f"Product data saved: {output_file}")
        print("PRODUCT GENERATION COMPLETED")
        return product_data, output_file

# CLI usage
if __name__ == "__main__":
    import sys
    theme = sys.argv[1] if len(sys.argv) > 1 else "random"
    
    generator = ProductContentGenerator()
    product, file = generator.create_product_package(theme)
    print(f"\nProduct created: {product['title']}")
    print(f"Price: ${product['price']}")
    print(f"Data file: {file}")
