# Target Companies Job Sites

## Overview

This document lists all target company job posting websites that the Job Fitment Analysis Agent can search. Companies are organized by priority level and industry sector.

## Primary Target Companies (From Problem Statement)

| Company | Job Site URL | Industry | Priority Default |
|---------|-------------|----------|------------------|
| **Cisco** | https://careers.cisco.com/global/en | Networking/Security | 1 |
| **SAP** | https://jobs.sap.com/ | Enterprise Software | 1 |
| **Google** | https://careers.google.com/jobs/ | Tech/Search/Cloud | 1 |
| **Apple** | https://jobs.apple.com/ | Consumer Tech | 1 |
| **Amazon** | https://www.amazon.jobs/ | E-commerce/Cloud | 2 |
| **Tesla** | https://www.tesla.com/careers | Automotive/Energy | 2 |

## Extended Company List

### Tier 1: Tech Giants

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| Microsoft | https://careers.microsoft.com/ | Cloud, Enterprise, Gaming |
| Meta | https://www.metacareers.com/ | Social Media, VR/AR, AI |
| Netflix | https://jobs.netflix.com/ | Streaming, Content |
| NVIDIA | https://www.nvidia.com/en-us/about-nvidia/careers/ | GPUs, AI Hardware |

### Tier 2: Enterprise & Software

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| IBM | https://www.ibm.com/careers/ | Enterprise AI, Cloud |
| Intel | https://jobs.intel.com/ | Semiconductors |
| Oracle | https://www.oracle.com/careers/ | Database, Cloud |
| Salesforce | https://www.salesforce.com/company/careers/ | CRM, Cloud |
| Adobe | https://www.adobe.com/careers.html | Creative Software |
| VMware | https://careers.vmware.com/ | Virtualization |
| Dell | https://jobs.dell.com/ | Hardware, Services |
| HP | https://jobs.hp.com/ | Hardware, Printing |

### Tier 3: Finance & Fintech

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| Goldman Sachs | https://www.goldmansachs.com/careers/ | Investment Banking |
| JPMorgan Chase | https://careers.jpmorgan.com/ | Banking, Fintech |
| Morgan Stanley | https://www.morganstanley.com/careers | Investment Banking |
| Stripe | https://stripe.com/jobs | Payments |
| Square | https://squareup.com/careers | Payments, POS |
| PayPal | https://www.paypal.com/us/webapps/mpp/jobs | Payments |
| Visa | https://usa.visa.com/careers.html | Payments Network |
| Mastercard | https://www.mastercard.us/en-us/vision/who-we-are/careers.html | Payments |

### Tier 4: Startups & Growth Companies

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| Airbnb | https://careers.airbnb.com/ | Travel, Marketplace |
| Uber | https://www.uber.com/us/en/careers/ | Mobility, Delivery |
| Lyft | https://www.lyft.com/careers | Mobility |
| DoorDash | https://careers.doordash.com/ | Delivery |
| Shopify | https://www.shopify.com/careers | E-commerce Platform |
| Databricks | https://www.databricks.com/company/careers | Data/AI Platform |
| Snowflake | https://careers.snowflake.com/ | Data Cloud |
| Palantir | https://www.palantir.com/careers/ | Data Analytics |

### Tier 5: Consulting & Services

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| Accenture | https://www.accenture.com/us-en/careers | Consulting, Tech |
| Deloitte | https://www2.deloitte.com/us/en/careers/careers.html | Consulting |
| McKinsey | https://www.mckinsey.com/careers | Consulting |
| BCG | https://www.bcg.com/careers | Consulting |
| Bain | https://www.bain.com/careers/ | Consulting |

### Tier 6: Healthcare & Biotech

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| Johnson & Johnson | https://jobs.jnj.com/ | Healthcare |
| Pfizer | https://www.pfizer.com/about/careers | Pharma |
| Moderna | https://www.modernatx.com/careers | Biotech |
| UnitedHealth | https://careers.unitedhealthgroup.com/ | Healthcare Services |

### Tier 7: Aerospace & Defense

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| SpaceX | https://www.spacex.com/careers | Space |
| Boeing | https://jobs.boeing.com/ | Aerospace |
| Lockheed Martin | https://www.lockheedmartinjobs.com/ | Defense |
| Northrop Grumman | https://www.northropgrumman.com/careers/ | Defense |

### Tier 8: Telecommunications

| Company | Job Site URL | Focus Areas |
|---------|-------------|-------------|
| AT&T | https://www.att.jobs/ | Telecom |
| Verizon | https://www.verizon.com/about/careers | Telecom |
| T-Mobile | https://www.t-mobile.com/careers | Telecom |
| Qualcomm | https://www.qualcomm.com/company/careers | Mobile Tech |

## Search Tips

### Keywords by Role Type

**Software Engineering:**
- "software engineer", "developer", "SDE"
- "backend", "frontend", "full stack"
- "platform", "infrastructure"

**Data & ML:**
- "data scientist", "data engineer"
- "machine learning", "AI engineer"
- "analytics", "ML engineer"

**Product & Design:**
- "product manager", "PM"
- "UX designer", "product designer"
- "UX researcher"

**DevOps & Cloud:**
- "DevOps", "SRE", "platform engineer"
- "cloud engineer", "infrastructure"
- "site reliability"

### Experience Level Keywords

| Level | Keywords |
|-------|----------|
| Entry | "new grad", "entry level", "junior", "associate", "I", "L3" |
| Mid | "mid-level", "II", "L4", "engineer" |
| Senior | "senior", "III", "L5", "staff", "lead" |
| Principal | "principal", "distinguished", "L6+", "architect" |

## API Access Notes

Some companies offer public APIs for job searches:
- **LinkedIn Jobs API** - Requires LinkedIn partnership
- **Indeed API** - Limited public access
- **Glassdoor API** - Requires partnership

For the agent, we primarily use web scraping of public career pages.

## Update Frequency

Company career pages are updated frequently. Recommended refresh:
- Priority 1 companies: Check daily
- Priority 2 companies: Check weekly
- Priority 3 companies: Check bi-weekly

## Usage in Agent

```python
from job_fitment_agent import TARGET_COMPANIES, CompanyConfig

# Add custom companies
my_companies = [
    CompanyConfig("MyDreamCompany", "https://careers.example.com", priority=1),
]

# Or modify existing priorities
for company in TARGET_COMPANIES:
    if company.name == "Google":
        company.priority = 1  # Make it highest priority
```
