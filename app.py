"""Compatibility entry point for the ChatSim SQLite workbench."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parent / "workbench/libera_workbench.py"), run_name="__main__")
