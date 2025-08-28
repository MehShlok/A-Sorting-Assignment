<!-- USE Ctrl+Shift+V in VSCode to preview the following markdown -->
# The Sorting Assignment (A step-by-step usage guide)
A modular Python application that demonstrates **separation of concerns** across sorting, I/O, networking, and orchestration layers.

---

## Features

- **Sorting Module (`sorting.py`)**
  - Implements core business logic (`sort_data()`).
  - Provides utility functions: `sort_data_inplace()`, `is_sorted()`, and built-in self-tests.
  - Handles mixed data types by converting non-comparable elements into strings.

- **I/O Module (`io_handler.py`)**
  - Abstracts console and file operations.
  - Functions: `read_keyboard_input()`, `write_screen_output()`, `read_file_input()`, `write_file_output()`.
  - `parse_input()` detects integers, floats, and strings automatically.

- **Networking Module (`network_handler.py`)**
  - Provides `NetworkServer` and `NetworkClient` classes.
  - Supports TCP communication with customizable handlers.
  - Includes `create_sorting_handler()` to bridge sorting logic with network requests.

- **Main Orchestrator (`main.py`)**
  - Command-line entry point.
  - Routes execution to the correct module based on CLI arguments.
  - Demonstrates clean separation between orchestration and core logic.

Run the following command to display usage information:
```bash
  python3 main.py
```

---

## Requirements
- A Python **3.8+** version. To check your current version, execute the following command:
```bash
python3 --version
```

---

## Modes of Operation

### 1. **Keyboard Input Mode**
Interactive sorting directly from the terminal.
```bash
python3 main.py keyboard
```

### 2. **File Mode**
Read input from a file and write sorted output to another file (or display on screen if no output file is provided).
```bash
python3 main.py file <input_file> [output_file]
```

### 3. **In-place File Sorting**
Sort a file and overwrite it with the sorted content.
```bash
python3 main.py file_inplace <filename>
``` 

### 4. **Network Server Mode**
Start a TCP server that listens for sorting requests.
```bash
python3 main.py server [port] 
```

### 5. **Network Client Mode**
Connect to a server and send data for sorting.
```bash
python3 main.py client "<data>" [host] [port]
```

### 6. **Test Mode**
Run built-in tests for all modules.
```bash
python3 main.py test
```
### 7. **Test individual modules**
```bash
python3 sorting.py           # Test sorting module
python3 io_handler.py        # Test I/O module  
python3 network_handler.py   # Test network module
```

## A common error 

If you run the `network_handler.py` module directly without starting the server first:

```bash
$ python3 network_handler.py
Testing network module...
Server reachable: False
Client response: Error: Cannot connect to server at localhost:8080
```
This is expected behavior because the server is not running.
To fix this, start the server first,
```bash
$ python3 network_handler.py server
```
Then run the client again to send data.

An individual course project by 
**Shlok Mehendale**
