"""
network_handler.py - Network Module
Handles network communication for remote sorting operations.
"""

import socket
import threading
import time
from typing import Callable, Any


class NetworkServer:
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.client_handler = None
    
    def set_client_handler(self, handler: Callable[[str], str]):
        self.client_handler = handler
    
    def handle_client_connection(self, client_socket: socket.socket, address: tuple):
        print(f"Connection established with {address}")
        
        try:
            while self.is_running:
                data = client_socket.recv(1024).decode('utf-8').strip()
                
                if not data:
                    break
                
                print(f"Received from {address}: {data}")
                
                # Process data using the handler
                if self.client_handler:
                    response = self.client_handler(data)
                else:
                    response = f"Echo: {data}"
                
                client_socket.send(f"{response}\n".encode('utf-8'))
                
        except ConnectionResetError:
            print(f"Client {address} disconnected unexpectedly")
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {address} closed")
    
    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.is_running = True
            print(f"Server listening on {self.host}:{self.port}")
            print("Press Ctrl+C to stop the server")
            
            while self.is_running:
                try:
                    client_socket, address = self.server_socket.accept()
                    
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client_connection,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except OSError:
                    # Server socket was closed
                    break
                    
        except KeyboardInterrupt:
            print("\nShutting down server...")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop_server()
    
    def stop_server(self):
        """Stop the network server."""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
            print("Server stopped")


class NetworkClient:
    
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port
    
    def send_data(self, data: str, timeout: int = 5) -> str:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)
            
            # Connect to server
            client_socket.connect((self.host, self.port))
            
            # Send data
            client_socket.send(data.encode('utf-8'))
            
            # Receive response
            response = client_socket.recv(1024).decode('utf-8').strip()
            
            client_socket.close()
            return response
            
        except ConnectionRefusedError:
            return f"Error: Cannot connect to server at {self.host}:{self.port}"
        except socket.timeout:
            return f"Error: Connection timeout after {timeout} seconds"
        except Exception as e:
            return f"Error: {e}"
    
    def test_connection(self) -> bool:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2)
            result = client_socket.connect_ex((self.host, self.port))
            client_socket.close()
            return result == 0
        except Exception:
            return False


def create_sorting_handler(sort_function: Callable[[list], list], 
                         parse_function: Callable[[str], list]) -> Callable[[str], str]:
    def handler(input_data: str) -> str:
        try:
            # Parse input
            data = parse_function(input_data)
            
            if not data:
                return "Error: No valid data to sort"
            
            # Sort data
            sorted_data = sort_function(data)
            
            # Return sorted result
            return ' '.join(map(str, sorted_data))
            
        except Exception as e:
            return f"Error processing data: {e}"
    
    return handler


# Module-level test functions
def test_network_module():
    print("Testing network module...")
    
    # Test client without server (should fail gracefully)
    client = NetworkClient()
    print(f"Server reachable: {client.test_connection()}")
    
    response = client.send_data("test data")
    print(f"Client response: {response}")


def run_test_server():
    server = NetworkServer()
    
    def echo_handler(data: str) -> str:
        return f"Echo: {data}"
    
    server.set_client_handler(echo_handler)
    server.start_server()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        run_test_server()
    else:
        test_network_module()