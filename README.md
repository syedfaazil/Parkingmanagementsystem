# Smart Parking System

A Python-based intelligent parking management system with a graphical interface, automated spot allocation, dynamic rate management, and real-time duration tracking. This project uses **Tkinter** for the GUI and implements multiple search algorithms for optimal parking spot assignment based on vehicle type.

---

## Features

- **Automated Spot Assignment:** Allocates the best available spot using **BFS**, **DFS**, or **A*** search algorithms depending on vehicle type.
- **Vehicle Type Support:** Supports **Cars**, **Bikes**, **SUVs**, and **Electric Vehicles**, each with unique parking preferences and rates.
- **Dynamic Rate Management:** Admin interface to update hourly rates for each vehicle type.
- **Real-Time Duration Tracking:** Displays live parking durations for all occupied spots.
- **Reserved Parking:** Designated spots for handicapped and VIP users.
- **Interactive GUI:** Easy-to-use interface for check-in, check-out, and lot management.
- **Help & User Guide:** Built-in help window and about section for user assistance.

---

## Getting Started

### Prerequisites

- Python **3.7** or higher
- Tkinter (usually included with Python)
- No external dependencies required

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-parking-system.git
cd smart-parking-system

# Run the application
python parkingmanagement.py
```

---

## Usage

### Check-In a Vehicle

1. Select the vehicle type from the dropdown (**Car**, **Bike**, **SUV**, **Electric**).
2. Click **Check In**.
3. The system will assign the optimal spot and display the spot number, rate, and check-in time.

### Check-Out a Vehicle

1. Click **Check Out**.
2. Enter your assigned spot number (e.g., `A3`, `B4`).
3. The system will calculate the total charges based on duration and display a summary.

### Admin: Update Rates

1. Go to **Admin > Update Rates** in the menu bar.
2. Update hourly rates for each vehicle type.
3. Click **Save Changes**.

### Reset Lot

- Use the **Reset Lot** button or **File > Reset Lot** to clear all parked vehicles and restore reserved spots.

### Help

- Access **Help > User Guide** for detailed instructions and tips.
- **Help > About** provides version and credits information.

---

## Parking Lot Details

- **5x5 Grid** (25 spots)
- **Reserved Spots:**
  - `A1`: Handicapped
  - `A2`: VIP
- **Spot Naming:** `A1–E5` (Rows `A–E`, Columns `1–5`)
- **Vehicle-Specific Allocation:**
  - **Car:** Closest to entrance (**BFS**)
  - **Bike:** Flexible, can use farther spots (**DFS**)
  - **SUV:** Prefers edge spots (**A***)
  - **Electric:** Spots near charging points (**A***)

---

## Algorithms

| Vehicle Type | Search Algorithm | Allocation Preference                     |
|--------------|------------------|-------------------------------------------|
| Car          | BFS              | Closest to entrance                       |
| Bike         | DFS              | Any available, including farther spots    |
| SUV          | A*               | Edge spots, optimal path                  |
| Electric     | A*               | Near charging points (entrance side)      |

---

## Customization

- **Change Grid Size:** Modify the `self.parking_lot` initialization in the code.
- **Add More Vehicle Types:** Update the `self.rates` dictionary and spot assignment logic.
- **Reserved Spots:** Adjust the initialization in `reset_lot()` and `__init__()` methods.

---

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0):

> Copyright 2025 Parking Solutions
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at:
>
> [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)
>
> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

---

> **Enjoy using the Smart Parking System! 🚗🚀**
