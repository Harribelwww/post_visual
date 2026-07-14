"""Research-result plotting recipes."""

from .comparison import ablation, model_comparison
from .interpretation import embedding, feature_importance
from .metrics import calibration_curve, confusion_matrix
from .signal import connectivity_matrix
from .training import training_curves

__all__ = [
    "ablation",
    "calibration_curve",
    "confusion_matrix",
    "connectivity_matrix",
    "embedding",
    "feature_importance",
    "model_comparison",
    "training_curves",
]
