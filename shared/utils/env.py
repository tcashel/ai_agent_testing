"""Environment variable utilities."""

import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv


def load_env(
    env_path: Optional[Union[str, Path]] = None, 
    project_root: bool = True
) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Path to .env file (defaults to .env in current directory)
        project_root: Whether to also load .env from project root
    """
    # Load project-specific .env if provided
    if env_path:
        path = Path(env_path) if isinstance(env_path, str) else env_path
        load_dotenv(path)
    else:
        # Load from current directory
        load_dotenv()
    
    # Also load from project root if requested
    if project_root:
        # Find project root (contains .git)
        current = Path.cwd()
        root = current
        
        while root != root.parent:
            if (root / ".git").exists():
                break
            root = root.parent
            
        # Load .env from root if found and different from current
        if root != current and (root / ".env").exists():
            load_dotenv(root / ".env")
            print(f"Loaded environment from {root / '.env'}")