"""Configuration settings for arXiv CS daily paper distributor"""

import os
class Config:
    """Base configuration class."""
    
    # ArXiv API settings
    AXRIV_API_BASE_URL = "https://export.arxiv.org/api/query"
    CS_CATEGORIES = ["cs.AI", "cs.LG", "cs.NE", "cs.CM", "cs.CH", "cs.DS", "cs.CV", "cs.CL", "cs.RO", "cs.SI", "cs.CE", "cs.MO", "cs.SY", "cs.OS", "cs.SC", "cs.HC", "cs.MM"]
    
    # Database settings
    SQLITE_DATABASE_URI = "sqlite:///arxiv_cs_daily.db"
    
    # Email settings
    EMAIL_SENDER = "arAICS@example.com"
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # Scheduling settings
    FETCH_INTERVAL = 24 # hours
    
    # Logging
    LOG_LEVER = "INFO"