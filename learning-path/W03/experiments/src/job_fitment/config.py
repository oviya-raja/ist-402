"""
Configuration and constants for Job Fitment Agent.
"""

from pathlib import Path
from .models import CompanyConfig

# Primary target companies from the problem statement
TARGET_COMPANIES = [
    CompanyConfig("Cisco", "https://careers.cisco.com/global/en", 1),
    CompanyConfig("SAP", "https://jobs.sap.com/", 1),
    CompanyConfig("Google", "https://careers.google.com/jobs/", 1),
    CompanyConfig("Apple", "https://jobs.apple.com/", 1),
    CompanyConfig("Amazon", "https://www.amazon.jobs/", 2),
    CompanyConfig("Tesla", "https://www.tesla.com/careers", 2),
    CompanyConfig("Microsoft", "https://careers.microsoft.com/", 2),
    CompanyConfig("Meta", "https://www.metacareers.com/", 2),
    CompanyConfig("Netflix", "https://jobs.netflix.com/", 3),
    CompanyConfig("NVIDIA", "https://www.nvidia.com/en-us/about-nvidia/careers/", 3),
    CompanyConfig("Intel", "https://jobs.intel.com/", 3),
    CompanyConfig("IBM", "https://www.ibm.com/careers/", 3),
]

# Output directory
OUTPUT_DIR = Path("data/job_fitment")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

