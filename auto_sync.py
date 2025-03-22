import time
import schedule
from sync_to_sheets import DataSyncer
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sync.log'),
        logging.StreamHandler()
    ]
)

def sync_job():
    """Run the sync job and log the results."""
    try:
        logging.info("Starting scheduled sync...")
        syncer = DataSyncer()
        syncer.sync_all()
        logging.info("Sync completed successfully!")
    except Exception as e:
        logging.error(f"Error during sync: {str(e)}")

def main():
    # Schedule the sync job
    schedule.every(15).minutes.do(sync_job)  # Sync every 15 minutes
    
    # Run the sync immediately when starting
    sync_job()
    
    logging.info("Auto-sync started. Will sync every 15 minutes.")
    logging.info("Press Ctrl+C to stop.")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 