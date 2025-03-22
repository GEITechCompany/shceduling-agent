# Schedule Organization System

This system organizes daily schedules into meaningful categories for better management and accessibility.

## Directory Structure

```
Organized_Schedules/
├── Job_Categories/
│   ├── Window_Cleaning/
│   ├── Light_Fixture_Cleaning/
│   ├── Eaves_Cleaning/
│   └── Other_Maintenance/
├── Time_Based/
│   ├── 2023/
│   │   ├── Q1/
│   │   ├── Q2/
│   │   ├── Q3/
│   │   └── Q4/
│   └── 2024/
│       ├── Q1/
│       ├── Q2/
│       ├── Q3/
│       └── Q4/
├── Status/
│   ├── Completed/
│   ├── Rescheduled/
│   ├── Cancelled/
│   └── Pending/
├── Client_Type/
│   ├── Residential/
│   └── Commercial/
├── Crew_Organization/
│   ├── Solo/
│   └── Team/
├── Documentation/
├── Financial/
└── Location_Based/
```

## Features

1. **Automated Categorization**: Python script automatically categorizes CSV files based on content
2. **Symbolic Links**: Files are linked across multiple relevant categories
3. **New Template**: Comprehensive template for future schedule entries
4. **Multiple Views**: Access the same schedule from different organizational perspectives

## Files

- `schedule_template.csv`: New comprehensive template for creating schedules
- `categorize_schedules.py`: Script to automatically organize existing schedules
- `requirements.txt`: Python dependencies

## Usage

1. **Setting Up**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Organization Script**:
   ```bash
   python categorize_schedules.py
   ```

3. **Creating New Schedules**:
   - Copy `schedule_template.csv`
   - Fill in the required information
   - Save in the appropriate directories

## Categories Explanation

1. **Job Categories**
   - Window Cleaning
   - Light Fixture Cleaning
   - Eaves Cleaning
   - Other Maintenance

2. **Time-based Organization**
   - Organized by year and quarter
   - Easy access to historical data

3. **Status Categories**
   - Completed: Finished jobs
   - Rescheduled: Postponed jobs
   - Cancelled: Terminated jobs
   - Pending: Upcoming jobs

4. **Client Type**
   - Residential: Home-based jobs
   - Commercial: Business-based jobs

5. **Crew Organization**
   - Solo: Single-person jobs
   - Team: Multiple-person jobs

## Template Sections

1. **Basic Information**
   - Date and time details
   - Client information
   - Location details

2. **Job Details**
   - Service description
   - Requirements
   - Equipment needs

3. **Pricing Breakdown**
   - Base price
   - Additional services
   - Discounts

4. **Notes and Documentation**
   - Pre-job notes
   - Progress notes
   - Post-job notes

5. **Follow-up**
   - Next service date
   - Maintenance requirements
   - Special instructions 