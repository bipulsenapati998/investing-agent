import logging
import os
from datetime import datetime

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Setup a logger with both file and console handlers
    
    Args:
        name: Name of the logger
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        fmt='%(levelname)s - %(name)s - %(message)s'
    )
    
    # Create file handler
    log_filename = f"{log_dir}/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create application-wide loggers
def get_app_logger() -> logging.Logger:
    """Get the main application logger"""
    return setup_logger("app", logging.INFO)

def get_creator_logger() -> logging.Logger:
    """Get the creator agent logger"""
    return setup_logger("creator", logging.INFO)

def get_agent_logger() -> logging.Logger:
    """Get the agent logger"""
    return setup_logger("agent", logging.INFO)

def get_messages_logger() -> logging.Logger:
    """Get the messages utility logger"""
    return setup_logger("messages", logging.INFO)