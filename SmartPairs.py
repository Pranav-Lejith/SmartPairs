class SmartPairs:
    # Setup menu configuration mapping for IDLE's extension engine
    menudefs = []

    def __init__(self, editwin):
        self.editwin = editwin
        self.text = editwin.text
        
        # Define character mapping rules
        self.pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
            '"': '"',
            "'": "'"
        }
        
        # Bind the key press events to our custom logic
        for opening_char in self.pairs.keys():
            self.text.bind(f"<Key-{opening_char}>", self.handle_keypress)

    def handle_keypress(self, event):
        opening = event.char
        closing = self.pairs.get(opening)
        
        if closing:
            # Insert the pair of brackets/quotes at the current index
            self.text.insert("insert", opening + closing)
            # Move the text cursor back by 1 character to step inside the pair
            self.text.mark_set("insert", "insert-1c")
            # Break the event chain so IDLE doesn't double-insert the original character
            return "break"
