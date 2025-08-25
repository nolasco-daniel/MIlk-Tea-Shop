import tkinter as tk
from tkinter import ttk, messagebox

def show_table_management(parent, data_manager, colors):
    table_window = tk.Toplevel(parent)
    table_window.title("Table Management")
    table_window.geometry("800x600")
    table_window.configure(bg=colors["background"])
    table_window.transient(parent)
    table_window.grab_set()
    
    header_frame = tk.Frame(table_window, bg=colors["primary"], padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    
    tk.Label(header_frame, text="Table Management", 
            font=("Helvetica", 18, "bold"), 
            fg="white", bg=colors["primary"]).pack(anchor="w")
    
    content_frame = tk.Frame(table_window, bg=colors["background"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    tables_frame = tk.Frame(content_frame, bg=colors["background"])
    tables_frame.pack(fill=tk.BOTH, expand=True)
    
    table_frames = []
    row, col = 0, 0
    max_cols = 4
    
    for table in data_manager.tables:
        table_frame = create_table_card(tables_frame, table, colors, data_manager)
        table_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        table_frames.append(table_frame)
        
        col += 1
        if col >= max_cols:
            col = 0
            row += 1
    
    for i in range(max_cols):
        tables_frame.columnconfigure(i, weight=1)
    
    buttons_frame = tk.Frame(table_window, bg=colors["background"], padx=20, pady=20)
    buttons_frame.pack(fill=tk.X)
    
    def refresh_tables():
        for frame in table_frames:
            frame.destroy()
        
        row, col = 0, 0
        table_frames.clear()
        
        for table in data_manager.tables:
            table_frame = create_table_card(tables_frame, table, colors, data_manager)
            table_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            table_frames.append(table_frame)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    refresh_btn = tk.Button(buttons_frame, text="Refresh", 
                           bg=colors["secondary"], fg="white", 
                           font=("Helvetica", 12, "bold"),
                           activebackground=colors["accent"],
                           command=refresh_tables)
    refresh_btn.pack(side=tk.LEFT, padx=5)
    
    close_btn = tk.Button(buttons_frame, text="Close", 
                         bg=colors["primary"], fg="white", 
                         font=("Helvetica", 12, "bold"),
                         activebackground=colors["secondary"],
                         command=table_window.destroy)
    close_btn.pack(side=tk.RIGHT, padx=5)

def create_table_card(parent, table, colors, data_manager):
    bg_color = "white"
    status_color = colors["success"]
    
    if table.status == "Occupied":
        status_color = colors["danger"]
    elif table.status == "Reserved":
        status_color = colors["accent"]
    
    card = tk.Frame(parent, bg=bg_color, relief=tk.RAISED, borderwidth=1)
    card.configure(padx=15, pady=15, width=150, height=150)
    card.pack_propagate(False)
    
    name_label = tk.Label(card, text=table.name, 
                         font=("Helvetica", 14, "bold"), 
                         fg=colors["primary"],
                         bg=bg_color)
    name_label.pack(fill=tk.X)
    
    capacity_label = tk.Label(card, text=f"Capacity: {table.capacity}", 
                             font=("Helvetica", 10), 
                             fg=colors["light_text"],
                             bg=bg_color)
    capacity_label.pack(fill=tk.X)
    
    status_frame = tk.Frame(card, bg=status_color, height=5)
    status_frame.pack(fill=tk.X, pady=8)
    
    status_label = tk.Label(card, text=f"Status: {table.status}", 
                           font=("Helvetica", 12), 
                           fg=colors["text"],
                           bg=bg_color)
    status_label.pack(fill=tk.X)
    
    if table.status == "Occupied" and table.current_order:
        order_label = tk.Label(card, text=f"Order: #{table.current_order.id}", 
                              font=("Helvetica", 10), 
                              fg=colors["light_text"],
                              bg=bg_color)
        order_label.pack(fill=tk.X, pady=(5, 0))
        
        items_count = len(table.current_order.items)
        items_label = tk.Label(card, text=f"Items: {items_count}", 
                              font=("Helvetica", 10), 
                              fg=colors["light_text"],
                              bg=bg_color)
        items_label.pack(fill=tk.X)
    
    buttons_frame = tk.Frame(card, bg=bg_color)
    buttons_frame.pack(fill=tk.X, pady=(10, 0))
    
    if table.status == "Available":
        reserve_btn = tk.Button(buttons_frame, text="Reserve", 
                               bg=colors["accent"], fg="white",
                               font=("Helvetica", 10),
                               command=lambda: reserve_table(table))
        reserve_btn.pack(fill=tk.X)
    elif table.status == "Occupied":
        clear_btn = tk.Button(buttons_frame, text="Clear Table", 
                             bg=colors["danger"], fg="white",
                             font=("Helvetica", 10),
                             command=lambda: clear_table(table))
        clear_btn.pack(fill=tk.X)
    elif table.status == "Reserved":
        clear_btn = tk.Button(buttons_frame, text="Cancel Reservation", 
                             bg=colors["secondary"], fg="white",
                             font=("Helvetica", 10),
                             command=lambda: clear_table(table))
        clear_btn.pack(fill=tk.X)
    
    def reserve_table(table):
        table.reserve()
        status_frame.config(bg=colors["accent"])
        status_label.config(text=f"Status: {table.status}")
        
        for widget in buttons_frame.winfo_children():
            widget.destroy()
        
        clear_btn = tk.Button(buttons_frame, text="Cancel Reservation", 
                             bg=colors["secondary"], fg="white",
                             font=("Helvetica", 10),
                             command=lambda: clear_table(table))
        clear_btn.pack(fill=tk.X)
    
    def clear_table(table):
        if table.status == "Occupied":
            result = messagebox.askyesno("Clear Table", 
                                        f"Are you sure you want to clear {table.name}? This will mark the order as completed.")
            if not result:
                return
        
        data_manager.clear_table(table.id)
        
        status_frame.config(bg=colors["success"])
        status_label.config(text=f"Status: {table.status}")
        
        for widget in card.winfo_children():
            if widget not in [name_label, capacity_label, status_frame, status_label, buttons_frame]:
                widget.destroy()
        
        for widget in buttons_frame.winfo_children():
            widget.destroy()
        
        reserve_btn = tk.Button(buttons_frame, text="Reserve", 
                               bg=colors["accent"], fg="white",
                               font=("Helvetica", 10),
                               command=lambda: reserve_table(table))
        reserve_btn.pack(fill=tk.X)
    
    return card

def select_table_dialog(parent, data_manager, colors, callback):
    table_dialog = tk.Toplevel(parent)
    table_dialog.title("Select Table")
    table_dialog.geometry("600x500")
    table_dialog.configure(bg=colors["background"])
    table_dialog.transient(parent)
    table_dialog.grab_set()
    
    header_frame = tk.Frame(table_dialog, bg=colors["primary"], padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    
    tk.Label(header_frame, text="Select a Table", 
            font=("Helvetica", 18, "bold"), 
            fg="white", bg=colors["primary"]).pack(anchor="w")
    
    content_frame = tk.Frame(table_dialog, bg=colors["background"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    available_tables = data_manager.get_available_tables()
    
    if not available_tables:
        tk.Label(content_frame, text="No tables available. Please clear a table first.", 
                font=("Helvetica", 14),
                fg=colors["danger"],
                bg=colors["background"]).pack(pady=50)
        
        tk.Button(content_frame, text="Close", 
                 bg=colors["primary"], fg="white", 
                 font=("Helvetica", 12, "bold"),
                 command=table_dialog.destroy).pack(pady=10)
        return
    
    tables_frame = tk.Frame(content_frame, bg=colors["background"])
    tables_frame.pack(fill=tk.BOTH, expand=True)
    
    row, col = 0, 0
    max_cols = 3
    
    for table in available_tables:
        table_btn = create_selectable_table(tables_frame, table, colors, 
                                           lambda t=table: select_table(t))
        table_btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        col += 1
        if col >= max_cols:
            col = 0
            row += 1
    
    for i in range(max_cols):
        tables_frame.columnconfigure(i, weight=1)
    
    def select_table(table):
        callback(table.id)
        table_dialog.destroy()
    
    cancel_btn = tk.Button(content_frame, text="Cancel", 
                          bg=colors["secondary"], fg="white", 
                          font=("Helvetica", 12, "bold"),
                          command=table_dialog.destroy)
    cancel_btn.pack(pady=10)

def create_selectable_table(parent, table, colors, on_select):
    btn = tk.Button(parent, bg="white", relief=tk.RAISED, borderwidth=1,
                   command=on_select, padx=15, pady=15, width=15, height=8)
    
    name_label = tk.Label(btn, text=table.name, 
                         font=("Helvetica", 14, "bold"), 
                         fg=colors["primary"],
                         bg="white")
    name_label.pack(pady=(10, 5))
    
    capacity_label = tk.Label(btn, text=f"Capacity: {table.capacity}", 
                             font=("Helvetica", 12), 
                             fg=colors["text"],
                             bg="white")
    capacity_label.pack()
    
    status_frame = tk.Frame(btn, bg=colors["success"], height=5, width=100)
    status_frame.pack(pady=10)
    
    click_label = tk.Label(btn, text="Click to select", 
                          font=("Helvetica", 10, "italic"), 
                          fg=colors["light_text"],
                          bg="white")
    click_label.pack(pady=(10, 0))
    
    return btn

