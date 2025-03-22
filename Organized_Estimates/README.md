# QuickBooks Estimates Organization System

This system organizes QuickBooks estimate files into meaningful categories for better analysis and accessibility.

## Directory Structure

```
Organized_Estimates/
├── Service_Categories/
│   ├── Window_Cleaning/
│   ├── Light_Fixture/
│   ├── Eaves_Cleaning/
│   ├── Post_Construction/
│   ├── Power_Washing/
│   ├── Screen_Services/
│   ├── Glass_Services/
│   └── Other_Services/
├── Time_Based/
│   ├── 2022/
│   │   ├── Q1/
│   │   ├── Q2/
│   │   ├── Q3/
│   │   └── Q4/
│   ├── 2023/
│   │   └── [quarters]
│   └── 2024/
│       └── [quarters]
├── Revenue_Ranges/
│   ├── 0-500/
│   ├── 501-1000/
│   ├── 1001-2000/
│   └── 2000+/
├── Client_Categories/
│   ├── Residential/
│   ├── Commercial/
│   ├── Regular_Clients/
│   └── One_Time_Clients/
└── Service_Combinations/
    ├── Single_Service/
    ├── Multi_Service/
    └── Package_Deals/
```

## Categories Explanation

1. **Service Categories**
   - Window_Cleaning: All window cleaning services
   - Light_Fixture: Light fixture cleaning and maintenance
   - Eaves_Cleaning: Eaves and gutter cleaning services
   - Post_Construction: Post-construction cleaning services
   - Power_Washing: Power and pressure washing services
   - Screen_Services: Screen cleaning and repairs
   - Glass_Services: Specialized glass cleaning services
   - Other_Services: Miscellaneous services

2. **Time-Based Organization**
   - Organized by year (2022-2024)
   - Further divided into quarters
   - Helps track seasonal trends and year-over-year growth

3. **Revenue Ranges**
   - 0-500: Small jobs
   - 501-1000: Medium jobs
   - 1001-2000: Large jobs
   - 2000+: Premium jobs
   - Useful for analyzing pricing strategies and revenue distribution

4. **Client Categories**
   - Residential: Individual homeowners
   - Commercial: Business clients
   - Regular_Clients: Repeat customers
   - One_Time_Clients: Single-service customers
   - Helps in customer relationship management and marketing

5. **Service Combinations**
   - Single_Service: Clients who ordered one type of service
   - Multi_Service: Clients who combined two services
   - Package_Deals: Clients who ordered three or more services
   - Useful for package pricing and upselling strategies

## Features

1. **Symbolic Links**
   - Files appear in multiple relevant categories
   - Original files remain unchanged
   - Easy to track a client across different categories

2. **Automated Categorization**
   - Python script automatically categorizes based on content
   - Handles multiple years of data
   - Intelligent service and client categorization

3. **Flexible Organization**
   - Multiple views of the same data
   - Easy to analyze trends and patterns
   - Supports business decision-making

## Usage

1. **Running the Organization Script**:
   ```bash
   python organize_estimates.py
   ```

2. **Analyzing Data**:
   - Navigate to specific categories to view relevant estimates
   - Cross-reference between categories for deeper insights
   - Track changes over time and across service types

3. **Business Intelligence**:
   - Identify popular service combinations
   - Track high-value clients
   - Analyze seasonal trends
   - Monitor service distribution

## Benefits

1. **Business Analysis**
   - Easy identification of top services
   - Clear view of client distribution
   - Revenue pattern analysis
   - Seasonal trend tracking

2. **Customer Management**
   - Quick access to client history
   - Identification of regular clients
   - Service preference tracking
   - Opportunity spotting for upselling

3. **Financial Planning**
   - Revenue distribution analysis
   - Service pricing optimization
   - Package deal effectiveness
   - Seasonal revenue patterns 