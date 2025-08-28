"""
io_handler.py - Input/Output Module
Handles all input and output operations for the sorting application.
"""

import sys
from typing import List, Union, Any


def parse_input(input_str: str) -> List[Union[int, float, str]]:
    if not input_str or not input_str.strip():
        return []
    
    data = []
    for item in input_str.split():
        try:
            # Try integer first
            data.append(int(item))
        except ValueError:
            try:
                # Try float next
                data.append(float(item))
            except ValueError:
                # Keep as string
                data.append(item)
    return data


def read_keyboard_input() -> List[Union[int, float, str]]:
    try:
        print("Enter items separated by spaces (or 'q' to quit):")
        user_input = input(">>> ").strip()
        
        if user_input.lower() == 'q':
            return []
            
        return parse_input(user_input)
        
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return []


def read_file_input(filename: str) -> List[Union[int, float, str]]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                print(f"Warning: File '{filename}' is empty.")
                return []
            return parse_input(content)
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied reading '{filename}'.")
        return []
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return []


def write_screen_output(data: List[Any], label: str = "Result") -> None:
    if not data:
        print(f"{label}: (empty)")
    else:
        print(f"{label}: {' '.join(map(str, data))}")


def write_file_output(data: List[Any], filename: str) -> bool:
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            if data:
                file.write(' '.join(map(str, data)) + '\n')
            else:
                file.write('(empty)\n')
        
        print(f"Output written to '{filename}'")
        return True
        
    except PermissionError:
        print(f"Error: Permission denied writing to '{filename}'.")
        return False
    except Exception as e:
        print(f"Error writing to file '{filename}': {e}")
        return False


def get_file_size(filename: str) -> int:
    try:
        import os
        return os.path.getsize(filename)
    except Exception:
        return -1


def file_exists(filename: str) -> bool:
    try:
        import os
        return os.path.isfile(filename)
    except Exception:
        return False


# Module-level test function
def test_io_module():
    print("Testing I/O module...")
    
    # Test parsing
    test_input = "42 3.14 apple 99 zebra"
    parsed = parse_input(test_input)
    print(f"Parsed '{test_input}': {parsed}")
    print(f"Types: {[type(x).__name__ for x in parsed]}")
    
    # Test screen output
    write_screen_output(parsed, "Parsed Data")
    
    # Test empty input
    empty_parsed = parse_input("")
    print(f"Empty input result: {empty_parsed}")


if __name__ == "__main__":
    test_io_module()