import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog

class SmartPairs:
    menudefs = [
        ('options', [
            ('AmpXD Override', '<<toggle-ampxd-mode>>'),
        ])
    ]

    def __init__(self, editwin):
        self.editwin = editwin
        self.text = editwin.text
        self.active = False 
        
        self.SECRET_PASSWORD = "amphibiar"
        
        self.history = []
        self.history_index = -1
        self.current_working_line = ""

        self.pairs = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}
        
        self.text.bind('<<toggle-ampxd-mode>>', self.toggle_mode)
        self.text.bind("<KeyPress-Up>", self.history_up)
        self.text.bind("<KeyPress-Down>", self.history_down)
        
        for opening_char in self.pairs.keys():
            self.text.bind(f"<Key-{opening_char}>", self.handle_keypress)

    def toggle_mode(self, event=None):
        if not self.active:
            user_input = simpledialog.askstring(
                "Access Required", 
                "Enter Admin Password to enable AmpXD Override:", 
                show='*'
            )
            
            if user_input == self.SECRET_PASSWORD:
                self.active = True
                messagebox.showinfo("AmpXD Override", " Heyyy access granted! Mode is now ENABLED [✓]. Code works.")
            else:
                messagebox.showerror("Access Denied", "Incorrect password. Wrong user. Please run as Ghost. Mode remains disabled.")
        else:
            self.active = False
            messagebox.showinfo("AmpXD Override", "AmpXD Mode is now DISABLED [✗]")
            
        return "break"

    def handle_keypress(self, event):
        if not self.active:
            return None 
            
        opening = event.char
        closing = self.pairs.get(opening)
        
        if closing:
            self.text.insert("insert", opening + closing)
            self.text.mark_set("insert", "insert-1c")
            return "break"

    def get_current_line_text(self):
        return self.text.get("insert linestart", "insert lineend")

    def history_up(self, event):
        if not self.active:
            return None

        all_lines = self.text.get("1.0", "end-1c").split("\n")
        self.history = [line.strip() for line in all_lines if line.strip()]
        
        if not self.history:
            return "break"

        if self.history_index == -1:
            self.current_working_line = self.get_current_line_text()
            self.history_index = len(self.history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
            
        self.text.delete("insert linestart", "insert lineend")
        self.text.insert("insert linestart", self.history[self.history_index])
        return "break"

    def history_down(self, event):
        if not self.active or self.history_index == -1:
            return None

        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.text.delete("insert linestart", "insert lineend")
            self.text.insert("insert linestart", self.history[self.history_index])
        else:
            self.history_index = -1
            self.text.delete("insert linestart", "insert lineend")
            self.text.insert("insert linestart", self.current_working_line)
            
        return "break"
