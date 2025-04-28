# Parking Management System

An advanced Parking Management application built using Python's Tkinter library, featuring algorithmic handling of parking slot management, vehicle entry/exit tracking, and fee calculation based on parking duration.

## Features

-> Vehicle Entry and Exit Management
-> Dynamic Slot Allocation (First-Come-First-Served)
-> Real-Time Parking Slot Availability Tracking
-> Automatic Calculation of Parking Duration and Fees
-> User-Friendly Graphical Interface (GUI)
-> Robust backend logic for accurate time and fee management

## Algorithms and Techniques Used

- **Queue-Based Slot Allocation:**  
  Slots are assigned dynamically to vehicles based on availability, following a first-available strategy.
  
- **Greedy Approach for Slot Assignment:**  
  Immediate assignment without checking for future optimization — fast and efficient.

- **Time-Based Billing Algorithm:**  
  Calculates parking fees based on the difference between entry and exit timestamps.

- **Tkinter Event-Driven Programming:**  
  GUI events are handled efficiently for user interaction.

## How to Run

Make sure you have Python 3 installed. Tkinter is already included in most Python installations.

Run the following command:

```bash
python parkingmanagement.py
