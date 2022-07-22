from __future__ import annotations

import numpy as np


def check_conseq_nums(arr: np.ndarray, min_conseq: int) -> tuple[bool, int]:
    """Helper function to check whether there are min_conseq consequtive numbers in the array

    Args:
        arr (np.ndarray): The array to check for consequtive numbers
        min_conseq (int): The minimum number of consequtive numbers required

    Returns:
        tuple[bool, int]: Whether there are min_conseq consequtive numbers in the array
                          and the ID of the number that is repeated min_conseq times (consecutively)
    """

    if arr.size < min_conseq:
        return False, -1

    for i, num in enumerate(arr[:-(min_conseq-1)]):
        if np.all(arr[i:i+min_conseq] == num):
            return True, num
    return False, -1
