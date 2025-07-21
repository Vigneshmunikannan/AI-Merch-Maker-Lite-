import subprocess
import json
import time
import requests
from datetime import datetime
import os

class PipelineOrchestrator:
    def __init__(self, java_server_url="http://localhost:8080"):
        self.java_server_url = java_server_url
        self.results = []
    
    def check_server_health(self):
        """Check if Java server is running"""
        try:
            response = requests.get(f"{self.java_server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_complete_pipeline(self, theme="random"):
        """Execute the complete pipeline"""
        print("🚀 STARTING AI MERCH MAKER LITE PIPELINE")
        print("=" * 60)
        print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Theme: {theme}")
        print("=" * 60)
        
        pipeline_start = time.time()
        
        try:
            # Step 1: Generate Product Content (Python)
            print("\n📝 STEP 1: PRODUCT CONTENT GENERATION")
            print("-" * 40)
            product_data, product_file = self.run_product_generation(theme)
            if not product_data:
                raise Exception("Product generation failed")
            
            # Step 2: Create Mockup (JavaScript)
            print("\n🎨 STEP 2: MOCKUP GENERATION")
            print("-" * 40)
            mockup_data = self.run_mockup_generation(product_file)
            if not mockup_data:
                raise Exception("Mockup generation failed")
            
            # Step 3: Check Java Server
            print("\n🔍 STEP 3: SERVER HEALTH CHECK")
            print("-" * 40)
            if not self.check_server_health():
                print("⚠️ Java server not running. Please start it first:")
                print("   cd java && java ProductPublisher")
                raise Exception("Java server not available")
            print("✅ Java server is running")
            
            # Step 4: Publish Product (Java API)
            print("\n📤 STEP 4: PRODUCT PUBLISHING")
            print("-" * 40)
            publish_result = self.publish_product(product_data)
            if not publish_result:
                raise Exception("Product publishing failed")
            
            # Calculate total time
            total_time = time.time() - pipeline_start
            
            # Success summary
            print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"⏱️  Total execution time: {total_time:.2f} seconds")
            print(f"🆔 Product ID: {publish_result.get('product_id', 'N/A')}")
            print(f"🏷️  Product: {product_data['title']}")
            print(f"💰 Price: ${product_data.get('price', 'N/A')}")
            print(f"🔗 Product URL: {publish_result.get('product_url', 'N/A')}")
            print("=" * 60)
            
            # Save pipeline results
            pipeline_result = {
                "success": True,
                "execution_time": total_time,
                "product_data": product_data,
                "mockup_data": mockup_data,
                "publish_result": publish_result,
                "completed_at": datetime.now().isoformat()
            }
            
            with open(f"pipeline_result_{product_data['id']}.json", 'w') as f:
                json.dump(pipeline_result, f, indent=2)
            
            return pipeline_result
            
        except Exception as e:
            print(f"\n❌ PIPELINE FAILED: {str(e)}")
            return None
    
    def run_product_generation(self, theme):
        """Execute Python product generation"""
        try:
            # Run Python script
            result = subprocess.run([
                'python', 'python/product_generator.py', theme
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                return None, None
            
            # Find the generated product file
            import glob
            product_files = glob.glob("product_data_*.json")
            if not product_files:
                print("❌ No product data file found")
                return None, None
            
            latest_file = max(product_files, key=os.path.getctime)
            
            # Load product data
            with open(latest_file, 'r') as f:
                product_data = json.load(f)
            
            print(f"✅ Product generated: {product_data['title']}")
            return product_data, latest_file
            
        except subprocess.TimeoutExpired:
            print("❌ Product generation timed out")
            return None, None
        except Exception as e:
            print(f"❌ Error in product generation: {str(e)}")
            return None, None
    
    def run_mockup_generation(self, product_file):
        """Execute JavaScript mockup generation"""
        try:
            # Run Node.js script
            result = subprocess.run([
                'node', 'javascript/mockup_generator.js', product_file
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                return None
            
            # Find mockup data file
            import glob
            mockup_files = glob.glob("mockup_data_*.json")
            if not mockup_files:
                print("❌ No mockup data file found")
                return None
            
            latest_mockup = max(mockup_files, key=os.path.getctime)
            
            # Load mockup data
            with open(latest_mockup, 'r') as f:
                mockup_data = json.load(f)
            
            print(f"✅ Mockup generated: {mockup_data['result']['product_type']}")
            return mockup_data
            
        except subprocess.TimeoutExpired:
            print("❌ Mockup generation timed out")
            return None
        except Exception as e:
            print(f"❌ Error in mockup generation: {str(e)}")
            return None
    
    def publish_product(self, product_data):
        """Publish product to Java server"""
        try:
            # Prepare product data for publishing
            publish_data = {
                "id": product_data["id"],
                "title": product_data["title"],
                "description": product_data["description"],
                "tags": product_data["tags"],
                "image_file": product_data["image_file"],
                "price": product_data.get("price", 19.99)
            }
            
            # Send to Java server
            response = requests.post(
                f"{self.java_server_url}/publish",
                json=publish_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Product published with ID: {result['product_id']}")
                return result
            else:
                print(f"❌ Publishing failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ Error publishing product: {str(e)}")
            return None
    
    def schedule_daily_run(self, theme="random"):
        """Simulate daily scheduling"""
        print("🕐 DAILY SCHEDULER SIMULATION")
        print("=" * 40)
        print("In production, this would:")
        print("1. Run pipeline every 24 hours")
        print("2. Handle errors and retries")
        print("3. Send notifications")
        print("4. Generate reports")
        print("\nFor demo, running once...")
        print("=" * 40)
        
        return self.run_complete_pipeline(theme)

def main():
    import sys
    
    # Parse command line arguments
    theme = sys.argv[1] if len(sys.argv) > 1 else "random"
    mode = sys.argv[2] if len(sys.argv) > 2 else "once"
    
    orchestrator = PipelineOrchestrator()
    
    if mode == "schedule":
        result = orchestrator.schedule_daily_run(theme)
    else:
        result = orchestrator.run_complete_pipeline(theme)
    
    if result:
        print(f"\n✅ Pipeline execution completed successfully!")
    else:
        print(f"\n❌ Pipeline execution failed!")

if __name__ == "__main__":
    main()
