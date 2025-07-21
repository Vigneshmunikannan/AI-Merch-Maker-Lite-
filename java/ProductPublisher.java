import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.Executors;

public class ProductPublisher {
    private static final String PRODUCTS_LOG = "published_products.log";
    private static final String PRODUCTS_DB = "products_database.json";
    private static final int PORT = 8080;
    
    public static void main(String[] args) throws Exception {
        ProductPublisher publisher = new ProductPublisher();
        publisher.startServer();
    }
    
    public void startServer() throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
        
        // Set up endpoints
        server.createContext("/publish", new PublishHandler());
        server.createContext("/products", new ProductListHandler());
        server.createContext("/stats", new StatsHandler());
        server.createContext("/health", new HealthHandler());
        
        server.setExecutor(Executors.newFixedThreadPool(4));
        server.start();
        
        System.out.println("🚀 PRODUCT PUBLISHER SERVER STARTED");
        System.out.println("📍 Server running on: http://localhost:" + PORT);
        System.out.println("🔗 Available endpoints:");
        System.out.println("   POST /publish    - Publish a product");
        System.out.println("   GET  /products   - List published products");
        System.out.println("   GET  /stats      - Get publishing statistics");
        System.out.println("   GET  /health     - Health check");
        System.out.println("🛑 Press Ctrl+C to stop the server");
    }
    
    // Handler for product publishing
    static class PublishHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equals(exchange.getRequestMethod())) {
                handlePublishRequest(exchange);
            } else {
                sendErrorResponse(exchange, 405, "Method not allowed");
            }
        }
        
        private void handlePublishRequest(HttpExchange exchange) throws IOException {
            try {
                // Read request body
                InputStream inputStream = exchange.getRequestBody();
                String requestBody = new String(inputStream.readAllBytes());
                
                System.out.println("\n📨 Received publish request");
                System.out.println("📄 Request data length: " + requestBody.length() + " bytes");
                
                // Validate and process product data
                ProductData productData = parseProductData(requestBody);
                
                if (productData == null) {
                    sendErrorResponse(exchange, 400, "Invalid product data");
                    return;
                }
                
                // Generate unique product ID
                String productId = "pub_" + System.currentTimeMillis() + "_" + 
                                 Math.abs(productData.title.hashCode() % 10000);
                
                // Create published product record
                PublishedProduct publishedProduct = new PublishedProduct(
                    productId,
                    productData.id,
                    productData.title,
                    productData.description,
                    productData.tags,
                    productData.imageFile,
                    generatePrice(productData),
                    LocalDateTime.now()
                );
                
                // Save to database and log
                saveToDatabase(publishedProduct);
                logPublication(publishedProduct);
                
                // Create success response
                String response = createPublishResponse(publishedProduct);
                
                // Send response
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
                
                System.out.println("✅ Product published successfully");
                System.out.println("🆔 Product ID: " + productId);
                System.out.println("🏷️  Title: " + productData.title);
                System.out.println("💰 Price: $" + publishedProduct.price);
                
            } catch (Exception e) {
                System.err.println("❌ Error publishing product: " + e.getMessage());
                sendErrorResponse(exchange, 500, "Internal server error: " + e.getMessage());
            }
        }
        
        private ProductData parseProductData(String json) {
            try {
                // Simple JSON parsing (in production, use a proper JSON library)
                ProductData data = new ProductData();
                
                // Extract basic fields using string manipulation
                data.id = extractJsonValue(json, "id");
                data.title = extractJsonValue(json, "title");
                data.description = extractJsonValue(json, "description");
                data.imageFile = extractJsonValue(json, "image_file");
                
                // Extract tags array
                data.tags = extractJsonArray(json, "tags");
                
                return data;
            } catch (Exception e) {
                System.err.println("Error parsing JSON: " + e.getMessage());
                return null;
            }
        }
        
        private String extractJsonValue(String json, String key) {
            String pattern = "\"" + key + "\"\\s*:\\s*\"([^\"]+)\"";
            java.util.regex.Pattern p = java.util.regex.Pattern.compile(pattern);
            java.util.regex.Matcher m = p.matcher(json);
            return m.find() ? m.group(1) : "";
        }
        
        private List<String> extractJsonArray(String json, String key) {
            List<String> result = new ArrayList<>();
            String pattern = "\"" + key + "\"\\s*:\\s*\\[([^\\]]+)\\]";
            java.util.regex.Pattern p = java.util.regex.Pattern.compile(pattern);
            java.util.regex.Matcher m = p.matcher(json);
            
            if (m.find()) {
                String arrayContent = m.group(1);
                String[] items = arrayContent.split(",");
                for (String item : items) {
                    String cleanItem = item.trim().replaceAll("\"", "");
                    result.add(cleanItem);
                }
            }
            return result;
        }
        
        private double generatePrice(ProductData data) {
            double basePrice = 19.99;
            double premium = 0.0;
            
            // Add premium based on tags
            for (String tag : data.tags) {
                String lowerTag = tag.toLowerCase();
                if (lowerTag.contains("premium") || lowerTag.contains("luxury")) {
                    premium += 10.0;
                } else if (lowerTag.contains("vintage") || lowerTag.contains("retro")) {
                    premium += 5.0;
                } else if (lowerTag.contains("space") || lowerTag.contains("galaxy")) {
                    premium += 7.0;
                }
            }
            
            return Math.round((basePrice + premium) * 100.0) / 100.0;
        }
        
        private void saveToDatabase(PublishedProduct product) {
            try {
                Path dbPath = Paths.get(PRODUCTS_DB);
                String productJson = productToJson(product);
                
                if (Files.exists(dbPath)) {
                    // Append to existing file
                    Files.write(dbPath, ("\n" + productJson).getBytes(), StandardOpenOption.APPEND);
                } else {
                    // Create new file
                    Files.write(dbPath, productJson.getBytes());
                }
            } catch (IOException e) {
                System.err.println("Error saving to database: " + e.getMessage());
            }
        }
        
        private void logPublication(PublishedProduct product) {
            try {
                String logEntry = String.format("%s - Published: %s - %s - $%.2f%n",
                    LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME),
                    product.publishedId,
                    product.title,
                    product.price);
                
                Files.write(Paths.get(PRODUCTS_LOG), logEntry.getBytes(), 
                           StandardOpenOption.CREATE, StandardOpenOption.APPEND);
            } catch (IOException e) {
                System.err.println("Error writing to log: " + e.getMessage());
            }
        }
        
        private String createPublishResponse(PublishedProduct product) {
            return String.format("""
                {
                    "success": true,
                    "product_id": "%s",
                    "message": "Product published successfully",
                    "published_at": "%s",
                    "product_url": "https://mockstore.example.com/products/%s",
                    "admin_url": "https://admin.mockstore.example.com/products/%s",
                    "price": %.2f,
                    "status": "published"
                }""",
                product.publishedId,
                product.publishedAt.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME),
                product.publishedId,
                product.publishedId,
                product.price);
        }
        
        private String productToJson(PublishedProduct product) {
            return String.format("""
                {
                    "published_id": "%s",
                    "original_id": "%s",
                    "title": "%s",
                    "description": "%s",
                    "tags": [%s],
                    "image_file": "%s",
                    "price": %.2f,
                    "published_at": "%s"
                }""",
                product.publishedId,
                product.originalId,
                product.title.replace("\"", "\\\""),
                product.description.replace("\"", "\\\""),
                String.join("\", \"", product.tags),
                product.imageFile,
                product.price,
                product.publishedAt.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        }
    }
    
    // Handler for listing products
    static class ProductListHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("GET".equals(exchange.getRequestMethod())) {
                String response = """
                    {
                        "message": "Product list endpoint",
                        "total_products": 0,
                        "products": [],
                        "note": "Check products_database.json file for saved products"
                    }""";
                
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            } else {
                sendErrorResponse(exchange, 405, "Method not allowed");
            }
        }
    }
    
    // Handler for statistics
    static class StatsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("GET".equals(exchange.getRequestMethod())) {
                long productCount = countProducts();
                String response = String.format("""
                    {
                        "total_products": %d,
                        "server_uptime": "%s",
                        "last_check": "%s",
                        "status": "active"
                    }""",
                    productCount,
                    "Running since server start",
                    LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
                
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            } else {
                sendErrorResponse(exchange, 405, "Method not allowed");
            }
        }
        
        private long countProducts() {
            try {
                Path dbPath = Paths.get(PRODUCTS_DB);
                if (Files.exists(dbPath)) {
                    return Files.lines(dbPath).count();
                }
            } catch (IOException e) {
                System.err.println("Error counting products: " + e.getMessage());
            }
            return 0;
        }
    }
    
    // Health check handler
    static class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
                {
                    "status": "healthy",
                    "service": "Product Publisher API",
                    "timestamp": "%s"
                }""".formatted(LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
            
            exchange.getResponseHeaders().add("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
    
    // Utility method for error responses
    static void sendErrorResponse(HttpExchange exchange, int statusCode, String message) throws IOException {
        String response = String.format("""
            {
                "success": false,
                "error": "%s",
                "timestamp": "%s"
            }""", message, LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        
        exchange.getResponseHeaders().add("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, response.getBytes().length);
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
    
    // Data classes
    static class ProductData {
        String id;
        String title;
        String description;
        List<String> tags = new ArrayList<>();
        String imageFile;
    }
    
    static class PublishedProduct {
        String publishedId;
        String originalId;
        String title;
        String description;
        List<String> tags;
        String imageFile;
        double price;
        LocalDateTime publishedAt;
        
        PublishedProduct(String publishedId, String originalId, String title, 
                        String description, List<String> tags, String imageFile, 
                        double price, LocalDateTime publishedAt) {
            this.publishedId = publishedId;
            this.originalId = originalId;
            this.title = title;
            this.description = description;
            this.tags = tags;
            this.imageFile = imageFile;
            this.price = price;
            this.publishedAt = publishedAt;
        }
    }
}
