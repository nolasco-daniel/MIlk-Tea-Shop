import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from models import Order
from data_manager import DataManager
from ui.product_card import create_product_card
from ui.product_options import show_product_options
from ui.checkout import show_checkout_window
from ui.table_management import show_table_management, select_table_dialog

from ui.product_sorting import create_sort_controls, sort_products

class MilkTeaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Bubble Bliss - Premium Milk Tea Shop")
        self.geometry("1280x720")
        self.configure(bg="#F8F5F2")
        
        try:
            self.iconbitmap("bubble_tea_icon.ico")
        except:
            pass
        
        self.data_manager = DataManager()
        
        self.current_order = Order()
        self.current_category = "All"
        self.current_sort = "default"
        
        self.colors = {
            "primary": "#6B4226",     
            "secondary": "#D4A373",   
            "accent": "#E9C46A",       
            "background": "#F8F5F2",   
            "text": "#2D2424",       
            "light_text": "#6B705C",  
            "success": "#588157",     
            "danger": "#BC6C25"       
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabel", background=self.colors["background"], foreground=self.colors["text"], font=("Helvetica", 12))
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), foreground=self.colors["primary"])
        self.style.configure("Title.TLabel", font=("Helvetica", 20, "bold"), foreground=self.colors["primary"])
        self.style.configure("Card.TFrame", background="#FFFFFF", relief="raised")
        
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.header_frame = ttk.Frame(self.main_container)
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.logo_label = ttk.Label(self.header_frame, text="🧋 Bubble Bliss", 
                                   style="Title.TLabel")
        self.logo_label.pack(side=tk.LEFT)
        
        ttk.Label(self.header_frame, text="Premium Milk Tea & Fruit Tea", 
                 font=("Helvetica", 14), foreground=self.colors["light_text"]).pack(side=tk.LEFT, padx=10)
        
        self.table_mgmt_btn = tk.Button(self.header_frame, text="Table Management", 
                                       bg=self.colors["secondary"], fg="white", 
                                       font=("Helvetica", 12, "bold"),
                                       command=self.show_table_management)
        self.table_mgmt_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.stock_mgmt_btn = tk.Button(self.header_frame, text="Stock Management", 
                                       bg=self.colors["accent"], fg="white", 
                                       font=("Helvetica", 12, "bold"),
                                       command=self.show_stock_management)
        self.stock_mgmt_btn.pack(side=tk.RIGHT)
        
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.menu_frame = ttk.Frame(self.content_frame, padding=10)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.search_frame = ttk.Frame(self.menu_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(self.search_frame, text="Search:", 
                 font=("Helvetica", 14, "bold"), 
                 foreground=self.colors["primary"]).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, 
                                     font=("Helvetica", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.clear_search_btn = tk.Button(self.search_frame, text="✕", 
                                         bg=self.colors["secondary"], fg="white",
                                         font=("Helvetica", 10, "bold"),
                                         width=2, command=self.clear_search)
        self.clear_search_btn.pack(side=tk.LEFT, padx=5)
        
        self.search_btn = tk.Button(self.search_frame, text="Search", 
                                   bg=self.colors["primary"], fg="white",
                                   font=("Helvetica", 12, "bold"),
                                   command=self.perform_search)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        
        self.category_frame = ttk.Frame(self.menu_frame)
        self.category_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(self.category_frame, text="Categories:", 
                 font=("Helvetica", 14, "bold"), foreground=self.colors["primary"]).pack(side=tk.LEFT, padx=(0, 10))
        
        categories = ["All", "Milk Tea", "Fruit Tea"]
        for category in categories:
            btn = tk.Button(self.category_frame, text=category, 
                           bg=self.colors["secondary"], fg="white", 
                           font=("Helvetica", 12, "bold"), 
                           relief=tk.RAISED,
                           padx=15, pady=5,
                           borderwidth=0,
                           command=lambda c=category: self.filter_products(c))
            btn.pack(side=tk.LEFT, padx=5)
        
        self.sort_frame = create_sort_controls(self.menu_frame, self.colors, self.sort_products_by)
        self.sort_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.products_frame = ttk.Frame(self.menu_frame)
        self.products_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.products_frame, bg=self.colors["background"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.products_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.results_label = ttk.Label(self.scrollable_frame, text="", 
                                      font=("Helvetica", 12, "italic"),
                                      foreground=self.colors["light_text"])
        
        self.order_frame = ttk.Frame(self.content_frame, padding=15, width=420)
        self.order_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.order_frame.pack_propagate(False)
        
        order_header_frame = ttk.Frame(self.order_frame)
        order_header_frame.pack(fill=tk.X, pady=(0, 15))
        
        order_header = ttk.Label(order_header_frame, text="Current Order", 
                                style="Header.TLabel")
        order_header.pack(side=tk.LEFT)
        
        self.order_list_frame = ttk.Frame(self.order_frame, relief=tk.GROOVE, borderwidth=1)
        self.order_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.order_canvas = tk.Canvas(self.order_list_frame, bg="white", highlightthickness=0)
        self.order_scrollbar = ttk.Scrollbar(self.order_list_frame, orient="vertical", command=self.order_canvas.yview)
        self.order_scrollable_frame = ttk.Frame(self.order_canvas, style="TFrame")
        
        self.order_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.order_canvas.configure(
                scrollregion=self.order_canvas.bbox("all")
            )
        )
        
        self.order_canvas.create_window((0, 0), window=self.order_scrollable_frame, anchor="nw")
        self.order_canvas.configure(yscrollcommand=self.order_scrollbar.set)
        
        self.order_canvas.pack(side="left", fill="both", expand=True)
        self.order_scrollbar.pack(side="right", fill="y")
        
        self.summary_frame = ttk.Frame(self.order_frame)
        self.summary_frame.pack(fill=tk.X, pady=15)
        
        subtotal_frame = ttk.Frame(self.summary_frame)
        subtotal_frame.pack(fill=tk.X, pady=2)
        ttk.Label(subtotal_frame, text="Subtotal:").pack(side=tk.LEFT)
        self.subtotal_label = ttk.Label(subtotal_frame, text="₱0.00")
        self.subtotal_label.pack(side=tk.RIGHT)
        
        self.total_frame = ttk.Frame(self.summary_frame)
        self.total_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.total_frame, text="Total:", font=("Helvetica", 14, "bold"), 
                 foreground=self.colors["primary"]).pack(side=tk.LEFT)
        self.total_label = ttk.Label(self.total_frame, text="₱0.00", 
                                    font=("Helvetica", 16, "bold"), 
                                    foreground=self.colors["primary"])
        self.total_label.pack(side=tk.RIGHT)
        
        self.checkout_btn = tk.Button(self.order_frame, text="Checkout", 
                                     bg=self.colors["primary"], fg="white", 
                                     font=("Helvetica", 14, "bold"),
                                     height=2,
                                     activebackground=self.colors["secondary"],
                                     command=self.checkout)
        self.checkout_btn.pack(fill=tk.X, pady=(10, 0))
        
        self.new_order_btn = tk.Button(self.order_frame, text="New Order", 
                                      bg=self.colors["secondary"], fg="white", 
                                      font=("Helvetica", 12, "bold"),
                                      activebackground=self.colors["accent"],
                                      command=self.new_order)
        self.new_order_btn.pack(fill=tk.X, pady=(10, 0))
        
        self.senior_discount_btn = tk.Button(self.order_frame, text="Senior Citizen Discount (20%)", 
                                      bg=self.colors["accent"], fg="white", 
                                      font=("Helvetica", 12, "bold"),
                                      activebackground=self.colors["secondary"],
                                      command=self.apply_senior_discount)
        self.senior_discount_btn.pack(fill=tk.X, pady=(10, 0))
        
        self.search_entry.bind("<Return>", lambda event: self.perform_search())
        
        self.filter_products("All")
    
    def filter_products(self, category):
        self.current_category = category
        self.search_var.set("")
        
        products = self.data_manager.get_products_by_category(category if category != "All" else None)
        sorted_products = sort_products(products, self.current_sort)
        self.display_products(products=sorted_products)
            
    def display_products(self, products=None, category=None, search_query=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if search_query:
            results_label = ttk.Label(self.scrollable_frame, text=search_query, 
                                     font=("Helvetica", 12, "italic"),
                                     foreground=self.colors["light_text"])
            results_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 10))
            start_row = 1
        else:
            start_row = 0
            
        if products is None:
            if category == "All":
                products = self.data_manager.get_products_by_category()
            else:
                products = self.data_manager.get_products_by_category(category)
        
        if not products:
            no_results = ttk.Label(self.scrollable_frame, text="No products found", 
                                  font=("Helvetica", 14, "bold"),
                                  foreground=self.colors["light_text"])
            no_results.grid(row=start_row, column=0, columnspan=3, padx=10, pady=50)
            
            if search_query:
                suggestions = ttk.Label(self.scrollable_frame, 
                                      text="Try different search terms or check the spelling",
                                      font=("Helvetica", 12),
                                      foreground=self.colors["light_text"])
                suggestions.grid(row=start_row+1, column=0, columnspan=3, padx=10, pady=10)
                
                show_all_btn = tk.Button(self.scrollable_frame, text="Show All Products", 
                                        bg=self.colors["secondary"], fg="white",
                                        font=("Helvetica", 12, "bold"),
                                        command=lambda: self.filter_products("All"))
                show_all_btn.grid(row=start_row+2, column=0, columnspan=3, padx=10, pady=10)
            
            return
            
        row, col = start_row, 0
        for product in products:
            card = create_product_card(self.scrollable_frame, product, self.colors, 
                                      lambda p=product: self.show_product_options(p))
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col > 2:  
                col = 0
                row += 1
                
        for i in range(3):
            self.scrollable_frame.columnconfigure(i, weight=1)
    
    def on_search_change(self, *args):
        if not self.search_var.get():
            self.filter_products(self.current_category)
        elif len(self.search_var.get()) >= 3:
            self.perform_search()
    
    def perform_search(self):
        query = self.search_var.get().strip()
        if not query:
            self.filter_products(self.current_category)
            return
        
        results = self.data_manager.search_products(query)
        self.current_search_results = results
        sorted_results = sort_products(results, self.current_sort)
        
        exact_match_found = any(query.lower() in product.name.lower() for product in results)
        search_message = f"Search results for: '{query}'"
        
        if not exact_match_found and results:
            search_message += " (including similar matches)"
            
        self.display_products(products=sorted_results, search_query=search_message)
    
    def clear_search(self):
        self.search_var.set("")
        self.filter_products(self.current_category)
    
    def show_product_options(self, product):
        show_product_options(self, product, self.colors, self.data_manager, self.add_to_order)
    
    def add_to_order(self, order_item):
        self.current_order.add_item(order_item)
        self.update_order_display()
    
    def apply_senior_discount(self):
        if not self.current_order.items:
            from tkinter import messagebox
            messagebox.showinfo("Empty Order", "Please add items to your order before applying a discount.")
            return
            
        if self.current_order.discount_percent > 0:
            from tkinter import messagebox
            messagebox.showinfo("Discount Already Applied", 
                               f"{self.current_order.discount_type} discount of {self.current_order.discount_percent}% is already applied.")
            return
            
        self.current_order.apply_discount(20, "Senior Citizen")
        self.update_order_display()
        
        from tkinter import messagebox
        messagebox.showinfo("Discount Applied", "20% Senior Citizen discount has been applied to your order.")
    
    def new_order(self):
        self.current_order = Order()
        self.update_order_display()
    
    def update_order_display(self):
        for widget in self.order_scrollable_frame.winfo_children():
            widget.destroy()
            
        if not self.current_order.items:
            empty_label = ttk.Label(self.order_scrollable_frame, 
                                   text="Your order is empty.\nAdd items from the menu.",
                                   font=("Helvetica", 12),
                                   foreground=self.colors["light_text"])
            empty_label.pack(pady=50)
            
        subtotal = 0
            
        for i, item in enumerate(self.current_order.items):
            item_frame = tk.Frame(self.order_scrollable_frame, bg="white", padx=10, pady=8)
            item_frame.pack(fill=tk.X, pady=2)

            top_frame = tk.Frame(item_frame, bg="white")
            top_frame.pack(fill=tk.X)
            
            tk.Label(top_frame, text=f"{item.quantity}x", 
                    font=("Helvetica", 12, "bold"),
                    width=3, bg="white",
                    fg=self.colors["primary"]).pack(side=tk.LEFT)
            
            name_label = tk.Label(top_frame, text=item.product.name, 
                                 font=("Helvetica", 12, "bold"),
                                 bg="white", anchor="w")
            name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            item_total = item.get_total()
            subtotal += item_total
            
            tk.Label(top_frame, text=f"₱{item_total:.2f}", 
                    font=("Helvetica", 12),
                    bg="white").pack(side=tk.RIGHT)
            
            if item.size != "Medium" or item.toppings:
                details_frame = tk.Frame(item_frame, bg="white")
                details_frame.pack(fill=tk.X, pady=(2, 0))
                
                details_text = f"Size: {item.size}"
                if item.toppings:
                    toppings_str = ", ".join([t["name"] for t in item.toppings])
                    details_text += f" • Toppings: {toppings_str}"
                
                tk.Label(details_frame, text=details_text, 
                        font=("Helvetica", 10),
                        fg=self.colors["light_text"],
                        bg="white", wraplength=300, 
                        justify=tk.LEFT).pack(side=tk.LEFT, padx=(25, 0))
            
            remove_btn = tk.Button(item_frame, text="×", 
                                  font=("Helvetica", 12, "bold"),
                                  bg="white", fg=self.colors["danger"],
                                  borderwidth=0,
                                  command=lambda idx=i: self.remove_item(idx))
            remove_btn.pack(anchor="e")

        self.subtotal_label.config(text=f"₱{subtotal:.2f}")
        
        if hasattr(self, 'discount_frame'):
            self.discount_frame.destroy()
            
        if self.current_order.discount_percent > 0:
            self.discount_frame = ttk.Frame(self.summary_frame)
            self.discount_frame.pack(fill=tk.X, pady=2, before=self.total_frame)
            
            discount_amount = self.current_order.get_discount_amount()
            ttk.Label(self.discount_frame, 
                     text=f"{self.current_order.discount_type} Discount ({self.current_order.discount_percent}%):").pack(side=tk.LEFT)
            ttk.Label(self.discount_frame, 
                     text=f"-₱{discount_amount:.2f}",
                     foreground=self.colors["success"]).pack(side=tk.RIGHT)
        
        if hasattr(self, 'tax_frame'):
            self.tax_frame.destroy()
            
        self.tax_frame = ttk.Frame(self.summary_frame)
        self.tax_frame.pack(fill=tk.X, pady=2, before=self.total_frame)
        tax = self.current_order.get_total() * 0.12
        ttk.Label(self.tax_frame, text="Tax (12%):").pack(side=tk.LEFT)
        ttk.Label(self.tax_frame, text=f"₱{tax:.2f}").pack(side=tk.RIGHT)
        
        order_total = self.current_order.get_total()
        tax = order_total * 0.12
        final_total = order_total + tax
        self.total_label.config(text=f"₱{final_total:.2f}")
    
    def remove_item(self, index):
        self.current_order.remove_item(index)
        self.update_order_display()
    
    def check_stock_availability(self):
        for item in self.current_order.items:
            product = self.data_manager.get_product_by_id(item.product.id)
            if not product or product.stock < item.quantity:
                return False, product.name if product else "Unknown product"
        return True, ""

    def checkout(self):
        if not self.current_order.items:
            from tkinter import messagebox
            messagebox.showinfo("Empty Order", "Please add items to your order before checkout.")
            return
        
        stock_available, product_name = self.check_stock_availability()
        if not stock_available:
            from tkinter import messagebox
            messagebox.showwarning("Stock Issue", 
                                  f"Sorry, {product_name} is no longer available in the requested quantity. Please update your order.")
            return
        
        if self.current_order.table_id is None:
            select_table_dialog(self, self.data_manager, self.colors, self.assign_table_to_order)
        else:
            show_checkout_window(self, self.current_order, self.colors, self.data_manager, self.new_order)
    
    def new_order(self):
        self.current_order = Order()
        self.update_order_display()

    def show_table_management(self):
        show_table_management(self, self.data_manager, self.colors)

    def assign_table_to_order(self, table_id):
        self.current_order.table_id = table_id
        show_checkout_window(self, self.current_order, self.colors, self.data_manager, self.new_order)

    def show_stock_management(self):
        from ui.stock_management import show_stock_management
        show_stock_management(self, self.data_manager, self.colors)

    def sort_products_by(self, sort_option):
        self.current_sort = sort_option
        
        if hasattr(self, 'current_search_results'):
            sorted_products = sort_products(self.current_search_results, sort_option)
            self.display_products(products=sorted_products, search_query=self.search_var.get())
        else:
            if self.current_category == "All":
                products = self.data_manager.get_products_by_category()
            else:
                products = self.data_manager.get_products_by_category(self.current_category)
            
            sorted_products = sort_products(products, sort_option)
            self.display_products(products=sorted_products)

