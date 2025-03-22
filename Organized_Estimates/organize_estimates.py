import os
import pandas as pd
import numpy as np
from datetime import datetime
import shutil
import glob

def create_directories():
    base_dir = "Organized_Estimates"
    directories = {
        "Service_Categories": [
            "Window_Cleaning",
            "Light_Fixture",
            "Eaves_Cleaning",
            "Post_Construction",
            "Power_Washing",
            "Screen_Services",
            "Glass_Services",
            "Other_Services"
        ],
        "Time_Based": {
            "2022": ["Q1", "Q2", "Q3", "Q4"],
            "2023": ["Q1", "Q2", "Q3", "Q4"],
            "2024": ["Q1", "Q2", "Q3", "Q4"]
        },
        "Revenue_Ranges": [
            "0-500",
            "501-1000",
            "1001-2000",
            "2000+"
        ],
        "Client_Categories": [
            "Residential",
            "Commercial",
            "Regular_Clients",
            "One_Time_Clients"
        ],
        "Service_Combinations": [
            "Single_Service",
            "Multi_Service",
            "Package_Deals"
        ]
    }
    
    # Create main directories
    for main_dir in directories.keys():
        main_path = os.path.join(base_dir, main_dir)
        if isinstance(directories[main_dir], list):
            for sub_dir in directories[main_dir]:
                os.makedirs(os.path.join(main_path, sub_dir), exist_ok=True)
        else:
            for year, quarters in directories[main_dir].items():
                year_path = os.path.join(main_path, year)
                for quarter in quarters:
                    os.makedirs(os.path.join(year_path, quarter), exist_ok=True)

def get_quarter(date_str):
    try:
        date = datetime.strptime(date_str, "%Y")
        month = 1  # Default to January if only year is provided
    except:
        try:
            date = datetime.strptime(date_str, "%B - %Y")
            month = date.month
        except:
            return "Q1"  # Default to Q1 if parsing fails
    
    return f"Q{(month-1)//3 + 1}"

def get_revenue_range(total):
    try:
        if isinstance(total, str):
            total = float(total.replace("$", "").replace(",", "").strip())
        else:
            total = float(total)
            
        if total <= 500:
            return "0-500"
        elif total <= 1000:
            return "501-1000"
        elif total <= 2000:
            return "1001-2000"
        else:
            return "2000+"
    except:
        return "0-500"

def categorize_services(row):
    services = []
    window_cleaning_terms = ['window', 'glass', 'skylight', 'atrium', 'solarium', 'sun room']
    eaves_terms = ['eaves', 'gutter', 'downspout', 'down spout', 'eavestrough']
    power_washing_terms = ['power', 'pressure', 'soft washing']
    screen_terms = ['screen']
    post_construction_terms = ['construction']
    light_fixture_terms = ['light fixture', 'lighting']
    
    for service, value in row.items():
        try:
            if pd.notna(value) and value != 0:
                if isinstance(value, str):
                    value = float(value.replace("$", "").replace(",", "").strip())
                if value <= 0:
                    continue
                    
                service_name = str(service).lower()
                
                # Check for window cleaning services
                if any(term in service_name for term in window_cleaning_terms):
                    services.append("Window_Cleaning")
                    
                # Check for eaves cleaning services
                if any(term in service_name for term in eaves_terms):
                    services.append("Eaves_Cleaning")
                    
                # Check for power washing services
                if any(term in service_name for term in power_washing_terms):
                    services.append("Power_Washing")
                    
                # Check for screen services
                if any(term in service_name for term in screen_terms):
                    services.append("Screen_Services")
                    
                # Check for post construction services
                if any(term in service_name for term in post_construction_terms):
                    services.append("Post_Construction")
                    
                # Check for light fixture services
                if any(term in service_name for term in light_fixture_terms):
                    services.append("Light_Fixture")
                    
                # If no specific category is found and the value is positive
                if not any(term in service_name for term in 
                          window_cleaning_terms + eaves_terms + power_washing_terms + 
                          screen_terms + post_construction_terms + light_fixture_terms):
                    services.append("Other_Services")
        except Exception as e:
            print(f"Error processing service {service}: {str(e)}")
            continue
    
    return list(set(services))

