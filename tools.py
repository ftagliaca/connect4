from __future__ import annotations

import numpy as np


def check_conseq_nums(arr: np.ndarray, min_conseq: int) -> bool:
    """
    Check if there are consecutive numbers in the array
    """

    for i, num in enumerate(arr[:-min_conseq]):
        if arr[i:i+min_conseq] == num:
            return True
    return False
