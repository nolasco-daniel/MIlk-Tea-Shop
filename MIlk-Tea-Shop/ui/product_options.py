import tkinter as tk
from models import OrderItem

def show_product_options(parent, product, colors, data_manager, add_to_order_callback):
    options_window = tk.Toplevel(parent)
    options_window.title(f"Customize {product.name}")
    options_window.geometry("450x600")
    options_window.configure(bg=colors["background"])
    options_window.transient(parent)  
    options_window.grab_set() 
    
    header_frame = tk.Frame(options_window, bg=colors["primary"], padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    
    tk.Label(header_frame, text=product.name, 
            font=("Helvetica", 18, "bold"), 
            fg="white", bg=colors["primary"]).pack(anchor="w")
    
    stock_text = f"In Stock: {product.stock}"
    stock_color = "white"
    tk.Label(header_frame, text=stock_text, 
            font=("Helvetica", 12, "bold"), 
            fg=stock_color, bg=colors["primary"]).pack(anchor="w")
    
    tk.Label(header_frame, text=product.description, 
            font=("Helvetica", 10), 
            fg="white", bg=colors["primary"],
            wraplength=400).pack(anchor="w", pady=(5, 0))
    
    content_frame = tk.Frame(options_window, bg=colors["background"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    size_frame = tk.LabelFrame(content_frame, text="Size", 
                              font=("Helvetica", 12, "bold"),
                              fg=colors["primary"],
                              bg=colors["background"])
    size_frame.pack(fill=tk.X, pady=10)
    
    size_var = tk.StringVar(value="Medium")
    sizes = [("Small", "Small (₱-10)"), ("Medium", "Medium"), ("Large", "Large (₱+20)")]
    
    for size_value, size_text in sizes:
        rb = tk.Radiobutton(size_frame, text=size_text, value=size_value, 
                           variable=size_var, bg=colors["background"],
                           font=("Helvetica", 11),
                           fg=colors["text"])
        rb.pack(anchor="w", padx=20, pady=5)
    
    toppings_frame = tk.LabelFrame(content_frame, text="Toppings", 
                                  font=("Helvetica", 12, "bold"),
                                  fg=colors["primary"],
                                  bg=colors["background"])
    toppings_frame.pack(fill=tk.X, pady=10)
    
    toppings_canvas = tk.Canvas(toppings_frame, bg=colors["background"], 
                               highlightthickness=0, height=180)
    toppings_scrollbar = tk.Scrollbar(toppings_frame, orient="vertical", 
                                      command=toppings_canvas.yview)
    toppings_scrollable = tk.Frame(toppings_canvas, bg=colors["background"])
    
    toppings_scrollable.bind(
        "<Configure>",
        lambda e: toppings_canvas.configure(
            scrollregion=toppings_canvas.bbox("all")
        )
    )
    
    toppings_canvas.create_window((0, 0), window=toppings_scrollable, anchor="nw")
    toppings_canvas.configure(yscrollcommand=toppings_scrollbar.set)
    
    toppings_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
    toppings_scrollbar.pack(side="right", fill="y")
    
    topping_vars = {}
    for topping in data_manager.toppings:
        var = tk.BooleanVar(value=False)
        topping_vars[topping["id"]] = var
        
        topping_frame = tk.Frame(toppings_scrollable, bg=colors["background"])
        topping_frame.pack(fill=tk.X, pady=3)
        
        cb = tk.Checkbutton(
            topping_frame, 
            text=f"{topping['name']}", 
            variable=var,
            bg=colors["background"],
            font=("Helvetica", 11),
            fg=colors["text"]
        )
        cb.pack(side=tk.LEFT)
        
        tk.Label(topping_frame, 
                text=f"₱{topping['price']}", 
                bg=colors["background"],
                fg=colors["light_text"]).pack(side=tk.RIGHT)
    
    quantity_frame = tk.LabelFrame(content_frame, text="Quantity", 
                                  font=("Helvetica", 12, "bold"),
                                  fg=colors["primary"],
                                  bg=colors["background"])
    quantity_frame.pack(fill=tk.X, pady=10)
    
    quantity_control = tk.Frame(quantity_frame, bg=colors["background"])
    quantity_control.pack(padx=20, pady=10)
    
    quantity_var = tk.IntVar(value=1)
    
    def decrease_quantity():
        if quantity_var.get() > 1:
            quantity_var.set(quantity_var.get() - 1)
            
    def increase_quantity():
        if quantity_var.get() < product.stock:
            quantity_var.set(quantity_var.get() + 1)
    
    decrease_btn = tk.Button(quantity_control, text="-", 
                            font=("Helvetica", 14, "bold"),
                            width=3, height=1,
                            command=decrease_quantity)
    decrease_btn.pack(side=tk.LEFT, padx=5)
    
    quantity_label = tk.Label(quantity_control, textvariable=quantity_var, width=3, 
                             font=("Helvetica", 14, "bold"),
                             bg=colors["background"])
    quantity_label.pack(side=tk.LEFT, padx=10)
    
    increase_btn = tk.Button(quantity_control, text="+", 
                            font=("Helvetica", 14, "bold"),
                            width=3, height=1,
                            command=increase_quantity)
    increase_btn.pack(side=tk.LEFT, padx=5)
    
    stock_note = tk.Label(quantity_frame, text=f"(Maximum: {product.stock})", 
                         font=("Helvetica", 10, "italic"),
                         fg=colors["light_text"],
                         bg=colors["background"])
    stock_note.pack(pady=(0, 10))
    
    buttons_frame = tk.Frame(options_window, bg=colors["background"], padx=20, pady=20)
    buttons_frame.pack(fill=tk.X)
    
    def add_to_order():
        selected_toppings = []
        for topping_id, var in topping_vars.items():
            if var.get():
                topping = next((t for t in data_manager.toppings if t["id"] == topping_id), None)
                if topping:
                    selected_toppings.append(topping)
        
        order_item = OrderItem(
            product=product,
            quantity=quantity_var.get(),
            toppings=selected_toppings,
            size=size_var.get()
        )
        
        add_to_order_callback(order_item)
        
        options_window.destroy()
    
    tk.Button(buttons_frame, text="Add to Order", 
             bg=colors["primary"], fg="white", 
             font=("Helvetica", 14, "bold"),
             height=2,
             activebackground=colors["secondary"],
             command=add_to_order).pack(fill=tk.X, pady=(0, 10))
    
    tk.Button(buttons_frame, text="Cancel", 
             bg=colors["secondary"], fg="white", 
             font=("Helvetica", 12),
             activebackground=colors["accent"],
             command=options_window.destroy).pack(fill=tk.X)

