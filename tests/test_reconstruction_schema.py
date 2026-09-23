from pathlib import Path
import importlib.util

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "reconstruction"
    / "validate_reconstruction.py"
)
spec = importlib.util.spec_from_file_location("validate_reconstruction", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_current_reconstruction_skeleton_is_valid():
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "reconstruction"
        / "galloway_exhibit1a_reconstructed.csv"
    )
    assert module.validate(path) == []
