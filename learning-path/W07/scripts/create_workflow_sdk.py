#!/usr/bin/env python3
"""
OpenAI Agent Builder Workflow Creation Script
Creates workflows programmatically using OpenAI API instead of manual clickops.

Based on: https://platform.openai.com/docs/guides/agent-builder
"""

import os
import json
import sys
from pathlib import Path
from openai import OpenAI
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load .env file from repository root
# Script is in: learning-path/W07/scripts/
# Repository root is 3 levels up
script_dir = Path(__file__).parent
repo_root = script_dir.parent.parent.parent
env_file = repo_root / ".env"

if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Loaded .env from: {env_file}")
else:
    # Try loading from current directory or parent
    load_dotenv()
    print(f"⚠️  .env file not found at {env_file}")
    print(f"   Looking for .env in: {Path.cwd()}")
    if not os.getenv("OPENAI_API_KEY"):
        print("   ⚠️  OPENAI_API_KEY not found. Please set it in .env file or environment.")

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in environment variables.")
    print("   Create a .env file in the repository root with:")
    print("   OPENAI_API_KEY=your-api-key-here")
    sys.exit(1)

client = OpenAI(api_key=api_key)

def create_workflow_definition(workflow_name: str, workflow_type: str = "job_search") -> Dict[str, Any]:
    """
    Create workflow definition based on our documented workflows.
    
    Args:
        workflow_name: Name of the workflow
        workflow_type: Either "job_search" or "qualification_check"
    
    Returns:
        Workflow definition dictionary
    """
    
    if workflow_type == "job_search":
        return {
            "name": workflow_name,
            "description": "Job Search & Fitment Analysis Workflow",
            "nodes": [
                {
                    "id": "user_input",
                    "type": "agent",
                    "name": "User Input",
                    "config": {
                        "system_prompt": "Accept user profile input for job search. Profile should include: skills (array), experience (string), education (string), target_companies (array).",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "profile": {
                                    "type": "object",
                                    "properties": {
                                        "skills": {"type": "array", "items": {"type": "string"}},
                                        "experience": {"type": "string"},
                                        "education": {"type": "string"},
                                        "target_companies": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["skills", "experience", "education"]
                                }
                            }
                        }
                    }
                },
                {
                    "id": "validate_input",
                    "type": "if_else",
                    "name": "Validate Input",
                    "config": {
                        "condition": "profile.skills && profile.experience && profile.education",
                        "true_path": "load_companies",
                        "false_path": "error_end"
                    }
                },
                {
                    "id": "load_companies",
                    "type": "transform",
                    "name": "Load Companies",
                    "config": {
                        "operation": "read_csv",
                        "file": "target-companies.csv",
                        "filter": {"status": "active"}
                    }
                },
                {
                    "id": "search_job_sites",
                    "type": "tool",
                    "name": "Search Job Sites",
                    "config": {
                        "tool_type": "web_scraper",
                        "targets": "{{load_companies.output.careers_url}}"
                    }
                },
                {
                    "id": "jobs_found_check",
                    "type": "if_else",
                    "name": "Jobs Found?",
                    "config": {
                        "condition": "search_job_sites.output.jobs.length > 0",
                        "true_path": "extract_job_details",
                        "false_path": "no_results_end"
                    }
                },
                {
                    "id": "extract_job_details",
                    "type": "transform",
                    "name": "Extract Job Details",
                    "config": {
                        "operation": "parse_job_postings",
                        "fields": ["title", "description", "requirements", "skills", "location"]
                    }
                },
                {
                    "id": "analyze_profile_match",
                    "type": "agent",
                    "name": "Analyze Profile Match",
                    "config": {
                        "system_prompt": "You are a Job Fitment Analysis Agent. Analyze job postings against student profiles. Calculate fitment percentages based on skills, experience, and education matches. Return structured analysis with matched skills, gaps, and fitment score.",
                        "input": "{{extract_job_details.output}} + {{user_input.output.profile}}"
                    }
                },
                {
                    "id": "calculate_fitment",
                    "type": "transform",
                    "name": "Calculate Fitment",
                    "config": {
                        "formula": "(matched_required_skills * 0.4) + (matched_preferred_skills * 0.2) + (experience_match * 0.2) + (education_match * 0.2)"
                    }
                },
                {
                    "id": "identify_skill_gaps",
                    "type": "transform",
                    "name": "Identify Skill Gaps",
                    "config": {
                        "operation": "compare_skills",
                        "required": "{{extract_job_details.output.required_skills}}",
                        "user": "{{user_input.output.profile.skills}}"
                    }
                },
                {
                    "id": "rank_results",
                    "type": "transform",
                    "name": "Rank Results",
                    "config": {
                        "operation": "sort",
                        "by": "fitment_percentage",
                        "order": "desc",
                        "limit": 10,
                        "priority_boost": 0.1
                    }
                },
                {
                    "id": "end",
                    "type": "end",
                    "name": "End",
                    "config": {
                        "output_format": "json",
                        "output": {
                            "jobs": "{{rank_results.output}}",
                            "fitment_scores": "{{calculate_fitment.output}}",
                            "skill_gaps": "{{identify_skill_gaps.output}}"
                        }
                    }
                }
            ],
            "edges": [
                {"from": "user_input", "to": "validate_input"},
                {"from": "validate_input", "to": "load_companies", "condition": "true"},
                {"from": "validate_input", "to": "error_end", "condition": "false"},
                {"from": "load_companies", "to": "search_job_sites"},
                {"from": "search_job_sites", "to": "jobs_found_check"},
                {"from": "jobs_found_check", "to": "extract_job_details", "condition": "true"},
                {"from": "jobs_found_check", "to": "no_results_end", "condition": "false"},
                {"from": "extract_job_details", "to": "analyze_profile_match"},
                {"from": "analyze_profile_match", "to": "calculate_fitment"},
                {"from": "calculate_fitment", "to": "identify_skill_gaps"},
                {"from": "identify_skill_gaps", "to": "rank_results"},
                {"from": "rank_results", "to": "end"}
            ]
        }
    
    else:  # qualification_check
        return {
            "name": workflow_name,
            "description": "Job Qualification Check Workflow",
            "nodes": [
                {
                    "id": "job_url_input",
                    "type": "agent",
                    "name": "Job URL Input",
                    "config": {
                        "system_prompt": "Accept job posting URL and user profile for qualification check.",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "job_url": {"type": "string", "format": "uri"},
                                "profile": {"type": "object"}
                            },
                            "required": ["job_url", "profile"]
                        }
                    }
                },
                {
                    "id": "validate_url",
                    "type": "if_else",
                    "name": "Validate URL",
                    "config": {
                        "condition": "is_valid_url(job_url_input.output.job_url) && job_url_input.output.profile",
                        "true_path": "access_job_posting",
                        "false_path": "error_end"
                    }
                },
                {
                    "id": "access_job_posting",
                    "type": "tool",
                    "name": "Access Job Posting",
                    "config": {
                        "tool_type": "web_scraper",
                        "url": "{{job_url_input.output.job_url}}"
                    }
                },
                {
                    "id": "posting_accessible",
                    "type": "if_else",
                    "name": "Posting Accessible?",
                    "config": {
                        "condition": "access_job_posting.output.status === 'success'",
                        "true_path": "extract_requirements",
                        "false_path": "access_error_end"
                    }
                },
                {
                    "id": "extract_requirements",
                    "type": "transform",
                    "name": "Extract Requirements",
                    "config": {
                        "operation": "parse_job_posting",
                        "fields": ["required_skills", "preferred_skills", "experience", "education"]
                    }
                },
                {
                    "id": "load_user_profile",
                    "type": "transform",
                    "name": "Load User Profile",
                    "config": {
                        "operation": "load_from_kb",
                        "profile_id": "{{job_url_input.output.profile.id}}"
                    }
                },
                {
                    "id": "compare_requirements",
                    "type": "agent",
                    "name": "Compare Requirements",
                    "config": {
                        "system_prompt": "Compare job requirements against user profile. Identify matched skills, missing qualifications, and calculate fitment percentage.",
                        "input": "{{extract_requirements.output}} + {{load_user_profile.output}}"
                    }
                },
                {
                    "id": "calculate_fitment",
                    "type": "transform",
                    "name": "Calculate Fitment",
                    "config": {
                        "formula": "(matched_required * 0.4) + (matched_preferred * 0.2) + (experience * 0.2) + (education * 0.2)"
                    }
                },
                {
                    "id": "identify_matches",
                    "type": "transform",
                    "name": "Identify Matches",
                    "config": {
                        "operation": "list_matches",
                        "source": "{{compare_requirements.output}}"
                    }
                },
                {
                    "id": "identify_gaps",
                    "type": "transform",
                    "name": "Identify Gaps",
                    "config": {
                        "operation": "list_gaps",
                        "source": "{{compare_requirements.output}}"
                    }
                },
                {
                    "id": "generate_recommendation",
                    "type": "if_else",
                    "name": "Generate Recommendation",
                    "config": {
                        "condition": "calculate_fitment.output.fitment_percentage",
                        "branches": [
                            {"condition": ">= 80", "path": "recommend_apply"},
                            {"condition": ">= 60", "path": "recommend_consider"},
                            {"condition": "< 60", "path": "recommend_improve"}
                        ]
                    }
                },
                {
                    "id": "end",
                    "type": "end",
                    "name": "End",
                    "config": {
                        "output_format": "json",
                        "output": {
                            "fitment_percentage": "{{calculate_fitment.output.fitment_percentage}}",
                            "matched_skills": "{{identify_matches.output}}",
                            "missing_skills": "{{identify_gaps.output}}",
                            "recommendation": "{{generate_recommendation.output}}"
                        }
                    }
                }
            ],
            "edges": [
                {"from": "job_url_input", "to": "validate_url"},
                {"from": "validate_url", "to": "access_job_posting", "condition": "true"},
                {"from": "validate_url", "to": "error_end", "condition": "false"},
                {"from": "access_job_posting", "to": "posting_accessible"},
                {"from": "posting_accessible", "to": "extract_requirements", "condition": "true"},
                {"from": "posting_accessible", "to": "access_error_end", "condition": "false"},
                {"from": "extract_requirements", "to": "load_user_profile"},
                {"from": "load_user_profile", "to": "compare_requirements"},
                {"from": "compare_requirements", "to": "calculate_fitment"},
                {"from": "calculate_fitment", "to": "identify_matches"},
                {"from": "identify_matches", "to": "identify_gaps"},
                {"from": "identify_gaps", "to": "generate_recommendation"},
                {"from": "generate_recommendation", "to": "end"}
            ]
        }


