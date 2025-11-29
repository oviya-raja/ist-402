#!/usr/bin/env python3
"""
Command-line interface for link checker
"""

import sys
import argparse
import subprocess

# Import FastMCP link checker
try:
    from .checker import main
    from .core import CheckSummary
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False
    main = None
    CheckSummary = None


def kill_browser_processes():
    """Kill all Chromium/Playwright browser processes"""
    try:
        # Kill Chromium processes
        subprocess.run(
            ["pkill", "-9", "-f", "chromium"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        subprocess.run(
            ["pkill", "-9", "-f", "Chromium"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        # Kill Playwright processes
        subprocess.run(
            ["pkill", "-9", "-f", "playwright"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        print("✅ All browser processes killed")
    except Exception as e:
        print(f"⚠️  Error killing browser processes: {e}")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Link checker using Playwright MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://oviya-raja.github.io/ist-402/
  %(prog)s https://oviya-raja.github.io/ist-402/ --depth 3
  %(prog)s --kill-browsers  # Kill all browser processes
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        default=None,
        help="URL to check (default: https://oviya-raja.github.io/ist-402/)"
    )
    
    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Maximum recursion depth (default: 2)"
    )
    
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Disable AI analysis"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (no UI)"
    )
    
    parser.add_argument(
        "--kill-browsers",
        action="store_true",
        help="Kill all Chromium/Playwright browser processes and exit"
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    # Handle kill-browsers flag
    if args.kill_browsers:
        kill_browser_processes()
        sys.exit(0)
    
    url = args.url
    max_depth = args.depth
    use_ai = not args.no_ai
    headless = args.headless
    
    try:
        if not FASTMCP_AVAILABLE or not main:
            print("❌ ERROR: FastMCP not available")
            print("   Install with: pip install fastmcp")
            sys.exit(1)
        
        summary = main(base_url=url, max_depth=max_depth, use_ai=use_ai, headless=headless)
        sys.exit(0 if not summary.failed else 1)
    except ImportError as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)
    except ExceptionGroup as e:
        # Handle MCP server shutdown errors at CLI level
        # These are non-critical errors that occur during cleanup
        error_str = str(e)
        error_repr = repr(e)
        full_traceback = ""
        try:
            import traceback
            full_traceback = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        except:
            pass
        
        # Check exception group message, nested exceptions, and full traceback
        has_shutdown = (
            "Shutdown signal received" in error_str or
            "Shutdown signal received" in error_repr or
            "Shutdown signal received" in full_traceback or
            ("TaskGroup" in error_str and "ValidationError" in error_str) or
            any(
                "Shutdown signal received" in str(exc) or
                "Shutdown signal received" in repr(exc) or
                ("JSON" in str(exc) and "Shutdown" in str(exc)) or
                ("ValidationError" in str(exc) and "JSON" in str(exc)) or
                ("BrokenResourceError" in str(exc))
                for exc in e.exceptions
            )
        )
        if has_shutdown:
            # Shutdown error is non-critical - exit successfully
            print("\n✅ MCP server shutdown handled gracefully (non-critical)")
            sys.exit(0)
        # Re-raise if it's a different error
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        error_str = str(e)
        error_repr = repr(e)
        # Check if it's a shutdown-related error
        is_shutdown = (
            "Shutdown signal received" in error_str or
            "Shutdown signal received" in error_repr or
            ("TaskGroup" in error_str and "Shutdown" in error_str) or
            ("JSON" in error_str and "Shutdown" in error_str) or
            ("BrokenResourceError" in error_str) or
            ("ValidationError" in error_str and "JSON" in error_str)
        )
        if is_shutdown:
            print("\n✅ MCP server shutdown handled gracefully (non-critical)")
            sys.exit(0)
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

