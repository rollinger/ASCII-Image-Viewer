import tty
import sys
import termios

def getch():
    # Save the current terminal settings
    old_settings = termios.tcgetattr(sys.stdin)
    
    try:
        # Set the terminal to raw mode
        tty.setraw(sys.stdin.fileno())
        
        # Read a single character
        char = sys.stdin.read(1)
        return char
    finally:
        # Restore the terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

# Example usage
if __name__ == "__main__":
  while True:
      key = getch()
      if key == 'q':  # Press 'q' to exit the loop
          break
      elif key == 'w':
          print("You pressed 'w'")
      elif key == 'a':
          print("You pressed 'a'")
      elif key == 's':
          print("You pressed 's'")
      elif key == 'd':
          print("You pressed 'd'")
