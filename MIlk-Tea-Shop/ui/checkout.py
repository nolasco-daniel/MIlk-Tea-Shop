import tkinter as tk
from tkinter import messagebox

def show_checkout_window(parent, order, colors, data_manager, new_order_callback):
    checkout_window = tk.Toplevel(parent)
    checkout_window.title("Checkout")
    checkout_window.geometry("500x600")
    checkout_window.configure(bg=colors["background"])
    checkout_window.transient(parent)
    checkout_window.grab_set()
    
    header_frame = tk.Frame(checkout_window, bg=colors["primary"], padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    
    tk.Label(header_frame, text="Order Summary", 
            font=("Helvetica", 18, "bold"), 
            fg="white", bg=colors["primary"]).pack(anchor="w")

    if order.table_id:
        table = data_manager.get_table_by_id(order.table_id)
        if table:
            table_info = tk.Frame(header_frame, bg=colors["primary"])
            table_info.pack(side=tk.RIGHT)
            
            tk.Label(table_info, text=f"Table: {table.name}", 
                    font=("Helvetica", 14, "bold"),
                    fg="white", bg=colors["primary"]).pack()
    
    content_frame = tk.Frame(checkout_window, bg=colors["background"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    items_frame = tk.LabelFrame(content_frame, text="Order Items", 
                               font=("Helvetica", 12, "bold"),
                               fg=colors["primary"],
                               bg=colors["background"])
    items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    items_canvas = tk.Canvas(items_frame, bg=colors["background"], highlightthickness=0)
    items_scrollbar = tk.Scrollbar(items_frame, orient="vertical", command=items_canvas.yview)
    items_scrollable = tk.Frame(items_canvas, bg=colors["background"])
    
    items_scrollable.bind(
        "<Configure>",
        lambda e: items_canvas.configure(
            scrollregion=items_canvas.bbox("all")
        )
    )
    
    items_canvas.create_window((0, 0), window=items_scrollable, anchor="nw")
    items_canvas.configure(yscrollcommand=items_scrollbar.set)
    
    items_canvas.pack(side="left", fill="both", expand=True)
    items_scrollbar.pack(side="right", fill="y")
    
    for item in order.items:
        item_frame = tk.Frame(items_scrollable, bg=colors["background"], pady=5)
        item_frame.pack(fill=tk.X)
        
        tk.Label(item_frame, text=f"{item.quantity}x", 
                width=3, bg=colors["background"]).pack(side=tk.LEFT)
        
        name_text = item.get_display_name()
        tk.Label(item_frame, text=name_text, 
                wraplength=300, justify=tk.LEFT,
                bg=colors["background"]).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(item_frame, text=f"₱{item.get_total():.2f}", 
                bg=colors["background"]).pack(side=tk.RIGHT)
    
    payment_frame = tk.LabelFrame(content_frame, text="Payment Details", 
                                 font=("Helvetica", 12, "bold"),
                                 fg=colors["primary"],
                                 bg=colors["background"])
    payment_frame.pack(fill=tk.X, pady=10)
    
    subtotal = sum(item.get_total() for item in order.items)
    subtotal_frame = tk.Frame(payment_frame, bg=colors["background"])
    subtotal_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(subtotal_frame, text="Subtotal:", 
            bg=colors["background"]).pack(side=tk.LEFT)
    tk.Label(subtotal_frame, text=f"₱{subtotal:.2f}", 
            bg=colors["background"]).pack(side=tk.RIGHT)
    
    if order.discount_percent > 0:
        discount_frame = tk.Frame(payment_frame, bg=colors["background"])
        discount_frame.pack(fill=tk.X, padx=10, pady=5)
        
        discount_amount = order.get_discount_amount()
        tk.Label(discount_frame, 
                text=f"{order.discount_type} Discount ({order.discount_percent}%):", 
                bg=colors["background"]).pack(side=tk.LEFT)
        tk.Label(discount_frame, 
                text=f"-₱{discount_amount:.2f}", 
                fg=colors["success"],
                bg=colors["background"]).pack(side=tk.RIGHT)
    
    tax = order.get_total() * 0.12
    tax_frame = tk.Frame(payment_frame, bg=colors["background"])
    tax_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(tax_frame, text="Tax (12%):", 
            bg=colors["background"]).pack(side=tk.LEFT)
    tk.Label(tax_frame, text=f"₱{tax:.2f}", 
            bg=colors["background"]).pack(side=tk.RIGHT)
    
    total = order.get_total() + tax
    total_frame = tk.Frame(payment_frame, bg=colors["background"])
    total_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Label(total_frame, text="Total:", 
            font=("Helvetica", 14, "bold"),
            fg=colors["primary"],
            bg=colors["background"]).pack(side=tk.LEFT)
    tk.Label(total_frame, text=f"₱{total:.2f}", 
            font=("Helvetica", 14, "bold"),
            fg=colors["primary"],
            bg=colors["background"]).pack(side=tk.RIGHT)
    
    buttons_frame = tk.Frame(checkout_window, bg=colors["background"], padx=20, pady=20)
    buttons_frame.pack(fill=tk.X)
    
    def confirm_order():
        for item in order.items:
            product = data_manager.get_product_by_id(item.product.id)
            if not product or product.stock < item.quantity:
                messagebox.showwarning("Stock Issue", 
                                      f"Sorry, {product.name if product else 'an item'} is no longer available in the requested quantity.")
                return
        
        if order.table_id:
            data_manager.assign_order_to_table(order, order.table_id)
        
        data_manager.save_order(order)
        
        total_with_tax = order.get_total() + (order.get_total() * 0.12)
        messagebox.showinfo("Order Placed", 
                           f"Order #{order.id} has been placed successfully! Total: ₱{total_with_tax:.2f}")
        
        checkout_window.destroy()
        new_order_callback()
    
    tk.Button(buttons_frame, text="Confirm Order", 
             bg=colors["success"], fg="white", 
             font=("Helvetica", 14, "bold"),
             height=2,
             activebackground=colors["secondary"],
             command=confirm_order).pack(fill=tk.X, pady=(0, 10))
    
    tk.Button(buttons_frame, text="Cancel", 
             bg=colors["secondary"], fg="white", 
             font=("Helvetica", 12),
             activebackground=colors["accent"],
             command=checkout_window.destroy).pack(fill=tk.X)