def create_workflow_via_api(workflow_definition: Dict[str, Any]) -> Optional[str]:
    """
    Create workflow using OpenAI API.
    
    Note: As of current documentation, workflows are primarily created via Agent Builder UI.
    This function attempts to use the API if available, otherwise provides the workflow definition
    that can be imported into Agent Builder.
    
    Args:
        workflow_definition: Workflow definition dictionary
    
    Returns:
        Workflow ID or instructions for manual import
    """
    
    # Check if workflows API is available
    # Note: OpenAI may not have a public API for workflow creation yet
    # The Agent Builder UI is the primary method
    
    try:
        # Attempt to use workflows API (if available)
        # This is experimental and may not be available
        response = client.beta.workflows.create(**workflow_definition)
        return response.id
    except AttributeError:
        # API not available - return workflow definition for manual import
        print("⚠️  Workflow creation API not available.")
        print("📝 Workflow definition created. Use one of these methods:")
        print("\n1. Import into Agent Builder:")
        print("   - Go to https://platform.openai.com/agent-builder/")
        print("   - Create new workflow")
        print("   - Use 'Import' or 'Code' option if available")
        print("\n2. Manual creation:")
        print("   - Follow the workflow diagrams in docs/workflow-diagrams/workflows.html")
        print("   - Use the step-by-step instructions provided")
        print("\n3. Download workflow code after UI creation:")
        print("   - Create workflow in Agent Builder UI")
        print("   - Click 'Code' in top navigation")
        print("   - Download Agent SDK code")
        
        return None


