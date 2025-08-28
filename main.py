#!/usr/bin/env python3
"""
main.py - Main Application Module
Entry point for the modular sorting application.
This module orchestrates all other modules and provides the CLI interface.
"""

import sys
import os

# Import our custom modules
try:
    from sorting import sort_data
    from io_handler import (
        read_keyboard_input, 
        read_file_input, 
        write_screen_output, 
        write_file_output,
        parse_input
    )
    from network_handler import NetworkServer, NetworkClient, create_sorting_handler
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all module files are in the same directory as main.py")
    sys.exit(1)


def show_usage():
    """Display usage information."""
    print("A Modular Sorting Application")
    print("=" * 40)
    print("Usage:")
    print("  python main.py keyboard                    - Interactive keyboard input")
    print("  python main.py file <input> [output]       - File input/output")
    print("  python main.py file_inplace <filename>     - In-place file sorting")
    print("  python main.py server [port]               - Start network server")
    print("  python main.py client <data> [host] [port] - Send data to server")
    print("  python main.py test                        - Run module tests")
    print()
    print("Examples:")
    print("  python main.py keyboard")
    print("  python main.py file numbers.txt sorted.txt")
    print("  python main.py file_inplace data.txt")
    print("  python main.py server 8080")
    print("  python main.py client '3 1 4 1 5 9 2 6' localhost 8080")


def handle_keyboard_mode():
    print("=== Keyboard Input Mode ===")
    while True:
        data = read_keyboard_input()
        
        if not data:  # User quit or error
            break
        
        # Call the sorting function (independent of main)
        sorted_data = sort_data(data)
        
        # Display results
        write_screen_output(data, "Original")
        write_screen_output(sorted_data, "Sorted")
        print("-" * 30)


def handle_file_mode(input_file: str, output_file: str = None):
    print(f"=== File Mode: {input_file} ===")
    
    # Read input from file
    data = read_file_input(input_file)
    
    if not data:
        print("No data to sort.")
        return
    
    print(f"Read {len(data)} items from '{input_file}'")
    write_screen_output(data, "Original data")
    
    sorted_data = sort_data(data)
    
    if output_file:
        # Write to different file
        success = write_file_output(sorted_data, output_file)
        if success:
            write_screen_output(sorted_data, "Sorted data")
    else:
        # Display on screen only
        write_screen_output(sorted_data, "Sorted data")


def handle_file_inplace_mode(filename: str):
    print(f"=== In-place File Mode: {filename} ===")
    
    # Read from file
    data = read_file_input(filename)
    
    if not data:
        print("No data to sort.")
        return
    
    print(f"Original content ({len(data)} items):")
    write_screen_output(data, "Before")
    
    sorted_data = sort_data(data)
    
    # Write back to same file
    success = write_file_output(sorted_data, filename)
    
    if success:
        write_screen_output(sorted_data, "After")
        print(f"File '{filename}' has been sorted in-place.")


def handle_server_mode(port: int = 8080):
    print(f"=== Network Server Mode (Port {port}) ===")
    
    # Create server
    server = NetworkServer('localhost', port)
    
    # Create handler that uses our sorting function
    handler = create_sorting_handler(sort_data, parse_input)
    server.set_client_handler(handler)
    
    # Start server
    print("Starting sorting server...")
    print("Server will sort any data sent to it and return results")
    server.start_server()


def handle_client_mode(data: str, host: str = 'localhost', port: int = 8080):
    print(f"=== Network Client Mode ({host}:{port}) ===")
    
    # Create client
    client = NetworkClient(host, port)
    
    # Test connection first
    if not client.test_connection():
        print(f"Cannot connect to server at {host}:{port}")
        print("Make sure the server is running first.")
        return
    
    print(f"Sending data: {data}")
    
    response = client.send_data(data)
    print(f"Server response: {response}")


def run_module_tests():
    print("=== Running Module Tests ===")
    
    print("\n1. Testing sorting module:")
    from sorting import test_sorting_module
    test_sorting_module()
    
    print("\n2. Testing I/O module:")
    from io_handler import test_io_module
    test_io_module()
    
    print("\n3. Testing network module:")
    from network_handler import test_network_module
    test_network_module()
    
    print("\n=== All Tests Completed ===")


def main():
    if len(sys.argv) < 2:
        show_usage()
        return
    
    mode = sys.argv[1].lower()
    
    try:
        if mode == 'keyboard':
            handle_keyboard_mode()
            
        elif mode == 'file':
            if len(sys.argv) < 3:
                print("Error: Please provide input filename")
                print("Usage: python main.py file <input_file> [output_file]")
                return
            
            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            handle_file_mode(input_file, output_file)
            
        elif mode == 'file_inplace':
            if len(sys.argv) < 3:
                print("Error: Please provide filename")
                print("Usage: python main.py file_inplace <filename>")
                return
            
            filename = sys.argv[2]
            handle_file_inplace_mode(filename)
            
        elif mode == 'server':
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
            handle_server_mode(port)
            
        elif mode == 'client':
            if len(sys.argv) < 3:
                print("Error: Please provide data to send")
                print("Usage: python main.py client <data> [host] [port]")
                return
            
            data = sys.argv[2]
            host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
            port = int(sys.argv[4]) if len(sys.argv) > 4 else 8080
            handle_client_mode(data, host, port)
            
        elif mode == 'test':
            run_module_tests()
            
        else:
            print(f"Error: Unknown mode '{mode}'")
            show_usage()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()