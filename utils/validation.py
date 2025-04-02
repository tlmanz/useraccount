from typing import Dict, Tuple, Any, Optional
from email_validator import validate_email, EmailNotValidError
from config import REQUIRED_FIELDS

# We can use this as a validation chain if needed.
def validate_user_data(user_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates if the user data contains all required fields.
    
    Args:
        user_data: Dictionary containing user data fields
        
    Returns:
        Tuple containing (is_valid, error_message)
        is_valid is True if all validations pass, False otherwise
        error_message contains all validation errors found, separated by semicolons
    """
    errors = []
    
    # Check required fields
    required_fields = REQUIRED_FIELDS
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Email validation is now handled separately in the main.py file
    
    # Return validation results
    if errors:
        return False, "; ".join(errors)
    return True, ""

# Email validation is separated from user data validation for better modularity.
def validate_email_address(email: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Validates an email address and returns the normalized version if valid.
    
    Args:
        email: The email address to validate
        
    Returns:
        Tuple containing (normalized_email, error_message)
        If valid, normalized_email contains the normalized email and error_message is None
        If invalid, normalized_email is None and error_message contains the error
    """
    try:
        # Validate and normalize the email, but skip DNS validation for testing purposes
        valid = validate_email(email, check_deliverability=False)
        # Return the normalized email address
        return valid.normalized, None
    except EmailNotValidError as e:
        # Return None for the email and the error message
        return None, str(e)
