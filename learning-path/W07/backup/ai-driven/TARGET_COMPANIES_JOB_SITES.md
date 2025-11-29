# Target Companies - Public Job Posting Sites

## List of Publicly Available Company Job Posting Websites

This document lists companies with publicly accessible job posting websites that the Job Fitment Analysis Agent can search within.

### Primary Target Companies (User Specified)

1. **Cisco**
   - URL: https://careers.cisco.com/global/en
   - Searchable: Yes
   - API Available: No
   - Notes: Ranked #3 on World's Best Workplaces 2025

2. **SAP**
   - URL: https://jobs.sap.com/
   - Searchable: Yes
   - API Available: No
   - Notes: Enterprise software company

3. **Google**
   - URL: https://careers.google.com/jobs/
   - Searchable: Yes
   - API Available: Limited
   - Notes: Technology and cloud services

4. **Apple**
   - URL: https://jobs.apple.com/
   - Searchable: Yes
   - API Available: No
   - Notes: Consumer electronics and software

5. **Amazon**
   - URL: https://www.amazon.jobs/
   - Searchable: Yes
   - API Available: No
   - Notes: E-commerce and cloud computing

6. **Tesla**
   - URL: https://www.tesla.com/careers
   - Searchable: Yes
   - API Available: No
   - Notes: Electric vehicles and energy

### Additional Technology Companies

7. **Microsoft**
   - URL: https://careers.microsoft.com/us/en
   - Searchable: Yes
   - API Available: No

5. **Meta (Facebook)**
   - URL: https://www.metacareers.com/
   - Searchable: Yes
   - API Available: No

6. **Netflix**
   - URL: https://jobs.netflix.com/
   - Searchable: Yes
   - API Available: No

7. **Salesforce**
   - URL: https://salesforce.wd1.myworkdayjobs.com/
   - Searchable: Yes
   - API Available: No

8. **Oracle**
   - URL: https://careers.oracle.com/
   - Searchable: Yes
   - API Available: No

9. **IBM**
   - URL: https://www.ibm.com/careers/us-en/
   - Searchable: Yes
   - API Available: No

10. **Adobe**
    - URL: https://careers.adobe.com/us/en
    - Searchable: Yes
    - API Available: No

11. **Intel**
    - URL: https://jobs.intel.com/
    - Searchable: Yes
    - API Available: No

12. **NVIDIA**
    - URL: https://nvidia.wd5.myworkdayjobs.com/
    - Searchable: Yes
    - API Available: No

13. **Tesla**
    - URL: https://www.tesla.com/careers
    - Searchable: Yes
    - API Available: No

14. **Uber**
    - URL: https://www.uber.com/careers/
    - Searchable: Yes
    - API Available: No

15. **Airbnb**
    - URL: https://careers.airbnb.com/
    - Searchable: Yes
    - API Available: No

### Financial Services

18. **JPMorgan Chase**
    - URL: https://careers.jpmorgan.com/
    - Searchable: Yes
    - API Available: No

19. **Goldman Sachs**
    - URL: https://www.goldmansachs.com/careers/
    - Searchable: Yes
    - API Available: No

20. **Morgan Stanley**
    - URL: https://www.morganstanley.com/people-opportunities/
    - Searchable: Yes
    - API Available: No

21. **Bank of America**
    - URL: https://careers.bankofamerica.com/
    - Searchable: Yes
    - API Available: No

22. **Citigroup**
    - URL: https://jobs.citi.com/
    - Searchable: Yes
    - API Available: No

### Consulting & Professional Services

23. **McKinsey & Company**
    - URL: https://www.mckinsey.com/careers
    - Searchable: Yes
    - API Available: No

24. **Boston Consulting Group (BCG)**
    - URL: https://careers.bcg.com/
    - Searchable: Yes
    - API Available: No

25. **Deloitte**
    - URL: https://www2.deloitte.com/us/en/careers.html
    - Searchable: Yes
    - API Available: No

26. **PwC**
    - URL: https://www.pwc.com/us/en/careers.html
    - Searchable: Yes
    - API Available: No

27. **EY (Ernst & Young)**
    - URL: https://careers.ey.com/
    - Searchable: Yes
    - API Available: No

28. **Accenture**
    - URL: https://www.accenture.com/us-en/careers
    - Searchable: Yes
    - API Available: No

### E-commerce & Retail

29. **Walmart**
    - URL: https://careers.walmart.com/
    - Searchable: Yes
    - API Available: No

30. **Target**
    - URL: https://corporate.target.com/careers
    - Searchable: Yes
    - API Available: No

### Healthcare & Pharmaceuticals

31. **Johnson & Johnson**
    - URL: https://www.careers.jnj.com/
    - Searchable: Yes
    - API Available: No

32. **Pfizer**
    - URL: https://www.pfizer.com/careers
    - Searchable: Yes
    - API Available: No

### Media & Entertainment

33. **Disney**
    - URL: https://jobs.disneycareers.com/
    - Searchable: Yes
    - API Available: No

34. **Warner Bros. Discovery**
    - URL: https://wbd.com/careers/
    - Searchable: Yes
    - API Available: No

### Automotive

35. **Ford**
    - URL: https://corporate.ford.com/careers.html
    - Searchable: Yes
    - API Available: No

36. **General Motors**
    - URL: https://search-careers.gm.com/
    - Searchable: Yes
    - API Available: No

### Aerospace & Defense

37. **Boeing**
    - URL: https://jobs.boeing.com/
    - Searchable: Yes
    - API Available: No

38. **Lockheed Martin**
    - URL: https://www.lockheedmartin.com/en-us/careers.html
    - Searchable: Yes
    - API Available: No

### Telecommunications

39. **Verizon**
    - URL: https://www.verizon.com/about/careers
    - Searchable: Yes
    - API Available: No

40. **AT&T**
    - URL: https://www.att.jobs/
    - Searchable: Yes
    - API Available: No

### Energy

41. **ExxonMobil**
    - URL: https://corporate.exxonmobil.com/careers
    - Searchable: Yes
    - API Available: No

42. **Chevron**
    - URL: https://careers.chevron.com/
    - Searchable: Yes
    - API Available: No

---

## Notes for Agent Implementation

### Search Methods:
1. **Web Scraping:** Most sites require web scraping (check robots.txt and terms of service)
2. **RSS Feeds:** Some companies provide RSS feeds for job postings
3. **Direct API:** Very few companies provide public APIs
4. **Job Aggregators:** Consider using aggregators like LinkedIn, Indeed, Glassdoor as alternative sources

### Important Considerations:
- **Rate Limiting:** Respect robots.txt and implement delays between requests
- **Terms of Service:** Review each company's ToS before scraping
- **Data Structure:** Job postings vary in format across companies
- **Authentication:** Some sites may require login for full access
- **Legal Compliance:** Ensure compliance with web scraping laws and regulations

### Recommended Approach:
For the assignment, the agent can:
1. Accept job posting URLs or text as input (manual copy-paste)
2. Analyze the job description against student profile
3. Provide fitment analysis and skill gap identification
4. Knowledge base can contain sample job postings from these companies

---

**Last Updated:** 2025-11-29  
**Purpose:** Reference list for Job Fitment Analysis Agent knowledge base

