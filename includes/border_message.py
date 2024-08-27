import shutil
import sys

# ANSI escape codes for colors
RESET = "\033[0m"
CYAN_BACKGROUND_BLACK_TEXT = "\033[46;30m"  # Cyan background with black text

def get_terminal_size():
    """Get the terminal size in columns and rows."""
    columns, rows = shutil.get_terminal_size()
    return columns, rows

def create_bordered_message(message):
    """Create a message with a cyan background and black text, adapting to terminal size."""
    columns, _ = get_terminal_size()

    # Replace literal "\n" with actual newlines
    message = message.replace("\\n", "\n")

    # Split the message into lines and determine the maximum line length
    lines = message.splitlines()
    max_line_length = max(len(line) for line in lines)

    # Add padding above and below the message
    padding_lines = 3
    padded_lines = [''] * padding_lines + lines + [''] * padding_lines

    # Determine the width of the border, ensuring it spans the full terminal width
    border_width = columns

    # Create top and bottom borders with cyan background and black text
    top_bottom_border = CYAN_BACKGROUND_BLACK_TEXT + "+" + "-" * (border_width - 4) + "+" + RESET

    # Format each line to be centered within the border
    formatted_lines = [top_bottom_border]
    for line in padded_lines:
        line_content = line.center(max_line_length)  # Center the text within the maximum line length
        total_padding = border_width - len(line_content) - 4  # Calculate padding for full width
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        line_with_background = (
            CYAN_BACKGROUND_BLACK_TEXT +
            "|" + " " * left_padding + line_content + " " * right_padding + "|" +
            RESET
        )
        formatted_lines.append(line_with_background)
    formatted_lines.append(top_bottom_border)

    return ("\n".join(formatted_lines)) + "\n"

def main(message):
    bordered_message = create_bordered_message(message)
    print(bordered_message)

if __name__ == "__main__":
    # Get message from command line arguments
    input_message = "*** IMPORTANT MESSAGE ***\\n\\n\\n"
    if len(sys.argv) > 1:
        input_message += sys.argv[1]

    main(input_message)
