import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque
import heapq
from datetime import datetime, timedelta
import math
class ParkingLotSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Parking System")
        # Initialize parking lot (5x5 grid)
        # 0: Empty, 1: Car, 2: Bike, 3: Reserved, 4: SUV, 5: Electric
        self.parking_lot = [[0 for _ in range(5)] for _ in range(5)]
        # Store parking times and spot names
        self.parking_times = {}  # (row, col): datetime
        self.spot_names = self.generate_spot_names()
        # Reserve some spots (marked as 3)
        self.parking_lot[0][0] = 3  # Reserved for handicapped
        self.parking_lot[0][1] = 3  # Reserved for VIP
        # Define rates and search preferences for different vehicle types
        self.rates = {
            "Car": {
                "hourly_rate": 100,
                "description": "AC Parking",
                "search_preference": "bfs"  # Cars prefer closest spots to entrance
            },
            "Bike": {
                "hourly_rate": 50,
                "description": "Regular Parking",
                "search_preference": "dfs"  # Bikes can navigate to farther spots easily
            },
            "SUV": {
                "hourly_rate": 150,
                "description": "Premium Parking",
                "search_preference": "astar"  # SUVs need optimal path considering space
            },
            "Electric": {
                "hourly_rate": 80,
                "description": "EV Parking with Charging",
                "search_preference": "astar"  # EVs need optimal spots near charging points
            }
        }
        self.setup_gui()
    def generate_spot_names(self):
        """Generate names for parking spots (A1-E5)"""
        names = {}
        for row in range(5):
            for col in range(5):
                names[(row, col)] = f"{chr(65 + row)}{col + 1}"
        return names
    def setup_gui(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Vehicle Details", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        # Vehicle Type Selection
        ttk.Label(input_frame, text="Vehicle Type:").grid(row=0, column=0, padx=5, pady=5)
        self.vehicle_type = ttk.Combobox(input_frame, values=list(self.rates.keys()))
        self.vehicle_type.grid(row=0, column=1, padx=5, pady=5)
        self.vehicle_type.set("Car")
        self.vehicle_type.bind('<<ComboboxSelected>>', self.update_rate_display)
        # Rate Display
        self.rate_label = ttk.Label(input_frame, text="")
        self.rate_label.grid(row=0, column=2, padx=5, pady=5)
        # Buttons Frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(button_frame, text="Check In", command=self.check_in_vehicle).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Check Out", command=self.checkout_vehicle).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset Lot", command=self.reset_lot).pack(side=tk.LEFT, padx=5)
        # Parking Lot Display Frame
        display_frame = ttk.LabelFrame(self.root, text="Parking Lot", padding="10")
        display_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.spot_labels = []
        for row in range(5):
            label_row = []
            for col in range(5):
                spot_frame = ttk.Frame(display_frame, borderwidth=1, relief="solid")
                spot_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                spot_frame.grid_columnconfigure(0, weight=1)
                spot_frame.grid_rowconfigure(0, weight=1)
                name_label = ttk.Label(spot_frame, text=self.spot_names[(row, col)])
                name_label.grid(row=0, column=0, padx=2, pady=1)
                status_label = ttk.Label(spot_frame, text="Empty")
                status_label.grid(row=1, column=0, padx=2, pady=1)
                time_label = ttk.Label(spot_frame, text="")
                time_label.grid(row=2, column=0, padx=2, pady=1)
                label_row.append((name_label, status_label, time_label))
            self.spot_labels.append(label_row)
        # Configure grid weights
        for i in range(5):
            display_frame.grid_columnconfigure(i, weight=1)
            display_frame.grid_rowconfigure(i, weight=1)
        self.update_rate_display()
        self.update_display()
        # Start timer for updating parking durations
        self.update_parking_times()
    def update_parking_times(self):
        """Update the displayed parking duration for occupied spots"""
        current_time = datetime.now()
        for row in range(5):
            for col in range(5):
                _, _, time_label = self.spot_labels[row][col]
                if (row, col) in self.parking_times:
                    duration = current_time - self.parking_times[(row, col)]
                    hours = duration.total_seconds() / 3600
                    time_label.config(text=f"Duration: {hours:.1f}h")
                else:
                    time_label.config(text="")
        # Update every minute
        self.root.after(60000, self.update_parking_times)
    def update_rate_display(self, event=None):
        """Update the displayed rate for the selected vehicle type"""
        vehicle_type = self.vehicle_type.get()
        rate_info = self.rates[vehicle_type]
        self.rate_label.config(text=f"Rate: Rs. {rate_info['hourly_rate']}/hour ({rate_info['description']})")
    def update_display(self):
        """Update the parking lot display"""
        vehicle_types = {0: "Empty", 1: "Car", 2: "Bike", 3: "Reserved", 4: "SUV", 5: "Electric"}  
        for row in range(5):
            for col in range(5):
                _, status_label, _ = self.spot_labels[row][col]
                spot_status = vehicle_types[self.parking_lot[row][col]]
                status_label.config(text=spot_status)
                
                if spot_status == "Empty":
                    status_label.config(foreground="green")
                elif spot_status == "Reserved":
                    status_label.config(foreground="red")
                else:
                    status_label.config(foreground="blue")
    def calculate_heuristic(self, row, col):
        """Calculate heuristic for A* search (Manhattan distance to entrance)"""
        return abs(row) + abs(col)
    def find_best_spot(self, vehicle_type):
        """Find the best parking spot using the appropriate search algorithm"""
        search_preference = self.rates[vehicle_type]["search_preference"]
        def is_suitable_spot(row, col):
            if self.parking_lot[row][col] != 0:
                return False
            if vehicle_type == "Electric":
                return row + col <= 3
            elif vehicle_type == "SUV":
                return row == 0 or row == 4 or col == 0 or col == 4
            return True
        if search_preference == "bfs":
            return self.bfs_search(is_suitable_spot)
        elif search_preference == "dfs":
            return self.dfs_search(is_suitable_spot)
        else:
            return self.astar_search(is_suitable_spot)
    def bfs_search(self, is_suitable_spot):
        """BFS implementation for finding parking spots"""
        queue = deque([(0, 0)])
        visited = set()
        while queue:
            row, col = queue.popleft()
            if (row, col) not in visited:
                visited.add((row, col))
                if is_suitable_spot(row, col):
                    return row, col
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < 5 and 0 <= new_col < 5 and 
                        (new_row, new_col) not in visited):
                        queue.append((new_row, new_col))
        return None
    def dfs_search(self, is_suitable_spot):
        """DFS implementation for finding parking spots"""
        def dfs_recursive(row, col, visited):
            if (row, col) in visited:
                return None
            visited.add((row, col))
            if is_suitable_spot(row, col):
                return (row, col)
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < 5 and 0 <= new_col < 5):
                    result = dfs_recursive(new_row, new_col, visited)
                    if result:
                        return result
            return None
        return dfs_recursive(0, 0, set())
    
    def astar_search(self, is_suitable_spot):
        """A* implementation for finding parking spots"""
        start = (0, 0)
        open_set = [(self.calculate_heuristic(0, 0), 0, start)]
        closed_set = set()
        g_scores = {start: 0}
        while open_set:
            current_f, current_g, (row, col) = heapq.heappop(open_set)
            if (row, col) in closed_set:
                continue
            closed_set.add((row, col))
            if is_suitable_spot(row, col):
                return row, col
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 5 and 0 <= new_col < 5:
                    neighbor = (new_row, new_col)
                    tentative_g = current_g + 1
                    if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                        g_scores[neighbor] = tentative_g
                        f_score = tentative_g + self.calculate_heuristic(new_row, new_col)
                        heapq.heappush(open_set, (f_score, tentative_g, neighbor))
        
        return None
    
    def check_in_vehicle(self):
        """Handle vehicle check-in process"""
        vehicle_type = self.vehicle_type.get()
        vehicle_code = {"Car": 1, "Bike": 2, "SUV": 4, "Electric": 5}[vehicle_type]
        spot = self.find_best_spot(vehicle_type)
        if spot:
            row, col = spot
            self.parking_lot[row][col] = vehicle_code
            self.parking_times[(row, col)] = datetime.now()
            self.update_display()
            rate_info = self.rates[vehicle_type]
            spot_name = self.spot_names[(row, col)]
            messagebox.showinfo(
                "Check-In Complete", 
                f"Spot assigned: {spot_name}\n"
                f"Type: {rate_info['description']}\n"
                f"Rate: Rs. {rate_info['hourly_rate']}/hour\n"
                f"Check-in time: {datetime.now().strftime('%H:%M:%S')}"
            )
        else:
            messagebox.showerror("No Spots", "No suitable parking spots available!")
    def checkout_vehicle(self):
        """Handle vehicle checkout process"""
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Vehicle Checkout")
        checkout_window.geometry("300x150")
        ttk.Label(checkout_window, text="Enter Spot Name:").pack(padx=5, pady=5)
        spot_entry = ttk.Entry(checkout_window)
        spot_entry.pack(padx=5, pady=5)
        def process_checkout():
            spot_name = spot_entry.get().upper()
            spot_found = False
            for (row, col), name in self.spot_names.items():
                if name == spot_name and self.parking_lot[row][col] != 0:
                    vehicle_code = self.parking_lot[row][col]
                    vehicle_type = {1: "Car", 2: "Bike", 4: "SUV", 5: "Electric"}[vehicle_code]
                    rate_info = self.rates[vehicle_type]
                    # Calculate actual duration
                    check_in_time = self.parking_times[(row, col)]
                    check_out_time = datetime.now()
                    duration = check_out_time - check_in_time
                    hours_parked = duration.total_seconds() / 3600
                    # Calculate charges
                    final_charge = rate_info['hourly_rate'] * math.ceil(hours_parked)
                    messagebox.showinfo(
                        "Checkout Complete",
                        f"Spot: {spot_name}\n"
                        f"Vehicle: {vehicle_type}\n"
                        f"Type: {rate_info['description']}\n"
                        f"Check-in: {check_in_time.strftime('%H:%M:%S')}\n"
                        f"Check-out: {check_out_time.strftime('%H:%M:%S')}\n"
                        f"Duration: {hours_parked:.2f} hours\n"
                        f"Rate: Rs. {rate_info['hourly_rate']}/hour\n"
                        f"Total charges: Rs. {final_charge:.2f}"
                    )
                    self.parking_lot[row][col] = 0
                    del self.parking_times[(row, col)]
                    spot_found = True
                    break
            if not spot_found:
                messagebox.showerror("Error", "Invalid spot or spot is empty!")
            self.update_display()
            checkout_window.destroy()
        ttk.Button(checkout_window, text="Process Checkout", command=process_checkout).pack(pady=10)
        ttk.Button(checkout_window, text="Cancel", command=checkout_window.destroy).pack(pady=5)
    def reset_lot(self):
        """Reset the parking lot to initial state"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the parking lot? This will clear all parked vehicles."):
            self.parking_lot = [[0 for _ in range(5)] for _ in range(5)]
            self.parking_lot[0][0] = 3  # Reserved for handicapped
            self.parking_lot[0][1] = 3  # Reserved for VIP
            self.parking_times.clear()
            self.update_display()
            messagebox.showinfo("Reset Complete", "Parking lot has been reset to initial state!")
def main():
    root = tk.Tk()
    app = ParkingLotSystem(root)
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Center the window on screen
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Configure grid weights for resizing
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    
    # Add menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Reset Lot", command=app.reset_lot)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Admin menu for rate management
    def update_rates():
        rate_window = tk.Toplevel(root)
        rate_window.title("Update Parking Rates")
        rate_window.geometry("400x300")
        rate_window.transient(root)  # Make window modal
        # Center the window
        rate_window.geometry(f"+{center_x + 200}+{center_y + 150}")
        # Add heading
        ttk.Label(rate_window, text="Update Parking Rates", font=('Arial', 12, 'bold')).pack(pady=10)
        # Create frame for rate inputs
        rate_frame = ttk.Frame(rate_window)
        rate_frame.pack(padx=20, pady=10)
        rate_entries = {}
        # Create entries for each vehicle type
        for idx, (vehicle, info) in enumerate(app.rates.items()):
            ttk.Label(rate_frame, text=f"{vehicle} Rate:").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            rate_entry = ttk.Entry(rate_frame)
            rate_entry.insert(0, str(info['hourly_rate']))
            rate_entry.grid(row=idx, column=1, padx=5, pady=5)
            ttk.Label(rate_frame, text="Rs./hour").grid(row=idx, column=2, padx=5, pady=5)
            rate_entries[vehicle] = rate_entry
        def save_rates():
            try:
                for vehicle, entry in rate_entries.items():
                    new_rate = float(entry.get())
                    if new_rate <= 0:
                        raise ValueError(f"Invalid rate for {vehicle}")
                    app.rates[vehicle]['hourly_rate'] = new_rate
                app.update_rate_display()
                messagebox.showinfo("Success", "Parking rates updated successfully!")
                rate_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Please enter valid rates (positive numbers only)!\n{str(e)}")
        # Add buttons
        button_frame = ttk.Frame(rate_window)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save Changes", command=save_rates).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=rate_window.destroy).pack(side=tk.LEFT, padx=5)
    admin_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Admin", menu=admin_menu)
    admin_menu.add_command(label="Update Rates", command=update_rates)
    # Help menu
    def show_help():
        help_window = tk.Toplevel(root)
        help_window.title("Parking System Help")
        help_window.geometry("500x400")
        help_window.transient(root)
        help_text = """
