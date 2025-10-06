-- Create database
CREATE DATABASE IF NOT EXISTS apex_digital;
USE apex_digital;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    company VARCHAR(100),
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'customer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
);

-- Products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    short_description VARCHAR(500),
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'ZAR',
    category VARCHAR(100) NOT NULL,
    service_type VARCHAR(50),
    delivery_days INT DEFAULT 7,
    image_url VARCHAR(500),
    features JSON,
    requirements JSON,
    is_active BOOLEAN DEFAULT TRUE,
    ai_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_service_type (service_type),
    INDEX idx_active (is_active)
);

-- Orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    client_requirements JSON,
    delivery_date TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (status)
);

-- Order items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    configuration JSON,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_order_id (order_id)
);

-- Payments table
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'ZAR',
    status VARCHAR(50) DEFAULT 'pending',
    payment_reference VARCHAR(100),
    payfast_payment_id VARCHAR(100),
    raw_response JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    INDEX idx_order_id (order_id),
    INDEX idx_payment_reference (payment_reference)
);

-- AI Services table
CREATE TABLE ai_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    agent_type VARCHAR(50) NOT NULL,
    capabilities JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_agent_type (agent_type)
);

-- AI Tasks table
CREATE TABLE ai_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    user_id INT NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    task_data JSON NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    result_data JSON,
    progress INT DEFAULT 0,
    assigned_agents JSON,
    error_message TEXT,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_service_type (service_type)
);

-- Insert sample products
INSERT INTO products (name, description, short_description, price, category, service_type, delivery_days, features) VALUES
('Basic Website', 'Professional single-page website with responsive design and contact form', 'Get your business online with a stunning single-page website', 2499.00, 'website', 'basic', 7, '["Responsive Design", "Contact Form", "SEO Optimization", "1 Page", "Basic Hosting"]'),
('E-Commerce Store', 'Full online store with product management, cart, and secure payments', 'Start selling online with a complete e-commerce solution', 5999.00, 'ecommerce', 'standard', 14, '["Product Management", "Shopping Cart", "Payment Gateway", "Order Tracking", "Inventory Management"]'),
('Content Creation Package', 'AI-powered content creation for your website and social media', 'Engaging content tailored to your brand voice', 1299.00, 'content', 'basic', 3, '["Website Copy", "Social Media Posts", "Blog Articles", "SEO Optimization", "Brand Voice Matching"]'),
('Social Media Marketing', 'Complete social media management and advertising campaigns', 'Grow your audience and engagement across all platforms', 2999.00, 'marketing', 'premium', 7, '["Content Strategy", "Post Scheduling", "Audience Analysis", "Performance Tracking", "Ad Management"]'),
('Website + Marketing Bundle', 'Complete website with integrated marketing campaign', 'All-in-one solution for online presence and growth', 7999.00, 'bundle', 'premium', 14, '["Professional Website", "SEO Setup", "Social Media Integration", "Email Marketing", "Analytics Dashboard"]');

-- Insert AI services
INSERT INTO ai_services (name, description, agent_type, capabilities) VALUES
('Content Creator AI', 'Creates engaging content for websites, social media, and marketing materials', 'content', '["website_content", "social_media", "blog_posts", "ad_copy", "email_marketing"]'),
('Marketing Pro AI', 'Develops and executes comprehensive marketing strategies across all platforms', 'marketing', '["social_media_campaigns", "email_marketing", "ad_optimization", "audience_analysis", "performance_tracking"]'),
('Website Builder AI', 'Designs and develops responsive, professional websites automatically', 'website', '["responsive_design", "ui_ux", "frontend_development", "seo_optimization", "performance_optimization"]'),
('Security Guardian AI', 'Provides military-grade security and compliance monitoring', 'security', '["threat_detection", "vulnerability_scanning", "compliance_monitoring", "data_protection", "access_control"]'),
('Payment Processor AI', 'Manages secure payments and financial distribution', 'payment', '["payment_processing", "fraud_detection", "financial_reporting", "tax_compliance", "revenue_distribution"]');
