import tkinter as tk

def create_product_card(parent, product, colors, on_add_click):
    card = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=1)
    card.configure(padx=15, pady=15)
    
    name_label = tk.Label(card, text=product.name, 
                         font=("Helvetica", 14, "bold"), 
                         fg=colors["primary"],
                         bg="white")
    name_label.pack(fill=tk.X)
    
    category_label = tk.Label(card, text=product.category, 
                             font=("Helvetica", 10), 
                             fg=colors["light_text"],
                             bg="white")
    category_label.pack(fill=tk.X)
    
    separator = tk.Frame(card, height=1, bg=colors["secondary"], bd=0)
    separator.pack(fill=tk.X, pady=8)
    
    price_frame = tk.Frame(card, bg="white")
    price_frame.pack(fill=tk.X)
    
    price_label = tk.Label(price_frame, text=f"₱{product.price:.2f}", 
                          font=("Helvetica", 12, "bold"),
                          fg=colors["primary"],
                          bg="white")
    price_label.pack(side=tk.LEFT)
    
    stock_color = colors["success"] if product.stock > 10 else colors["danger"] if product.stock <= 5 else colors["accent"]
    stock_label = tk.Label(price_frame, text=f"Stock: {product.stock}", 
                          font=("Helvetica", 10),
                          fg=stock_color,
                          bg="white")
    stock_label.pack(side=tk.RIGHT)
    
    desc_label = tk.Label(card, text=product.description, 
                         wraplength=180, justify=tk.LEFT,
                         fg=colors["light_text"],
                         bg="white",
                         height=3)
    desc_label.pack(fill=tk.X, pady=(5, 10))
    
    add_btn = tk.Button(card, text="Add to Order", 
                       bg=colors["primary"] if product.stock > 0 else colors["light_text"], 
                       fg="white",
                       font=("Helvetica", 11, "bold"),
                       activebackground=colors["secondary"],
                       padx=10, pady=5,
                       state=tk.NORMAL if product.stock > 0 else tk.DISABLED,
                       command=on_add_click)
    add_btn.pack(fill=tk.X)
    
    return card

