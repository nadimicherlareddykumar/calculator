import tkinter as tk
from tkinter import ttk, font, Menu
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator Pro")
        self.root.geometry("380x620")
        self.root.resizable(False, False)
        self.root.config(bg="#1a1a2e")
        
        # Variable to store the expression
        self.expression = ""
        self.result_shown = False
        self.history = []
        self.memory = 0
        
        # Add window icon styling
        try:
            self.root.iconbitmap('calculator.ico')
        except:
            pass
        
        # Create UI
        self.create_menu()
        self.create_widgets()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        
        # Add smooth animations
        self.animate_startup()
        
    def create_menu(self):
        """Create menu bar with additional options"""
        menubar = Menu(self.root, bg="#16213e", fg="#ffffff", activebackground="#4ecca3")
        self.root.config(menu=menubar)
        
        # Edit menu
        edit_menu = Menu(menubar, tearoff=0, bg="#16213e", fg="#ffffff", activebackground="#4ecca3")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy Result (Ctrl+C)", command=self.copy_result)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear History", command=self.clear_history)
        
        # View menu
        view_menu = Menu(menubar, tearoff=0, bg="#16213e", fg="#ffffff", activebackground="#4ecca3")
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="History", command=self.show_history)
        
        # Memory menu
        memory_menu = Menu(menubar, tearoff=0, bg="#16213e", fg="#ffffff", activebackground="#4ecca3")
        menubar.add_cascade(label="Memory", menu=memory_menu)
        memory_menu.add_command(label="Memory Clear (MC)", command=lambda: self.memory_operation('MC'))
        memory_menu.add_command(label="Memory Recall (MR)", command=lambda: self.memory_operation('MR'))
        memory_menu.add_command(label="Memory Add (M+)", command=lambda: self.memory_operation('M+'))
        memory_menu.add_command(label="Memory Subtract (M-)", command=lambda: self.memory_operation('M-'))
    
    def animate_startup(self):
        """Smooth startup animation"""
        self.root.attributes('-alpha', 0.0)
        self.fade_in()
    
    def fade_in(self, alpha=0.0):
        """Fade in animation"""
        alpha += 0.1
        if alpha <= 1.0:
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self.fade_in(alpha))
        else:
            self.root.attributes('-alpha', 1.0)
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Display frame with gradient effect
        display_frame = tk.Frame(main_frame, bg="#16213e", bd=0, relief=tk.FLAT)
        display_frame.pack(fill=tk.BOTH, padx=5, pady=(5, 15))
        
        # Memory indicator
        self.memory_indicator = tk.Label(
            display_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="#16213e",
            fg="#4ecca3",
            anchor="w",
            padx=20,
            pady=2
        )
        self.memory_indicator.pack(fill=tk.BOTH)
        
        # Secondary display (shows previous expression)
        self.secondary_display = tk.Label(
            display_frame,
            text="",
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="#94a3b8",
            anchor="e",
            padx=20,
            pady=5
        )
        self.secondary_display.pack(fill=tk.BOTH)
        
        # Main display
        self.display = tk.Label(
            display_frame,
            text="0",
            font=("Segoe UI", 36, "bold"),
            bg="#16213e",
            fg="#ffffff",
            anchor="e",
            padx=20,
            pady=15
        )
        self.display.pack(fill=tk.BOTH)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#1a1a2e")
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Define buttons with improved layout
        buttons = [
            ['AC', '⌫', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '='],
            ['√', 'x²', 'MR', 'MC']
        ]
        
        # Modern color scheme
        colors = {
            'number': {'bg': '#2d3250', 'fg': '#ffffff', 'hover': '#3d4260'},
            'operator': {'bg': '#f05454', 'fg': '#ffffff', 'hover': '#ff6b6b'},
            'special': {'bg': '#424769', 'fg': '#ffffff', 'hover': '#525b7f'},
            'equals': {'bg': '#4ecca3', 'fg': '#ffffff', 'hover': '#5fddb3'},
            'memory': {'bg': '#8b5cf6', 'fg': '#ffffff', 'hover': '#9d71f7'},
            'scientific': {'bg': '#f59e0b', 'fg': '#ffffff', 'hover': '#fbbf24'}
        }
        
        # Create buttons with hover effects
        self.buttons = {}
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                # Determine button style
                if button_text == '=':
                    style = colors['equals']
                elif button_text in ['AC', '⌫', '%', '±']:
                    style = colors['special']
                elif button_text in ['÷', '×', '-', '+']:
                    style = colors['operator']
                elif button_text in ['MR', 'MC']:
                    style = colors['memory']
                elif button_text in ['√', 'x²']:
                    style = colors['scientific']
                else:
                    style = colors['number']
                
                btn = tk.Button(
                    button_frame,
                    text=button_text,
                    font=("Segoe UI", 18, "bold"),
                    bg=style['bg'],
                    fg=style['fg'],
                    activebackground=style['hover'],
                    activeforeground="#ffffff",
                    bd=0,
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=lambda x=button_text: self.on_button_click(x)
                )
                
                # Grid placement
                btn.grid(row=i, column=j, sticky="nsew", padx=4, pady=4)
                
                # Store button reference for hover effects
                self.buttons[button_text] = {'btn': btn, 'style': style}
                
                # Bind hover events
                btn.bind('<Enter>', lambda e, b=button_text: self.on_hover(b, True))
                btn.bind('<Leave>', lambda e, b=button_text: self.on_hover(b, False))
        
        # Configure grid weights for responsive buttons
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1, minsize=60)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1, minsize=70)
    
    def on_hover(self, button_text, is_entering):
        """Handle button hover effects"""
        if button_text in self.buttons:
            btn_info = self.buttons[button_text]
            if is_entering:
                btn_info['btn'].config(bg=btn_info['style']['hover'])
            else:
                btn_info['btn'].config(bg=btn_info['style']['bg'])
    
    def update_display(self, value=None):
        """Update the calculator display"""
        if value is None:
            display_text = self.expression if self.expression else "0"
        else:
            display_text = value
        
        # Limit display length for better UX
        if len(str(display_text)) > 15:
            self.display.config(font=("Segoe UI", 24, "bold"))
        else:
            self.display.config(font=("Segoe UI", 36, "bold"))
        
        self.display.config(text=display_text)
    
    def on_button_click(self, char):
        if char == 'AC':
            # Clear all
            self.expression = ""
            self.secondary_display.config(text="")
            self.update_display("0")
            self.result_shown = False
        
        elif char == 'MC':
            # Memory Clear
            self.memory_operation('MC')
        
        elif char == 'MR':
            # Memory Recall
            self.memory_operation('MR')
        
        elif char == '√':  # Square root
            if self.expression:
                try:
                    value = float(eval(self.expression.replace('×', '*').replace('÷', '/')))
                    if value < 0:
                        self.update_display("Error: Negative root")
                        return
                    result = math.sqrt(value)
                    self.secondary_display.config(text=f"√({self.expression})")
                    self.expression = str(result if not result.is_integer() else int(result))
                    self.update_display()
                    self.result_shown = True
                except:
                    self.update_display("Error")
        
        elif char == 'x²':  # Square
            if self.expression:
                try:
                    value = float(eval(self.expression.replace('×', '*').replace('÷', '/')))
                    result = value ** 2
                    self.secondary_display.config(text=f"({self.expression})²")
                    self.expression = str(result if not result.is_integer() else int(result))
                    self.update_display()
                    self.result_shown = True
                except:
                    self.update_display("Error")
        
        elif char == '⌫':  # Backspace
            if self.result_shown:
                self.expression = ""
                self.result_shown = False
            else:
                self.expression = self.expression[:-1]
            self.update_display()
        
        elif char == '%':
            # Percentage
            if self.expression:
                try:
                    value = float(self.expression)
                    result = value / 100
                    self.expression = str(result)
                    self.update_display()
                except:
                    pass
        
        elif char == '±':  # Plus/minus toggle
            if self.expression and self.expression != "0":
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
                self.update_display()
        
        elif char == '=':
            # Calculate result
            if not self.expression:
                return
            
            try:
                # Store original expression for secondary display
                original_expr = self.expression
                
                # Replace symbols with Python operators
                calc_expression = self.expression.replace('×', '*').replace('÷', '/')
                result = eval(calc_expression)
                
                # Format result
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 10)
                        # Remove trailing zeros
                        result = float(str(result).rstrip('0').rstrip('.'))
                
                # Update displays
                self.secondary_display.config(text=f"{original_expr} =")
                self.expression = str(result)
                self.update_display()
                self.result_shown = True
                
                # Add to history
                self.add_to_history(original_expr, result)
            
            except ZeroDivisionError:
                self.secondary_display.config(text="Error")
                self.update_display("Cannot divide by zero")
                self.expression = ""
                self.result_shown = True
            
            except Exception:
                self.secondary_display.config(text="Error")
                self.update_display("Invalid expression")
                self.expression = ""
                self.result_shown = True
        
        else:
            # Add character to expression
            if self.result_shown:
                # Start new calculation after result
                if char in ['÷', '×', '-', '+']:
                    # Continue with result
                    self.result_shown = False
                else:
                    # Start fresh
                    self.expression = ""
                    self.secondary_display.config(text="")
                    self.result_shown = False
            
            # Prevent multiple operators in a row
            if char in ['÷', '×', '-', '+'] and self.expression and self.expression[-1] in ['÷', '×', '-', '+']:
                self.expression = self.expression[:-1]
            
            # Prevent multiple decimal points in the same number
            if char == '.':
                # Check if current number already has a decimal
                parts = self.expression.split()
                if parts and '.' in parts[-1]:
                    return
            
            self.expression += char
            self.update_display()
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        # Number keys
        if key in '0123456789.':
            self.on_button_click(key)
        
        # Operators
        elif key == '+':
            self.on_button_click('+')
        elif key == '-':
            self.on_button_click('-')
        elif key in ['*', 'x', 'X']:
            self.on_button_click('×')
        elif key == '/':
            self.on_button_click('÷')
        elif key == '%':
            self.on_button_click('%')
        
        # Actions
        elif event.keysym == 'Return' or event.keysym == 'equal':
            self.on_button_click('=')
        elif event.keysym == 'BackSpace':
            self.on_button_click('⌫')
        elif event.keysym == 'Escape' or key.lower() == 'c':
            self.on_button_click('AC')
    
    def memory_operation(self, operation):
        """Handle memory operations"""
        try:
            current_value = float(self.expression) if self.expression else 0
        except:
            current_value = 0
        
        if operation == 'MC':
            self.memory = 0
            self.memory_indicator.config(text="")
        elif operation == 'MR':
            self.expression = str(self.memory if not float(self.memory).is_integer() else int(self.memory))
            self.update_display()
        elif operation == 'M+':
            self.memory += current_value
            self.memory_indicator.config(text=f"M: {self.memory}")
        elif operation == 'M-':
            self.memory -= current_value
            self.memory_indicator.config(text=f"M: {self.memory}")
    
    def add_to_history(self, expression, result):
        """Add calculation to history"""
        self.history.append(f"{expression} = {result}")
        if len(self.history) > 50:  # Keep last 50 calculations
            self.history.pop(0)
    
    def clear_history(self):
        """Clear calculation history"""
        self.history = []
    
    def show_history(self):
        """Show calculation history in a new window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("400x500")
        history_window.config(bg="#1a1a2e")
        history_window.resizable(False, False)
        
        # Title
        title_label = tk.Label(
            history_window,
            text="History",
            font=("Segoe UI", 18, "bold"),
            bg="#1a1a2e",
            fg="#ffffff",
            pady=10
        )
        title_label.pack()
        
        # Frame for history list
        frame = tk.Frame(history_window, bg="#16213e")
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame, bg="#424769")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for history
        history_list = tk.Listbox(
            frame,
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="#ffffff",
            selectbackground="#4ecca3",
            selectforeground="#ffffff",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        history_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_list.yview)
        
        # Populate history
        if self.history:
            for item in reversed(self.history):
                history_list.insert(tk.END, item)
        else:
            history_list.insert(tk.END, "No history yet")
        
        # Close button
        close_btn = tk.Button(
            history_window,
            text="Close",
            font=("Segoe UI", 12, "bold"),
            bg="#f05454",
            fg="#ffffff",
            activebackground="#ff6b6b",
            bd=0,
            cursor="hand2",
            command=history_window.destroy,
            pady=10
        )
        close_btn.pack(fill=tk.X, padx=15, pady=(0, 15))
    
    def copy_result(self):
        """Copy current result to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.expression if self.expression else "0")
            # Visual feedback
            original_text = self.secondary_display.cget("text")
            self.secondary_display.config(text="Copied to clipboard!")
            self.root.after(1000, lambda: self.secondary_display.config(text=original_text))
        except:
            pass

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
