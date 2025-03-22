import os
import shutil
import pandas as pd
from datetime import datetime
import re

def create_directories():
    base_dir = "Organized_Schedules"
    directories = [
        "Job_Categories/Window_Cleaning",
        "Job_Categories/Light_Fixture_Cleaning",
        "Job_Categories/Eaves_Cleaning",
        "Job_Categories/Other_Maintenance",
        "Time_Based/2023/Q1",
        "Time_Based/2023/Q2",
        "Time_Based/2023/Q3",
        "Time_Based/2023/Q4",
        "Time_Based/2024/Q1",
        "Time_Based/2024/Q2",
        "Time_Based/2024/Q3",
        "Time_Based/2024/Q4",
        "Status/Completed",
        "Status/Rescheduled",
        "Status/Cancelled",
        "Status/Pending",
        "Client_Type/Residential",
        "Client_Type/Commercial",
        "Crew_Organization/Solo",
        "Crew_Organization/Team",
        "Documentation",
        "Financial",
        "Location_Based"
    ]
    
    for directory in directories:
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)

def get_quarter(month):
    return (month - 1) // 3 + 1

def categorize_file(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except:
        try:
            df = pd.read_csv(file_path, encoding='latin1')
        except:
            print(f"Could not read file: {file_path}")
            return None
    
    categories = {
        'job_type': 'Other_Maintenance',
        'status': 'Pending',
        'client_type': 'Residential',
        'crew_type': 'Solo'
    }
    
    # Extract date from filename
    date_match = re.search(r'(\d{2})_(\d{2})_(\d{2})', os.path.basename(file_path))
    if date_match:
        month, day, year = map(int, date_match.groups())
        year = 2000 + year  # Convert 2-digit year to 4-digit
        quarter = get_quarter(month)
    else:
        return None

    # Determine job type
    job_keywords = {
        'window': 'Window_Cleaning',
        'light fixture': 'Light_Fixture_Cleaning',
        'eaves': 'Eaves_Cleaning'
    }
    
    for keyword, category in job_keywords.items():
        if any(keyword.lower() in str(cell).lower() for cell in df.values.flatten()):
            categories['job_type'] = category
            break

    # Determine status
    status_keywords = {
        'completed': 'Completed',
        'rescheduled': 'Rescheduled',
        'cancelled': 'Cancelled'
    }
    
    for keyword, status in status_keywords.items():
        if any(keyword.lower() in str(cell).lower() for cell in df.values.flatten()):
            categories['status'] = status
            break

    # Determine client type
    if any('commercial' in str(cell).lower() for cell in df.values.flatten()):
        categories['client_type'] = 'Commercial'

    # Determine crew type
    crew_indicators = ['team', 'crew', '+', '&', 'and']
    if any(indicator in str(cell).lower() for cell in df.values.flatten() for indicator in crew_indicators):
        categories['crew_type'] = 'Team'

    return {
        'year': year,
        'quarter': quarter,
        'categories': categories
    }

def organize_files():
    source_dir = "History CSV/Daily Schedules CSV"
    
    # Create necessary directories
    create_directories()
    
    # Process each CSV file
    for filename in os.listdir(source_dir):
        if not filename.endswith('.csv'):
            continue
            
        file_path = os.path.join(source_dir, filename)
        result = categorize_file(file_path)
        
        if result is None:
            continue
            
        year = result['year']
        quarter = result['quarter']
        categories = result['categories']
        
        # Create symbolic links in appropriate categories
        dest_paths = [
            f"Organized_Schedules/Job_Categories/{categories['job_type']}/{filename}",
            f"Organized_Schedules/Time_Based/{year}/Q{quarter}/{filename}",
            f"Organized_Schedules/Status/{categories['status']}/{filename}",
            f"Organized_Schedules/Client_Type/{categories['client_type']}/{filename}",
            f"Organized_Schedules/Crew_Organization/{categories['crew_type']}/{filename}"
        ]
        
        # Create symbolic links
        for dest_path in dest_paths:
            try:
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                os.symlink(os.path.abspath(file_path), dest_path)
            except Exception as e:
                print(f"Error creating symlink for {filename}: {str(e)}")

if __name__ == "__main__":
    organize_files() 