def readTerminal(output_widget):
    """
    Reads the current text from a Tkinter ScrolledText terminal widget.

    Parameters:
        output_widget: The Tkinter ScrolledText widget displaying output.

    Returns:
        str: The content of the terminal/output widget.
    """
    # Make sure widget is readable
    output_widget.config(state="normal")
    content = output_widget.get(1.0, "end-1c")  # Read all text, remove trailing newline
    output_widget.config(state="disabled")
    return content