Smart Parking System Help

1. Vehicle Types and Rates:
   - Car: Standard vehicle parking with AC
   - Bike: Two-wheeler parking
   - SUV: Large vehicle parking
   - Electric: EV parking with charging facilities

2. Parking Features:
   - Automated spot assignment based on vehicle type
   - Real-time parking duration tracking
   - Dynamic rate calculation
   - Reserved spots for special needs

3. How to Park:
   a) Select your vehicle type
   b) Click "Check In"
   c) Note your assigned spot number

4. How to Check Out:
   a) Click "Check Out"
   b) Enter your spot number
   c) View and pay the calculated charges based on actual duration

5. Special Features:
   - Intelligent spot allocation algorithms
   - Real-time duration tracking
   - Automatic rate calculation
   - Reserved spots (A1, A2) for handicapped and VIP parking

6. Tips:
   - Electric vehicles get spots near charging points
   - SUVs are assigned wider spots
   - Regular maintenance times: 2:00 AM - 4:00 AM daily

Note: For emergencies or assistance, please contact parking staff.
        """
        # Create text widget with scrollbar
        text_frame = ttk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        # Pack widgets
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Insert help text and disable editing
        text_widget.insert(tk.END, help_text)
        text_widget.configure(state='disabled')
        # Add close button
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)
    # Add help menu items
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="User Guide", command=show_help)
    help_menu.add_separator()
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", 
        "Smart Parking System v1.0\n\n"
        "An intelligent parking management solution\n"
        "featuring automated spot allocation and\n"
        "real-time duration tracking.\n\n"
        "© 2024 Parking Solutions"))
    # Start the application
    root.mainloop()
if __name__ == "__main__":
    main()
