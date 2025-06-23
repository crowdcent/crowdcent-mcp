import sys
import platform
import os
from datetime import datetime


# ANSI color codes for terminal output
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_startup_banner():
    """Print a cool ASCII art banner and system info on startup"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
   ██████╗██████╗  ██████╗ ██╗    ██╗██████╗  ██████╗███████╗███╗   ██╗████████╗
  ██╔════╝██╔══██╗██╔═══██╗██║    ██║██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝
  ██║     ██████╔╝██║   ██║██║ █╗ ██║██║  ██║██║     █████╗  ██╔██╗ ██║   ██║   
  ██║     ██╔══██╗██║   ██║██║███╗██║██║  ██║██║     ██╔══╝  ██║╚██╗██║   ██║   
  ╚██████╗██║  ██║╚██████╔╝╚███╔███╔╝██████╔╝╚██████╗███████╗██║ ╚████║   ██║   
   ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   
{Colors.RESET}
{Colors.MAGENTA}{"═" * 80}{Colors.RESET}
{Colors.GREEN}🚀 MCP Server for the Crowdcent Challenge{Colors.RESET}
{Colors.MAGENTA}{"═" * 80}{Colors.RESET}
"""

    print(banner)

    # System information
    print(f"{Colors.YELLOW}📊 System Information:{Colors.RESET}")
    print(
        f"   {Colors.DIM}├─{Colors.RESET} Platform: {Colors.CYAN}{platform.system()} {platform.release()}{Colors.RESET}"
    )
    print(
        f"   {Colors.DIM}├─{Colors.RESET} Python: {Colors.CYAN}{sys.version.split()[0]}{Colors.RESET}"
    )
    print(
        f"   {Colors.DIM}├─{Colors.RESET} Process ID: {Colors.CYAN}{os.getpid()}{Colors.RESET}"
    )
    print(
        f"   {Colors.DIM}└─{Colors.RESET} Started: {Colors.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}"
    )
    print()

    # Available tools summary
    print(f"{Colors.YELLOW}🛠️  Available Tools:{Colors.RESET}")
    tools = [
        "list_all_challenges",
        "get_challenge_info", 
        "switch_challenge",
        "list_training_datasets",
        "download_training_dataset",
        "download_inference_data",
        "submit_predictions_from_file",
        "submit_predictions_from_dataframe",
        "list_submissions",
        "get_submission",
        "download_meta_model",
        "get_training_dataset_info",
        "get_inference_data_info",
    ]

    # Display tools in columns
    cols = 2
    for i in range(0, len(tools), cols):
        row_tools = tools[i : i + cols]
        print(f"   {Colors.DIM}├─{Colors.RESET} ", end="")
        for j, tool in enumerate(row_tools):
            print(f"{Colors.GREEN}✓{Colors.RESET} {tool:<32}", end="")
        print()

    print(f"\n{Colors.MAGENTA}{'═' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}✨ Server starting...{Colors.RESET}\n")


def print_shutdown_message():
    """Print a cool shutdown message"""
    print(f"\n{Colors.MAGENTA}{'═' * 80}{Colors.RESET}")
    print(f"{Colors.YELLOW}🛑 Shutting down CrowdCent MCP Server...{Colors.RESET}")
    print(
        f"{Colors.CYAN}Thanks for using CrowdCent! See you next time! 👋{Colors.RESET}"
    )
    print(f"{Colors.MAGENTA}{'═' * 80}{Colors.RESET}\n")


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print_shutdown_message()
    sys.exit(0)