def save_workflow_definition(workflow_definition: Dict[str, Any], filename: str = "workflow_definition.json"):
    """Save workflow definition to JSON file for manual import."""
    output_path = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(output_path, 'w') as f:
        json.dump(workflow_definition, f, indent=2)
    print(f"✅ Workflow definition saved to: {output_path}")
    return output_path


def main():
    """Main function to create workflows."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create OpenAI Agent Builder workflows programmatically")
    parser.add_argument("--workflow", choices=["job_search", "qualification_check", "both"], 
                       default="both", help="Which workflow to create")
    parser.add_argument("--output", default="workflow_definition.json", 
                       help="Output filename for workflow definition")
    parser.add_argument("--api", action="store_true", 
                       help="Attempt to create via API (may not be available)")
    
    args = parser.parse_args()
    
    workflows_to_create = []
    if args.workflow in ["job_search", "both"]:
        workflows_to_create.append(("Job Search & Fitment Analysis", "job_search"))
    if args.workflow in ["qualification_check", "both"]:
        workflows_to_create.append(("Job Qualification Check", "qualification_check"))
    
    for name, workflow_type in workflows_to_create:
        print(f"\n📋 Creating workflow: {name}")
        workflow_def = create_workflow_definition(name, workflow_type)
        
        if args.api:
            workflow_id = create_workflow_via_api(workflow_def)
            if workflow_id:
                print(f"✅ Workflow created with ID: {workflow_id}")
        else:
            filename = f"{workflow_type}_{args.output}"
            save_workflow_definition(workflow_def, filename)
            create_workflow_via_api(workflow_def)  # This will print instructions


if __name__ == "__main__":
    main()

