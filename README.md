# TQM-Based Parking Management System

A desktop-based Parking Management System developed using **Python, Tkinter, and SQLite** with the principles of **Total Quality Management (TQM)**.

The main quality objective of this project is to:

> Reduce duplicate vehicle entries and improve parking data accuracy through defect prevention, standardization, quality monitoring, and continuous improvement.

---

## Project Objective

Traditional parking processes can suffer from problems such as:

- Duplicate vehicle entries
- Duplicate parking IDs
- Invalid vehicle information
- Incorrect phone numbers
- Parking slot conflicts
- Incorrect vehicle entry and exit records
- Inconsistent vehicle-number formats

This project focuses on preventing these defects before incorrect data reaches the database.

### Primary Quality Target

**Actual Active Duplicate Vehicles = 0**

---

# Technologies Used

- Python
- Tkinter
- SQLite
- Git
- GitHub
- Python unittest

---

# Main Modules

The application contains the following modules:

### Dashboard

Displays live parking statistics:

- Total parking slots
- Available slots
- Occupied slots

### Add Vehicle

Allows an operator to register a new vehicle.

Includes:

- Required-field validation
- Parking ID validation
- Vehicle-number normalization
- Owner-name validation
- Phone-number validation
- Search Before Add
- Duplicate detection
- Parking-slot verification
- Confirmation dialog
- Safe database transaction

### Search Vehicle

Allows parking records to be searched using:

- Parking ID
- Vehicle Number

### Vehicle Exit

Provides a controlled vehicle-exit process.

Includes:

- Active vehicle verification
- Exit confirmation
- Double-exit prevention
- Exit-time recording
- Automatic parking-slot release
- Transaction-based updates

### Parking Records

Displays parking history including:

- Parking ID
- Vehicle number
- Owner
- Phone number
- Vehicle type
- Parking slot
- Entry time
- Exit time
- Status

Records can be filtered and searched.

### Parking Slots

Displays parking-slot status.

The system contains:

- 20 Car Slots: A01 - A20
- 20 Bike Slots: B01 - B20

Total:

**40 Parking Slots**

Each slot can have:

- Available
- Occupied

status.

### Quality Dashboard

Displays TQM quality-performance indicators including:

- Successful Entries
- Vehicle Exits
- Duplicate Attempts
- Validation Failures
- Slot Conflicts
- Actual Active Duplicates
- Duplicate Prevention Rate
- Entry Success Rate
- Data Quality Status

It also displays recent quality events.

---

# Core TQM Features

## 1. Unique ID Constraints

Every Parking ID must be unique.

SQLite provides a database-level UNIQUE constraint.

This prevents duplicate Parking IDs even if an application-level check fails.

---

## 2. Pre-Add Validation

Input is validated before insertion into the database.

The system validates:

- Required fields
- Parking ID
- Vehicle number
- Owner name
- Phone number
- Vehicle type
- Parking slot

This follows the TQM principle of:

**Defect Prevention at Source**

---

## 3. Search Before Add

Before a vehicle is inserted, the system checks whether the same vehicle is already actively parked.

If an active record exists, the new entry is prevented.

This reduces duplicate vehicle records.

---

## 4. Confirmation Dialogs

Before important operations are completed, the operator is asked to verify the information.

Confirmation is used during:

- Vehicle Entry
- Vehicle Exit

This reduces human-entry errors.

---

# Vehicle Number Standardization

Different representations of a vehicle number are normalized.

For example:

```text
uk04ab1234
UK04 AB 1234
UK04-AB-1234