def determine_client_category(row, all_data):
    client_name = row.name
    client_appearances = all_data.index.value_counts()[client_name]
    total_services = sum(1 for value in row if pd.notna(value) and 
                        (isinstance(value, (int, float)) and value > 0 or
                         isinstance(value, str) and float(value.replace("$", "").replace(",", "").strip()) > 0))
    
    categories = []
    
    # Regular vs One-time
    if client_appearances > 1 or total_services > 2:
        categories.append("Regular_Clients")
    else:
        categories.append("One_Time_Clients")
    
    # Commercial vs Residential
    commercial_terms = ["Ltd", "Inc", "Limited", "Corporation", "Corp", "Company", "Co.", "Services"]
    if any(term.lower() in str(client_name).lower() for term in commercial_terms):
        categories.append("Commercial")
    else:
        categories.append("Residential")
    
    return categories

def determine_service_combination(services):
    if len(services) == 0:
        return ["Single_Service"]
    elif len(services) == 1:
        return ["Single_Service"]
    elif len(services) == 2:
        return ["Multi_Service"]
    else:
        return ["Package_Deals"]

def create_symlink(source, dest):
    try:
        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        # Remove existing symlink or file
        if os.path.exists(dest):
            if os.path.islink(dest):
                os.unlink(dest)
            else:
                os.remove(dest)
        
        # Create relative symlink
        source_rel = os.path.relpath(source, os.path.dirname(dest))
        os.symlink(source_rel, dest)
        print(f"Created symlink: {dest} -> {source_rel}")
    except Exception as e:
        print(f"Error creating symlink from {source} to {dest}: {str(e)}")

def organize_file(file_path):
    try:
        print(f"\nProcessing file: {file_path}")
        
        # Skip the header rows that contain the title and company name
        df = pd.read_csv(file_path, skiprows=lambda x: x < 4)
        year = os.path.basename(file_path).split()[2].split('.')[0]
        
        print(f"Year extracted: {year}")
        
        # Remove summary rows and empty columns
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        
        # Set client name as index
        df = df.set_index(df.columns[0])
        
        print(f"Found {len(df)} clients to process")
        
        # Process each client
        for client, row in df.iterrows():
            if isinstance(client, str) and client != "TOTAL":
                print(f"\nProcessing client: {client}")
                services = categorize_services(row)
                print(f"Services: {services}")
                
                client_categories = determine_client_category(row, df)
                print(f"Client categories: {client_categories}")
                
                service_combinations = determine_service_combination(services)
                print(f"Service combinations: {service_combinations}")
                
                total = row.get("TOTAL", 0)
                revenue_range = get_revenue_range(total)
                print(f"Revenue range: {revenue_range}")
                
                quarter = get_quarter(year)
                print(f"Quarter: {quarter}")
                
                # Create symbolic links
                source_path = os.path.abspath(file_path)
                
                # Service Categories
                for service in services:
                    dest_path = os.path.join("Organized_Estimates", "Service_Categories", service, os.path.basename(file_path))
                    create_symlink(source_path, dest_path)
                
                # Time Based
                dest_path = os.path.join("Organized_Estimates", "Time_Based", year, quarter, os.path.basename(file_path))
                create_symlink(source_path, dest_path)
                
                # Revenue Ranges
                dest_path = os.path.join("Organized_Estimates", "Revenue_Ranges", revenue_range, os.path.basename(file_path))
                create_symlink(source_path, dest_path)
                
                # Client Categories
                for category in client_categories:
                    dest_path = os.path.join("Organized_Estimates", "Client_Categories", category, os.path.basename(file_path))
                    create_symlink(source_path, dest_path)
                
                # Service Combinations
                for combination in service_combinations:
                    dest_path = os.path.join("Organized_Estimates", "Service_Combinations", combination, os.path.basename(file_path))
                    create_symlink(source_path, dest_path)
                
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        raise

def main():
    try:
        # Create directory structure
        create_directories()
        
        # Process each QuickBooks estimate file using glob pattern matching
        csv_pattern = "History CSV/QUICKBOOKS ESTIMATE* 202?.csv"
        source_files = glob.glob(csv_pattern)
        
        if not source_files:
            print(f"No files found matching pattern: {csv_pattern}")
            return
            
        print(f"Found files to process: {source_files}")
        
        for file_path in source_files:
            organize_file(file_path)
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 