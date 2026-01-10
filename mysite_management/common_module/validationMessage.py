import enum 


class Messages(enum.Enum):
    """Enum for messages."""
    SUCCESS = "Success"
    FAILURE = "Failure"
    INVALID_INPUT = "Invalid input"
    INVALID_PASSWORD = "Invalid password"
    PROFILE_IS_UPDATED_SUCCESSFULLY = "Profile is updated successfully."
  
    
    LOGIN_USER = "Login user"
    YOU_ARE_NOW_LOGGED_IN = "you are now logged in."
    YOUR_ACCOUNT_IS_REGISTRATED_SUCCESSFULLY = "Your account is registrated successfully and registrated email is send successfully."
   
    INVALID_CREDENTIALS = "Invalid credentials"
    INVALID_TOKEN = "Invalid token"
    TOKEN_EXPIRED = "Token expired"

    USER_NOT_FOUND = "Staff user not found."
    USER_ALREADY_LOGGED_IN = "Staff user already logged in."
    LOGOUT_USER = "Logout Staff user"
    USER_NOT_LOGGED_IN = "Staff user not logged in."
    USER_NOT_VERIFIED = "Staff user not verified."
    USER_ALREADY_VERIFIED = "Staff user already verified."
    USER_IS_REGISTER = "Staff user is register successfully."
    USER_IS_NOT_REGISTER = "Staff user is not register."
    USER_IS_VERIFIED = "Staff user is verified successfully."
    USER_IS_UPDATED_SUCCESSFULLY = "Staff user is updated successfully."
    USER_ALREADY_EXISTS = "Staff user already exists."
    USER_IS_DELETED_SUCCESSFULLY = "Staff user is deleted successfully."

    PRODUCT_IS_ADD_SUCCESSFULLY = "Product is added successfully."
    PRODUCT_IS_UPDATED_SUCCESSFULLY = "Product is updated successfully."
    PRODUCT_IS_DELETED_SUCCESSFULLY = "Product is deleted successfully."
    PRODUCT_NOT_FOUND = "Product not found."
    PRODUCT_ALREADY_EXISTS = "Product already exists."

    CATEGORY_IS_ADD_SUCCESSFULLY = "Category is added successfully."



