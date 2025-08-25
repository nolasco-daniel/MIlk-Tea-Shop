import tkinter as tk
from tkinter import ttk
from algorithms import bubble_sort

def create_sort_controls(parent, colors, on_sort_change):
    sort_frame = ttk.Frame(parent)
    
    ttk.Label(sort_frame, text="Sort by:", 
             font=("Helvetica", 14, "bold"), 
             foreground=colors["primary"]).pack(side=tk.LEFT, padx=(0, 10))
    
    sort_var = tk.StringVar(value="default")
    
    sort_options = [
        ("default", "Default"),
        ("name_asc", "Name (A-Z)"),
        ("name_desc", "Name (Z-A)"),
        ("price_asc", "Price (Low to High)"),
        ("price_desc", "Price (High to Low)"),
        ("stock_asc", "Stock (Low to High)"),
        ("stock_desc", "Stock (High to Low)")
    ]
    
    sort_dropdown = ttk.Combobox(sort_frame, 
                                textvariable=sort_var,
                                values=[opt[1] for opt in sort_options],
                                state="readonly",
                                width=20,
                                font=("Helvetica", 12))
    sort_dropdown.current(0)
    sort_dropdown.pack(side=tk.LEFT, padx=5)
    
    option_map = {opt[1]: opt[0] for opt in sort_options}
    
    def on_dropdown_change(event):
        selected_display = sort_dropdown.get()
        selected_value = option_map.get(selected_display, "default")
        on_sort_change(selected_value)
    
    sort_dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)
    
    return sort_frame

def sort_products(products, sort_option):
    if sort_option == "default" or not sort_option:
        return products
    
    field, direction = sort_option.split('_')
    reverse = direction == "desc"
    
    if field == "name":
        return bubble_sort(products, key=lambda p: p.name.lower(), reverse=reverse)
    elif field == "price":
        return bubble_sort(products, key=lambda p: p.price, reverse=reverse)
    elif field == "stock":
        return bubble_sort(products, key=lambda p: p.stock, reverse=reverse)
    
    return products

