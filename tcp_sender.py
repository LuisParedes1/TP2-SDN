import socket
import sys

def send_tcp_package(host, port, timeout):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)

        try:
            # Connect to the server
            s.connect((host, port))

            # Send a simple message
            message = 'Hello, server!'
            s.sendall(message.encode())

            # Receive a response (optional)
            data = s.recv(1024)
            print('Received:', data.decode())

        except socket.timeout:
            print(f"Connection timed out after {timeout} seconds")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # CLI arguments (you can enhance this part for better CLI interaction)
    if len(sys.argv) != 4:
        print("Usage: script.py <host> <port> <timeout>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    timeout = float(sys.argv[3])

    send_tcp_package(host, port, timeout)