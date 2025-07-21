const fs = require('fs');

class MockupGenerator {
    constructor() {
        this.templates = {
            tshirt: {
                name: "T-Shirt Mockup",
                dimensions: { width: 800, height: 600 },
                overlay_area: { x: 200, y: 150, width: 400, height: 300 }
            },
            mug: {
                name: "Coffee Mug Mockup",
                dimensions: { width: 600, height: 600 },
                overlay_area: { x: 150, y: 200, width: 300, height: 200 }
            },
            phone_case: {
                name: "Phone Case Mockup",
                dimensions: { width: 400, height: 800 },
                overlay_area: { x: 50, y: 100, width: 300, height: 600 }
            }
        };
    }

    simulateImageUpload(imageFile) {
        console.log('📤 Simulating image upload...');
        
        return new Promise((resolve) => {
            setTimeout(() => {
                const uploadResponse = {
                    success: true,
                    file_id: `upload_${Date.now()}`,
                    file_url: `https://mockapi.example.com/uploads/${imageFile}`,
                    file_size: this.getFileSize(imageFile),
                    uploaded_at: new Date().toISOString()
                };
                console.log('✅ Image upload simulated successfully');
                resolve(uploadResponse);
            }, 1000);
        });
    }

    getFileSize(filename) {
        try {
            const stats = fs.statSync(filename);
            return stats.size;
        } catch (error) {
            return 1024 * 150; // Default 150KB
        }
    }

    detectProductType(productData) {
        const title = productData.title.toLowerCase();
        const tags = productData.tags.map(tag => tag.toLowerCase());
        
        if (title.includes('mug') || tags.includes('coffee') || tags.includes('mug')) {
            return 'mug';
        } else if (title.includes('case') || tags.includes('phone case')) {
            return 'phone_case';
        } else {
            return 'tshirt'; // Default
        }
    }

    async generateMockup(productData) {
        console.log('=' * 50);
        console.log('🎨 STARTING MOCKUP GENERATION');
        console.log('=' * 50);
        
        const productType = this.detectProductType(productData);
        const template = this.templates[productType];
        
        console.log(`🏷️  Product Type: ${template.name}`);
        console.log(`📐 Template Dimensions: ${template.dimensions.width}x${template.dimensions.height}`);
        
        // Simulate image upload
        const uploadResponse = await this.simulateImageUpload(productData.image_file);
        
        // Simulate mockup processing
        console.log('🔄 Processing mockup overlay...');
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const mockupFilename = `mockup_${productData.id}.jpg`;
        
        // Simulate mockup file creation
        console.log(`💾 Generating mockup file: ${mockupFilename}`);
        
        // Create Printful-style API response
        const mockupResponse = {
            code: 200,
            result: {
                product_id: productData.id,
                variant_id: `${productData.id}_${productType}`,
                mockup_url: `https://mockapi.example.com/mockups/${mockupFilename}`,
                mockup_file: mockupFilename,
                product_type: productType,
                template_info: {
                    name: template.name,
                    dimensions: template.dimensions,
                    overlay_area: template.overlay_area
                },
                placement: {
                    area_width: template.overlay_area.width,
                    area_height: template.overlay_area.height,
                    top: template.overlay_area.y,
                    left: template.overlay_area.x
                },
                upload_info: uploadResponse,
                processing_time: "2.5 seconds",
                generated_at: new Date().toISOString()
            },
            extra: {
                print_area: `${template.overlay_area.width}x${template.overlay_area.height}px`,
                recommended_dpi: 300,
                supported_formats: ["JPG", "PNG", "PDF"]
            }
        };
        
        // Save mockup data
        const mockupDataFile = `mockup_data_${productData.id}.json`;
        fs.writeFileSync(mockupDataFile, JSON.stringify(mockupResponse, null, 2));
        
        console.log('✅ Mockup generation completed');
        console.log(`📁 Mockup data saved: ${mockupDataFile}`);
        
        return mockupResponse;
    }

    generateMockupSummary(mockupResponse) {
        const result = mockupResponse.result;
        return {
            product_id: result.product_id,
            mockup_file: result.mockup_file,
            product_type: result.product_type,
            dimensions: result.template_info.dimensions,
            generated_at: result.generated_at
        };
    }
}

// Main processing function
async function processProductMockup(productDataFile) {
    try {
        console.log(`📖 Loading product data from: ${productDataFile}`);
        
        const productData = JSON.parse(fs.readFileSync(productDataFile, 'utf8'));
        const generator = new MockupGenerator();
        
        const mockupResponse = await generator.generateMockup(productData);
        const summary = generator.generateMockupSummary(mockupResponse);
        
        console.log('\n📋 MOCKUP SUMMARY:');
        console.log(`   Product: ${productData.title}`);
        console.log(`   Type: ${summary.product_type}`);
        console.log(`   Dimensions: ${summary.dimensions.width}x${summary.dimensions.height}`);
        console.log(`   File: ${summary.mockup_file}`);
        
        return mockupResponse;
        
    } catch (error) {
        console.error('❌ Error processing mockup:', error.message);
        return null;
    }
}

module.exports = { MockupGenerator, processProductMockup };

// CLI usage
if (require.main === module) {
    const productFile = process.argv[2];
    
    if (!productFile) {
        console.log('Usage: node mockup_generator.js <product_data_file.json>');
        process.exit(1);
    }
    
    processProductMockup(productFile).then(result => {
        if (result) {
            console.log('\n🎉 Mockup processing completed successfully!');
        } else {
            console.log('\n💥 Mockup processing failed!');
        }
    });
}
