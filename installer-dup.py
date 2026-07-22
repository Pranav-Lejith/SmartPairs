import os
import sys
import ctypes
import shutil

# This is the exact, working code you verified
EXTENSION_CODE = """import tkinter.messagebox as messagebox
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
                messagebox.showinfo("AmpXD Override", "Access Granted! Mode is now ENABLED [✓]")
            else:
                messagebox.showerror("Access Denied", "Incorrect password. Mode remains disabled.")
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

        all_lines = self.text.get("1.0", "end-1c").split("\\n")
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
"""

CONFIG_TEXT = "\n\n[SmartPairs]\nenable=1\n[SmartPairs_cfgBindings]\ntoggle-ampxd-mode=\n"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    # Automatically requests Admin rights if not already elevated
    if not is_admin():
        print("Requesting Administrator Permissions...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("===================================================")
    print("             AmpXD Override Auto-Installer         ")
    print("===================================================")
    
    try:
        import idlelib
        idlelib_path = os.path.dirname(idlelib.__file__)
        print(f"✓ Found target folder: {idlelib_path}")
    except ImportError:
        print("❌ Error: Could not locate IDLE path automatically.")
        input("\nPress Enter to exit...")
        return

    script_file_path = os.path.join(idlelib_path, "SmartPairs.py")
    config_file_path = os.path.join(idlelib_path, "config-extensions.def")

    # Write exact uncorrupted script
    try:
        with open(script_file_path, "w", encoding="utf-8") as f:
            f.write(EXTENSION_CODE)
        print("✓ SmartPairs.py created successfully with perfect code formatting.")
    except Exception as e:
        print(f"❌ Error: Failed to write file. {e}")
        input("\nPress Enter to exit...")
        return

    # Append configuration safely
    with open(config_file_path, "r", encoding="utf-8") as f:
        config_content = f.read()

    if "[SmartPairs]" in config_content:
        print("✓ Configurations are already active inside IDLE.")
    else:
        # Create backup just in case
        shutil.copyfile(config_file_path, config_file_path + ".bak")
        with open(config_file_path, "a", encoding="utf-8") as f:
            f.write(CONFIG_TEXT)
        print("✓ Registered configurations inside config-extensions.def (Backup created).")

    print("\n===================================================")
    print("Installation Complete! Please close and restart IDLE.")
    print("===================================================")
    input("\nPress Enter to finish...")

if __name__ == "__main__":
    main()
