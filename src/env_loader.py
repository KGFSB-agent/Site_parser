import os


def load_env_file(file_path=".env"):
    """
    Manually load environment variables from a .env file and set them in the os environment.
    
    Args:
        file_path (str): The path to the .env file. Default is ".env".
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    
    with open(file_path, "r") as file:
        for line in file:
            # Removing spaces and comments
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split("=", 1)
                os.environ[key] = value
