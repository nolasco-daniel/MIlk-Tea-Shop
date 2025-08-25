from models import Product, Table

class DataManager:
    def __init__(self):
        self.products = []
        self.toppings = []
        self.orders = []
        self.tables = []
        self.load_data()
        
    def load_data(self):
        self.products = [
            Product(1, "Classic Milk Tea", 90, "Milk Tea", "Our signature milk tea with a perfect balance of tea and milk"),
            Product(2, "Taro Milk Tea", 110, "Milk Tea", "Creamy taro flavor with milk tea base"),
            Product(3, "Matcha Milk Tea", 120, "Milk Tea", "Rich green tea flavor with creamy milk"),
            Product(4, "Brown Sugar Milk Tea", 130, "Milk Tea", "Milk tea with caramelized brown sugar syrup"),
            Product(5, "Wintermelon Milk Tea", 100, "Milk Tea", "Subtle wintermelon taste with milk tea"),
            Product(6, "Okinawa Milk Tea", 125, "Milk Tea", "Roasted brown sugar flavor from Okinawa"),
            Product(7, "Thai Milk Tea", 115, "Milk Tea", "Authentic Thai tea with condensed milk"),
            Product(8, "Hokkaido Milk Tea", 135, "Milk Tea", "Rich and creamy with caramel notes"),
            Product(9, "Jasmine Milk Tea", 105, "Milk Tea", "Fragrant jasmine tea with milk"),
            Product(10, "Chocolate Milk Tea", 120, "Milk Tea", "Cocoa-infused milk tea blend"),
            
            Product(11, "Strawberry Fruit Tea", 120, "Fruit Tea", "Sweet strawberry flavor with fresh tea"),
            Product(12, "Mango Fruit Tea", 110, "Fruit Tea", "Refreshing mango taste with tea base"),
            Product(13, "Lychee Fruit Tea", 110, "Fruit Tea", "Sweet lychee flavor with jasmine tea"),
            Product(14, "Passion Fruit Tea", 115, "Fruit Tea", "Tangy passion fruit with green tea"),
            Product(15, "Peach Fruit Tea", 115, "Fruit Tea", "Sweet peach flavor with black tea"),
            Product(16, "Kiwi Fruit Tea", 120, "Fruit Tea", "Zesty kiwi with green tea base"),
            Product(17, "Blueberry Fruit Tea", 125, "Fruit Tea", "Sweet-tart blueberry with black tea"),
            Product(18, "Watermelon Fruit Tea", 110, "Fruit Tea", "Refreshing watermelon with green tea"),
            Product(19, "Grape Fruit Tea", 115, "Fruit Tea", "Sweet grape flavor with jasmine tea"),
            Product(20, "Pineapple Fruit Tea", 120, "Fruit Tea", "Tropical pineapple with black tea")
        ]
        
        self.toppings = [
            {"id": 1, "name": "Pearls", "price": 15},
            {"id": 2, "name": "Grass Jelly", "price": 15},
            {"id": 3, "name": "Pudding", "price": 20},
            {"id": 4, "name": "Aloe Vera", "price": 20},
            {"id": 5, "name": "Cream Cheese", "price": 25},
            {"id": 6, "name": "Red Bean", "price": 15},
            {"id": 7, "name": "Coconut Jelly", "price": 18},
            {"id": 8, "name": "Crystal Boba", "price": 20},
            {"id": 9, "name": "Fruit Popping Boba", "price": 22}
        ]
        
        self.load_tables()
        
    def load_tables(self):
        self.tables = [
            Table(1, "Table 1", 2),
            Table(2, "Table 2", 3),
            Table(3, "Table 3", 4),
            Table(4, "Table 4", 5),
            Table(5, "Table 5", 6),
            
        ]
    
    def get_products_by_category(self, category=None):
        if category:
            return [p for p in self.products if p.category == category]
        return self.products
    
    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None
    
    def save_order(self, order):
        self.orders.append(order)
        self.update_product_stock(order)
        total_with_tax = order.get_total() + (order.get_total() * 0.12)
        print(f"Order {order.id} saved with {order.get_item_count()} items, total: ₱{total_with_tax:.2f}")
        return True

    def get_available_tables(self):
        return [table for table in self.tables if table.is_available()]
    
    def get_table_by_id(self, table_id):
        for table in self.tables:
            if table.id == table_id:
                return table
        return None
    
    def assign_order_to_table(self, order, table_id):
        table = self.get_table_by_id(table_id)
        if table and table.is_available():
            table.occupy(order)
            return True
        return False
    
    def clear_table(self, table_id):
        table = self.get_table_by_id(table_id)
        if table:
            table.clear()
            return True
        return False
        
    def search_products(self, query):
        from algorithms import fuzzy_search_score
        
        if not query:
            return self.products
            
        query = query.lower()
        query_words = query.split()
        
        product_scores = {}
        
        for product in self.products:
            name_lower = product.name.lower()
            category_lower = product.category.lower()
            description_lower = product.description.lower()
            
            score = 0
            
            if query in name_lower:
                score += 100
            if query in category_lower:
                score += 50
            if query in description_lower:
                score += 25
            
            for word in query_words:
                if len(word) < 2:
                    continue
                    
                if word in name_lower:
                    score += 50
                if word in category_lower:
                    score += 25
                if word in description_lower:
                    score += 10
                
                for name_word in name_lower.split():
                    if name_word.startswith(word):
                        score += 30
                
                for category_word in category_lower.split():
                    if category_word.startswith(word):
                        score += 15
                
                for desc_word in description_lower.split():
                    if desc_word.startswith(word):
                        score += 5
            
            if score == 0:
                name_fuzzy_score = fuzzy_search_score(query, name_lower)
                if name_fuzzy_score > 0:
                    score += name_fuzzy_score * 0.8
                
                category_fuzzy_score = fuzzy_search_score(query, category_lower)
                if category_fuzzy_score > 0:
                    score += category_fuzzy_score * 0.4
                
                description_fuzzy_score = fuzzy_search_score(query, description_lower)
                if description_fuzzy_score > 0:
                    score += description_fuzzy_score * 0.2
            
            if score > 0:
                product_scores[product] = score
        
        sorted_products = sorted(product_scores.keys(), 
                                key=lambda p: product_scores[p], 
                                reverse=True)
        
        return sorted_products

    def update_product_stock(self, order):
        for item in order.items:
            product = self.get_product_by_id(item.product.id)
            if product:
                product.update_stock(item.quantity)
        return True

