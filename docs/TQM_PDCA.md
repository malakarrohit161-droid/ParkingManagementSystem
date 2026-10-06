# TQM Implementation in Parking Management System

## 1. Project Overview

The Parking Management System is a desktop application developed using:

- Python
- Tkinter
- SQLite
- Git and GitHub

The project applies Total Quality Management (TQM) principles to improve
the reliability and accuracy of the parking management process.

The primary quality objective of the system is:

> Reduce duplicate vehicle entries and improve parking data accuracy.

The system focuses on defect prevention instead of correcting incorrect
records after they have already been stored.

---

# 2. Problem Statement

Traditional or manually managed parking systems can suffer from problems
such as:

- Duplicate vehicle entries
- Duplicate parking IDs
- Incorrect vehicle numbers
- Invalid phone numbers
- Incorrect parking slot allocation
- Allocation of an already occupied slot
- Incorrect vehicle exit processing
- Inconsistent parking records

These problems reduce data quality and can cause incorrect parking
information.

The Parking Management System therefore uses multiple quality-control
mechanisms to prevent these problems.

---

# 3. Quality Objectives

The major quality objectives of the project are:

1. Reduce duplicate vehicle entries.
2. Maintain zero active duplicate vehicles.
3. Prevent invalid data before database insertion.
4. Standardize vehicle registration numbers.
5. Prevent duplicate parking IDs.
6. Prevent parking slot conflicts.
7. Maintain accurate entry and exit records.
8. Monitor quality-related events.
9. Measure system quality performance.
10. Support continuous improvement using quality data.

---

# 4. TQM Principles Used

## 4.1 Customer Focus

The system provides accurate parking information and reduces errors that
could affect parking users.

Features supporting customer focus include:

- Accurate vehicle records
- Easy vehicle search
- Correct parking slot allocation
- Reliable vehicle entry and exit
- Clear confirmation messages

---

## 4.2 Process Approach

Vehicle parking is treated as a controlled process.

The vehicle entry process follows:

User Input
→ Data Validation
→ Data Normalization
→ Search Before Add
→ Slot Verification
→ User Confirmation
→ Database Verification
→ Database Transaction
→ Quality Logging

This structured process reduces the possibility of errors.

---

## 4.3 Defect Prevention

The system attempts to prevent defects before incorrect information
reaches the database.

Examples include:

- Required field validation
- Parking ID format validation
- Vehicle number validation
- Phone number validation
- Owner name validation
- Search before add
- Duplicate vehicle detection
- Parking slot verification
- Confirmation dialogs
- Database unique constraints

---

## 4.4 Standardization

Vehicle numbers are converted into a standard format.

Examples:

UK04 AB 1234
UK04-AB-1234
uk04ab1234

are normalized to:

UK04AB1234

Parking slots also use standardized identifiers:

A01 - A20 = Car parking slots

B01 - B20 = Bike parking slots

Standardization improves consistency and helps prevent duplicate data.

---

## 4.5 Fact-Based Decision Making

The system records quality events in the quality_log table.

Examples of quality events include:

- VEHICLE_ADDED
- VEHICLE_EXITED
- DUPLICATE_ATTEMPT
- VALIDATION_FAILED
- SLOT_CONFLICT

These records are used to calculate quality metrics instead of making
decisions based only on assumptions.

---

## 4.6 Continuous Improvement

The Quality Dashboard provides measurable information about system
performance.

The collected information can be analyzed to identify common problems
and improve validation rules or parking procedures.

---

## 4.7 Quality Assurance

Quality assurance is supported through:

- Application validation
- Database constraints
- Automated unit tests
- Database integrity tests
- Standardized processes
- Quality event logging

Automated tests help detect regression defects during development.

---

## 4.8 Quality Control

The Quality Dashboard monitors actual quality results.

The dashboard displays:

- Successful Entries
- Vehicle Exits
- Duplicate Attempts
- Validation Failures
- Slot Conflicts
- Actual Active Duplicates
- Duplicate Prevention Rate
- Entry Success Rate
- Data Quality Status

---

# 5. PDCA Cycle Implementation

The project follows the PDCA cycle:

Plan
→ Do
→ Check
→ Act

---

# 6. PLAN

During the Plan phase, major parking quality problems were identified.

## Identified Problems

- Duplicate vehicle entries
- Duplicate parking IDs
- Invalid input data
- Inconsistent vehicle-number formats
- Incorrect parking slot allocation
- Occupied-slot conflicts
- Incorrect entry and exit records

## Main Quality Goal

Reduce duplicate entries and improve parking data accuracy.

## Quality Target

Actual Active Duplicate Vehicles = 0

The system was designed around this measurable target.

---

# 7. DO

During the Do phase, preventive controls were implemented.

## Input Validation

The system validates:

- Parking ID
- Vehicle number
- Owner name
- Phone number
- Vehicle type
- Parking slot

Invalid information is rejected before database insertion.

## Vehicle Number Normalization

