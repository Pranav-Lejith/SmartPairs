class SmartPairs:
    
    menudefs = []

    def __init__(self, editwin):
        self.editwin = editwin
        self.text = editwin.text
        
        self.pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
            '"': '"',
            "'": "'"
        }
        
        
        for opening_char in self.pairs.keys():
            self.text.bind(f"<Key-{opening_char}>", self.handle_keypress)

    def handle_keypress(self, event):
        opening = event.char
        closing = self.pairs.get(opening)
        
        if closing:
            self.text.insert("insert", opening + closing)
            self.text.mark_set("insert", "insert-1c")
            return "break"
