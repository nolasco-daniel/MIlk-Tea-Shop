from datetime import datetime

class Product:
    def __init__(self, id, name, price, category, description="", stock=50):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.stock = stock
    
    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False
    
    def is_available(self):
        return self.stock > 0

class OrderItem:
    def __init__(self, product, quantity=1, toppings=None, size="Medium"):
        self.product = product
        self.quantity = quantity
        self.toppings = toppings or []
        self.size = size
        
    def get_total(self):
        total = self.product.price
        
        if self.size == "Large":
            total += 20
        elif self.size == "Small":
            total -= 10
            
        for topping in self.toppings:
            total += topping["price"]
            
        return total * self.quantity
    
    def get_display_name(self):
        name = f"{self.product.name} ({self.size})"
        if self.toppings:
            toppings_str = ", ".join([t["name"] for t in self.toppings])
            name += f" with {toppings_str}"
        return name

class Order:
    def __init__(self, id=None, table_id=None):
        self.id = id or datetime.now().strftime("%Y%m%d%H%M%S")
        self.items = []
        self.timestamp = datetime.now()
        self.status = "Pending"
        self.table_id = table_id
        self.discount_percent = 0
        self.discount_type = None
        
    def add_item(self, order_item):
        self.items.append(order_item)
        
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
    
    def apply_discount(self, percent, discount_type="Senior Citizen"):
        self.discount_percent = percent
        self.discount_type = discount_type
            
    def get_total(self):
        subtotal = sum(item.get_total() for item in self.items)
        if self.discount_percent > 0:
            discount_amount = subtotal * (self.discount_percent / 100)
            return subtotal - discount_amount
        return subtotal
    
    def get_discount_amount(self):
        if self.discount_percent > 0:
            subtotal = sum(item.get_total() for item in self.items)
            return subtotal * (self.discount_percent / 100)
        return 0
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items)

class Table:
    def __init__(self, id, name, capacity, status="Available"):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.status = status
        self.current_order = None
        
    def occupy(self, order=None):
        self.status = "Occupied"
        self.current_order = order
        
    def reserve(self):
        self.status = "Reserved"
        
    def clear(self):
        self.status = "Available"
        self.current_order = None
        
    def is_available(self):
        return self.status == "Available"

