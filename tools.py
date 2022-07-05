from __future__ import annotations

import numpy as np


def check_conseq_nums(arr: np.ndarray, min_conseq: int) -> tuple[bool, int]:
    """
    Check if there are consecutive numbers in the array
    """

    if arr.size < min_conseq:
        return False, -1

    for i, num in enumerate(arr[:-(min_conseq-1)]):
        if np.all(arr[i:i+min_conseq] == num):
            return True, num
    return False, -1
