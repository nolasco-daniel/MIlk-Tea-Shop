import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def show_stock_management(parent, data_manager, colors):
    stock_window = tk.Toplevel(parent)
    stock_window.title("Stock Management")
    stock_window.geometry("800x600")
    stock_window.configure(bg=colors["background"])
    stock_window.transient(parent)
    stock_window.grab_set()
    
    header_frame = tk.Frame(stock_window, bg=colors["primary"], padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    
    tk.Label(header_frame, text="Stock Management", 
            font=("Helvetica", 18, "bold"), 
            fg="white", bg=colors["primary"]).pack(anchor="w")
    
    content_frame = tk.Frame(stock_window, bg=colors["background"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    columns = ("id", "name", "category", "price", "stock")
    tree = ttk.Treeview(content_frame, columns=columns, show="headings")
    
    tree.heading("id", text="ID")
    tree.heading("name", text="Product Name")
    tree.heading("category", text="Category")
    tree.heading("price", text="Price")
    tree.heading("stock", text="Stock")
    
    tree.column("id", width=50)
    tree.column("name", width=200)
    tree.column("category", width=100)
    tree.column("price", width=100)
    tree.column("stock", width=100)
    
    scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    for product in data_manager.products:
        tree.insert("", tk.END, values=(
            product.id, 
            product.name, 
            product.category, 
            f"₱{product.price:.2f}", 
            product.stock
        ))
    
    buttons_frame = tk.Frame(stock_window, bg=colors["background"], padx=20, pady=20)
    buttons_frame.pack(fill=tk.X)
    
    def update_stock():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection Required", "Please select a product to update stock.")
            return
        
        item_values = tree.item(selected_item[0], "values")
        product_id = int(item_values[0])
        product = data_manager.get_product_by_id(product_id)
        
        if not product:
            messagebox.showerror("Error", "Product not found.")
            return
        
        new_stock = simpledialog.askinteger("Update Stock", 
                                           f"Enter new stock for {product.name}:",
                                           parent=stock_window,
                                           minvalue=0,
                                           initialvalue=product.stock)
        
        if new_stock is not None:
            product.stock = new_stock
            
            tree.item(selected_item[0], values=(
                product.id, 
                product.name, 
                product.category, 
                f"₱{product.price:.2f}", 
                product.stock
            ))
            
            messagebox.showinfo("Stock Updated", f"Stock for {product.name} updated to {new_stock}.")
    
    def refresh_stock_view():
        for item in tree.get_children():
            tree.delete(item)
        
        for product in data_manager.products:
            tree.insert("", tk.END, values=(
                product.id, 
                product.name, 
                product.category, 
                f"₱{product.price:.2f}", 
                product.stock
            ))
    
    update_btn = tk.Button(buttons_frame, text="Update Stock", 
                          bg=colors["primary"], fg="white", 
                          font=("Helvetica", 12, "bold"),
                          command=update_stock)
    update_btn.pack(side=tk.LEFT, padx=5)
    
    refresh_btn = tk.Button(buttons_frame, text="Refresh", 
                           bg=colors["secondary"], fg="white", 
                           font=("Helvetica", 12, "bold"),
                           command=refresh_stock_view)
    refresh_btn.pack(side=tk.LEFT, padx=5)
    
    close_btn = tk.Button(buttons_frame, text="Close", 
                         bg=colors["accent"], fg="white", 
                         font=("Helvetica", 12, "bold"),
                         command=stock_window.destroy)
    close_btn.pack(side=tk.RIGHT, padx=5)

