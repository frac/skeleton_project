import sys
import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Get the src directory path
src_path = Path(__file__).parent.parent / "src"

# Add to Python path
sys.path.insert(0, str(src_path))

