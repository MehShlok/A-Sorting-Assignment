"""
sorting.py - Core Sorting Module
Contains the main sorting functionality that can be called from anywhere.
"""

from typing import List, Any, Union


def sort_data(data: List[Any], reverse: bool = False) -> List[Any]:
    if not data:
        return []
    
    try:
        return sorted(data, reverse=reverse)
    except TypeError as e:
        # Handle case where items aren't comparable
        print(f"Warning: Unable to sort mixed incompatible types: {e}")
        return data


def sort_data_inplace(data: List[Any], reverse: bool = False) -> None:
    if not data:
        return
    
    try:
        data.sort(reverse=reverse)
    except TypeError as e:
        print(f"Warning: Unable to sort mixed incompatible types: {e}")


def is_sorted(data: List[Any], reverse: bool = False) -> bool:
    if len(data) <= 1:
        return True
    
    if reverse:
        return all(data[i] >= data[i + 1] for i in range(len(data) - 1))
    else:
        return all(data[i] <= data[i + 1] for i in range(len(data) - 1))


# Module-level test function
def test_sorting_module():
    print("Testing sorting module...")
    
    # Test numeric data
    numbers = [64, 34, 25, 12, 22, 11, 90]
    sorted_numbers = sort_data(numbers)
    print(f"Original: {numbers}")
    print(f"Sorted: {sorted_numbers}")
    print(f"Is sorted: {is_sorted(sorted_numbers)}")
    
    # Test string data
    words = ['zebra', 'apple', 'banana', 'cherry']
    sorted_words = sort_data(words)
    print(f"Words: {words} -> {sorted_words}")
    
    # Test mixed data
    mixed = [3.14, 42, 'apple', 1.41]
    try:
        sorted_mixed = sort_data(mixed)
        print(f"Mixed: {mixed} -> {sorted_mixed}")
    except Exception as e:
        print(f"Mixed data error: {e}")


if __name__ == "__main__":
    test_sorting_module()