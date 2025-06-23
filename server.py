from mcp.server.fastmcp import FastMCP
from crowdcent_challenge import ChallengeClient
import os
import json
from typing import Optional, Dict, Any
from pathlib import Path
import signal
from startup import print_startup_banner, signal_handler
from dotenv import load_dotenv

load_dotenv()


mcp = FastMCP(
    name="crowdcent-mcp",
    version="0.1.0",
    description="A MCP server for the Crowdcent challenge",
)

print_startup_banner()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Global client instance
client: Optional[ChallengeClient] = ChallengeClient(
    api_key=os.getenv("CROWDCENT_API_KEY"), challenge_slug="hyperliquid-ranking"
)


@mcp.tool()
def list_all_challenges() -> Dict[str, Any]:
    """
    List all available challenges.

    Returns:
        Dictionary containing list of challenges with their details
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        challenges = client.list_all_challenges()
        return {"challenges": challenges}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_challenge_info() -> Dict[str, Any]:
    """
    Get detailed information about the current challenge.

    Returns:
        Dictionary containing challenge details
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        challenge = client.get_challenge()
        return {"challenge": challenge}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def switch_challenge(challenge_slug: str) -> str:
    """
    Switch to a different challenge.

    Args:
        challenge_slug: The slug of the challenge to switch to

    Returns:
        Success message
    """
    if not client:
        return "Client not initialized. Call init_client first."

    try:
        client.switch_challenge(challenge_slug)
        return f"Successfully switched to challenge: {challenge_slug}"
    except Exception as e:
        return f"Error switching challenge: {str(e)}"


@mcp.tool()
def list_training_datasets() -> Dict[str, Any]:
    """
    List all available training datasets for the current challenge.

    Returns:
        Dictionary containing list of training datasets
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        datasets = client.list_training_datasets()
        return {"datasets": datasets}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def download_training_dataset(version: str, dest_path: str) -> str:
    """
    Download a specific training dataset.

    Args:
        version: The version string of the training dataset (e.g., '1.0', '2.1') or 'latest'
        dest_path: Absolute path where to save the dataset, must end with .parquet

    Returns:
        Success message or error
    """
    if not client:
        return "Client not initialized. Call init_client first."

    try:
        # Convert to absolute path and ensure .parquet extension
        path = Path(dest_path).absolute()
        if path.suffix != '.parquet':
            path = path.with_suffix('.parquet')
        
        # Create parent directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        client.download_training_dataset(version, str(path))
        return f"Successfully downloaded dataset to: {path}"
    except Exception as e:
        return f"Error downloading dataset: {str(e)}"

@mcp.tool()
def download_inference_data(
    release_date: str,
    dest_path: str,
    poll: bool = True,
    poll_interval: int = 30,
    timeout: Optional[int] = 900,
) -> str:
    """
    Download inference data for a specific period.

    Args:
        release_date: The release date in 'YYYY-MM-DD' format or 'current' or 'latest'
        dest_path: Absolute path where to save the data, must end with .parquet
        poll: Whether to wait for the inference data to be available before downloading
        poll_interval: Seconds to wait between retries when polling
        timeout: Maximum seconds to wait before raising TimeoutError (None waits indefinitely)

    Returns:
        Success message or error
    """
    if not client:
        return "Client not initialized. Call init_client first."

    try:
        # Convert to absolute path and ensure .parquet extension
        path = Path(dest_path).absolute()
        if path.suffix != '.parquet':
            path = path.with_suffix('.parquet')
        
        # Create parent directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        client.download_inference_data(
            release_date,
            str(path),
            poll=poll,
            poll_interval=poll_interval,
            timeout=timeout,
        )
        return f"Successfully downloaded inference data to: {path}"
    except Exception as e:
        return f"Error downloading inference data: {str(e)}"


@mcp.tool()
def submit_predictions_from_file(file_path: str, slot: int = 1) -> Dict[str, Any]:
    """
    Submit predictions from a Parquet file.

    Args:
        file_path: Absolute path to the predictions file, must end with .parquet
        slot: Submission slot number (1-based, default: 1)

    Returns:
        Dictionary with submission details
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        submission = client.submit_predictions(file_path=file_path, slot=slot)
        return {"submission": submission}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def submit_predictions_from_dataframe(df, slot: int = 1) -> Dict[str, Any]:
    """
    Submit predictions from a JSON representation of a dataframe.

    Args:
        df: dataframe containing predictions data
        slot: Submission slot number (1-based, default: 1)

    Returns:
        Dictionary with submission details
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        submission = client.submit_predictions(df=df, slot=slot)
        return {"submission": submission}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_submissions(period: Optional[str] = None) -> Dict[str, Any]:
    """
    List recent submissions.

    Args:
        period: Optional filter for submissions by period:
                - 'current': Only show submissions for the current active period
                - 'YYYY-MM-DD': Only show submissions for a specific inference period date

    Returns:
        Dictionary containing list of submissions
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        submissions = client.list_submissions(period=period)
        return {"submissions": submissions}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_submission(submission_id: int) -> Dict[str, Any]:
    """
    Get details about a specific submission.

    Args:
        submission_id: The ID of the submission

    Returns:
        Dictionary containing submission details
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        submission = client.get_submission(submission_id)
        return {"submission": submission}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def download_meta_model(dest_path: str) -> str:
    """
    Download the consolidated meta model for the current challenge.

    Args:
        dest_path: Absolute path where to save the meta model, must end with .parquet

    Returns:
        Success message or error
    """
    if not client:
        return "Client not initialized. Call init_client first."

    try:
        # Convert to absolute path and ensure .parquet extension
        path = Path(dest_path).absolute()
        if path.suffix != '.parquet':
            path = path.with_suffix('.parquet')
        
        # Create parent directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        client.download_meta_model(str(path))
        return f"Successfully downloaded meta model to: {path}"
    except Exception as e:
        return f"Error downloading meta model: {str(e)}"


@mcp.tool()
def get_training_dataset_info(version: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific training dataset.

    Args:
        version: The version string of the training dataset (e.g., '1.0', '2.1') or 'latest'

    Returns:
        Dictionary containing dataset details
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        dataset = client.get_training_dataset(version)
        return {"dataset": dataset}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_inference_data_info(release_date: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific inference data period.

    Args:
        release_date: The release date in 'YYYY-MM-DD' format or 'current' or 'latest'

    Returns:
        Dictionary containing inference data details
    """
    if not client:
        return {"error": "Client not initialized. Call init_client first."}

    try:
        inference_data = client.get_inference_data(release_date)
        return {"inference_data": inference_data}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
