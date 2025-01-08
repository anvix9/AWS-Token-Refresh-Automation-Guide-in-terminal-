import os
import json
import subprocess
import datetime
from pathlib import Path
import time
import logging
from typing import Dict, Optional
import configparser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSTokenRefresher:
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.aws_cli_path = Path.home() / '.aws' / 'cli' / 'cache'
        self.credentials_path = Path.home() / '.aws' / 'credentials'

    def check_token_validity(self) -> bool:
        """Check if the current token is valid."""
        try:
            result = subprocess.run(
                ['aws', 'sts', 'get-caller-identity', '--profile', self.profile_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error checking token validity: {e}")
            return False

    def refresh_token(self) -> bool:
        """Initiate the SSO login process."""
        try:
            result = subprocess.run(
                ['aws', 'sso', 'login', '--profile', self.profile_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return False

    def get_latest_credentials(self) -> Optional[Dict]:
        """Get the most recent credentials from the CLI cache."""
        try:
            latest_file = None
            latest_time = datetime.datetime.min

            # Find the most recent credentials file
            for file in self.aws_cli_path.glob('*.json'):
                file_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)
                if file_time > latest_time:
                    latest_time = file_time
                    latest_file = file
            
            if latest_file:
                with open(latest_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error getting latest credentials: {e}")
            return None

    def update_credentials(self, new_credentials: Dict) -> bool:
        """Update the AWS credentials file with new tokens."""
        time.sleep(1) # to let the system refresh and find eaily the new created file
        print(f"New Credentials: {new_credentials}")
        try:
            # Create a backup of existing credentials
            if self.credentials_path.exists():
                backup_path = self.credentials_path.with_suffix('.backup')
                with open(self.credentials_path, 'r') as f:
                    with open(backup_path, 'w') as b:
                        b.write(f.read())

            # Update credentials
            config = configparser.ConfigParser()
            if self.credentials_path.exists():
                config.read(self.credentials_path)

            if self.profile_name not in config.sections():
                config.add_section(self.profile_name)
            
            print(dict(config['admin-1']))
            config[self.profile_name].update({
                'aws_access_key_id': new_credentials['Credentials']['AccessKeyId'],
                'aws_secret_access_key': new_credentials['Credentials']['SecretAccessKey'],
                'aws_session_token': new_credentials['Credentials']['SessionToken']
            })

            with open(self.credentials_path, 'w') as f:
                config.write(f)

            return True
        except Exception as e:
            logger.error(f"Error updating credentials: {e}")
            return False

    def run(self):
        """Main method to check and refresh tokens if needed."""
        logger.info("Checking AWS token validity...")
        
        if not self.check_token_validity():
            logger.info("Token expired or invalid. Initiating refresh...")
            
            if self.refresh_token():
                logger.info("Token refresh successful.")
                
                new_credentials = self.get_latest_credentials()
                if new_credentials and self.update_credentials(new_credentials):
                    logger.info("Credentials updated successfully.")
                    return True
                else:
                    logger.error("Failed to update credentials.")
                    return False
            else:
                logger.error("Token refresh failed.")
                return False
        else:
            logger.info("Token is still valid.")
            return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AWS Token Refresh Automation')
    parser.add_argument('--profile', default='default', help='AWS profile name')
    args = parser.parse_args()

    refresher = AWSTokenRefresher(args.profile)
    refresher.run()
