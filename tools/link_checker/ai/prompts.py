"""
Prompts for AI analysis
Externalized to keep main code clean
"""

AI_SYSTEM_PROMPT = "You are a web quality assurance expert."

AI_USER_PROMPT_TEMPLATE = """Analyze the following link check results and provide:
1. Overall assessment
2. Specific issues
3. Recommendations
4. Priority actions

Results:
- Passed: {passed_count} tests
- Failed: {failed_count} tests
- Warnings: {warnings_count} warnings
- Pages checked: {pages_checked}
- Links checked: {links_checked}

URL: {base_url}
Max Depth: {max_depth}
Page Title: {page_title}

Provide a concise, actionable analysis."""


def get_ai_prompt(summary, test_data):
    """
    Generate AI analysis prompt from summary and test data
    
    Args:
        summary: CheckSummary object
        test_data: TestData object
        
    Returns:
        Formatted prompt string
    """
    return AI_USER_PROMPT_TEMPLATE.format(
        passed_count=len(summary.passed),
        failed_count=len(summary.failed),
        warnings_count=len(summary.warnings),
        pages_checked=summary.pages_checked,
        links_checked=summary.total_links_checked,
        base_url=test_data.base_url,
        max_depth=test_data.max_depth,
        page_title=test_data.page_title
    )

