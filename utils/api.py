import requests
import time
from typing import Dict, Tuple, Any

from config import API_URL, MAX_RETRIES

def create_user(user_data: Dict[str, Any], api_url: str = API_URL, max_retries: int = MAX_RETRIES) -> Tuple[bool, str]:
    """
    Sends a request to create a user and handles the response with retry logic.
    
    Args:
        user_data: User data to send to the API
        api_url: The API endpoint URL
        max_retries: Maximum number of retry attempts
        
    Returns:
        Tuple containing (success, error_message)
        success is True if the API call was successful, False otherwise
        error_message contains details if there was an error, empty string otherwise
    """
    retry_count = 0
    while retry_count <= max_retries:
        try:
            response = requests.post(api_url, json=user_data, timeout=(3.05, 27))  # Connect timeout, Read timeout
            if response.status_code == 201:
                return True, ""
            else:
                error_message = f"API returned status code {response.status_code}"
                try:
                    error_details = response.json()
                    error_message += f": {error_details}"
                except ValueError:
                    error_message += f": {response.text}"
                return False, error_message
        except requests.exceptions.RequestException as e:
            retry_count += 1
            if retry_count > max_retries:
                return False, f"Request failed after {max_retries} retries: {str(e)}"
            # Exponential backoff
            wait_time = 2 ** retry_count
            time.sleep(wait_time)