Different representations of the same registration number are converted
to one standard format.

## Search Before Add

Before inserting a vehicle, the database is searched for an existing
active record with the same vehicle number.

If found, the new entry is prevented.

## Confirmation Dialog

Before saving a vehicle entry, the operator must verify the entered
information.

## Slot Validation

The system verifies:

- The slot exists
- The slot belongs to the correct vehicle type
- The slot is currently available

## Database Constraints

Database constraints provide another protection layer.

Examples:

- UNIQUE parking ID
- CHECK constraints
- FOREIGN KEY constraints
- Partial UNIQUE index for active vehicles

The partial unique index ensures that the same vehicle cannot have more
than one active Parked record.

---

# 8. CHECK

During the Check phase, system performance is measured.

The quality_log table records quality events.

The Quality Dashboard analyzes these records and displays quality
performance indicators.

## Quality Metrics

### Successful Entries

Number of successfully completed vehicle entries.

### Duplicate Attempts

Number of duplicate vehicle-entry attempts detected and prevented.

### Actual Active Duplicates

Number of vehicle numbers having more than one active Parked record.

Target:

Actual Active Duplicates = 0

### Duplicate Prevention Rate

Measures the effectiveness of duplicate prevention controls.

A result of 100% with zero active duplicates indicates that recorded
duplicate attempts were successfully prevented.

### Validation Failures

Number of invalid entry attempts rejected by validation rules.

### Slot Conflicts

Number of detected parking-slot conflicts.

### Vehicle Exits

Number of successfully completed vehicle exits recorded by the quality
logging system.

### Entry Success Rate

Measures the proportion of logged vehicle-entry attempts that were
successfully completed.

---

# 9. ACT

The Act phase uses the information collected during the Check phase to
improve the parking process.

Examples:

If validation failures are high:

→ Review common validation problems.

→ Improve user instructions.

→ Improve input validation rules.

If duplicate attempts increase:

→ Analyze the causes of repeated vehicle-entry attempts.

→ Improve operator workflow.

→ Improve duplicate warnings.

If slot conflicts increase:

→ Review parking slot allocation procedures.

→ Improve slot synchronization.

If Actual Active Duplicates becomes greater than zero:

→ Investigate database or application integrity immediately.

→ Identify the cause.

→ Correct the process.

→ Add or improve automated tests.

Therefore, the system supports continuous improvement rather than only
detecting errors.

---

# 10. Multi-Layer Duplicate Prevention

The system uses multiple layers of quality protection.

Vehicle Input
↓
Vehicle Number Normalization
↓
Format Validation
↓
Search Before Add
↓
Duplicate Detection
↓
Parking Slot Verification
↓
Confirmation Dialog
↓
Final Database Verification
↓
Database UNIQUE Constraint
↓
Quality Event Logging

This is a defense-in-depth approach to data quality.

---

# 11. Database-Level Quality Control

The database provides additional protection even if an application-level
validation rule fails.

A partial unique index is used:

CREATE UNIQUE INDEX idx_unique_active_vehicle
ON parking_records(vehicle_number)
WHERE status = 'Parked';

This allows historical records such as:

UK04AB1234 → Exited

UK04AB1234 → Exited

UK04AB1234 → Parked

but prevents:

UK04AB1234 → Parked

UK04AB1234 → Parked

Therefore, a vehicle can return to the parking facility after exiting,
but it cannot have two active parking entries simultaneously.

---

# 12. Automated Quality Assurance

Automated tests are used to verify important quality rules.

Validation tests verify:

- Uppercase normalization
- Space removal
- Hyphen removal
- Mixed-format normalization

Database tests verify:

- Valid record insertion
- Duplicate Parking ID rejection
- Duplicate active vehicle rejection
- Same vehicle allowed after previous exit
- Invalid status rejection
- Invalid parking-slot rejection

The automated tests reduce the risk of regression defects when the
software is modified.

---

# 13. Quality Reporting

The Quality Dashboard provides an option to export a CSV quality report.

The report contains:

- Quality performance metrics
- Quality target results
- Duplicate-prevention results
- Quality event history

This provides documented evidence of quality performance.

---

# 14. TQM Result

The project does not only manage parking records.

It manages the quality of the parking process.

The system follows the approach:

Prevent
→ Verify
→ Record
→ Measure
→ Analyze
→ Improve

This supports the main principles of Total Quality Management.

---

# 15. Conclusion

The Parking Management System demonstrates how TQM principles can be
applied to a software-based operational process.

Instead of relying only on error correction, the system uses validation,
standardization, duplicate prevention, database constraints, automated
testing, quality monitoring, and reporting.

The PDCA cycle provides a framework for continuous improvement:

Plan:
Identify quality problems and define measurable targets.

Do:
Implement preventive controls.

Check:
Measure quality performance using logged events and metrics.

Act:
Use measured results to improve the process.

The main measurable quality target of the project is:

> Maintain zero active duplicate vehicle records.