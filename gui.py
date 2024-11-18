import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from index import GenerationHandler
import threading
import customtkinter as ctk
import time
from itertools import cycle
import asyncio
import datetime
import os

class LoadingDots(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dots = cycle([".", "..", "..."])
        self.is_animating = False
        
    def start(self):
        self.is_animating = True
        self.animate()
        
    def stop(self):
        self.is_animating = False
        self.configure(text="")
        
    def animate(self):
        if self.is_animating:
            self.configure(text=next(self.dots))
            self.after(500, self.animate)

class ProcessingOverlay(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            corner_radius=15,
            border_width=2,
            border_color="#7289DA"
        )
        
        # Loading animation
        self.loading_text = ctk.CTkLabel(
            self,
            text="Processing",
            font=("Helvetica", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.loading_text.pack(pady=(20, 10))
        
        self.loading_dots = LoadingDots(
            self,
            text="",
            font=("Helvetica", 32, "bold"),
            text_color="#7289DA"
        )
        self.loading_dots.pack(pady=10)
        
        # Progress bar with custom styling
        self.progress = ctk.CTkProgressBar(
            self,
            width=300,
            height=15,
            corner_radius=7,
            progress_color="#7289DA",
            border_width=1
        )
        self.progress.pack(pady=(10, 20))
        self.progress.set(0)
        
    def start(self):
        self.loading_dots.start()
        self.animate_progress()
        
    def stop(self):
        self.loading_dots.stop()
        self.progress.set(0)
        
    def animate_progress(self):
        if self.loading_dots.is_animating:
            current = self.progress.get()
            if current >= 1:
                self.progress.set(0)
            else:
                self.progress.set(current + 0.1)
            self.after(300, self.animate_progress)

class CodeBuddyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeBuddy - Engineering Assistant")
        self.root.geometry("1200x800")
        
        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position coordinates
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        
        # Set the position
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Prevent resizing below minimum size
        self.root.minsize(800, 600)
        
        # Set theme and colors
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Custom colors
        self.colors = {
            "bg_primary": "#1A1B26",      # Darker background
            "bg_secondary": "#24283B",    # Slightly lighter background
            "accent": "#7AA2F7",         # Brighter blue
            "text_primary": "#FFFFFF",    # Pure white
            "text_secondary": "#A9B1D6",  # Light blue-grey
            "success": "#9ECE6A",        # Soft green
            "error": "#F7768E",          # Soft red
            "warning": "#E0AF68",        # Soft orange
            "code_bg": "#1F2335",        # Dark blue for code blocks
            "separator": "#414868"        # Mid-tone for separators
        }
        
        self.handler = GenerationHandler()
        
        # Add a directory for saved notes
        self.notes_dir = "saved_notes"
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
            
        # Call setup_gui() to initialize the interface
        self.setup_gui()
        
    def save_chat(self):
        """Save the chat content as notes"""
        try:
            # Get all text from chat display
            self.chat_display.configure(state="normal")
            chat_content = self.chat_display.get("1.0", tk.END)
            self.chat_display.configure(state="disabled")
            
            # Create filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"notes_{timestamp}.txt"
            filepath = os.path.join(self.notes_dir, filename)
            
            # Format the notes
            formatted_notes = self.format_notes(chat_content)
            
            # Save to file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(formatted_notes)
            
            # Show success message with file location
            messagebox.showinfo(
                "Notes Saved",
                f"Notes have been saved successfully!\nLocation: {filepath}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to save notes: {str(e)}"
            )

    def format_notes(self, content: str) -> str:
        """Format the chat content as structured notes"""
        formatted = "╔══════════════════════════════════════════════════════════╗\n"
        formatted += "║                   CodeBuddy Study Notes                  ║\n"
        formatted += "╚══════════════════════════════════════════════════════════╝\n\n"
        
        formatted += f"📅 Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        formatted += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Process the content
        lines = content.split('\n')
        current_section = None
        code_block = False
        
        for line in lines:
            if not line.strip():
                continue
            
            # Handle timestamps and speakers
            if line.startswith('[') and ']' in line:
                timestamp = line[1:line.find(']')]
                speaker = line[line.find(']')+1:].strip()
                if speaker.startswith('You'):
                    formatted += f"\n🗣️ User Question ({timestamp}):\n"
                    formatted += "┄" * 40 + "\n"
                elif speaker.startswith('CodeBuddy'):
                    formatted += f"\n💡 Answer ({timestamp}):\n"
                    formatted += "┄" * 40 + "\n"
                continue
            
            # Handle code blocks
            if '```' in line:
                code_block = not code_block
                if code_block:
                    formatted += "\n📝 Code Example:\n"
                    formatted += "┌" + "─" * 40 + "┐\n"
                else:
                    formatted += "└" + "─" * 40 + "┘\n"
                continue
            
            # Format the line
            if code_block:
                formatted += f"│ {line.ljust(39)}│\n"
            else:
                # Handle lists
                if line.strip().startswith(('•', '-', '*')):
                    formatted += f"  • {line.strip()[1:].strip()}\n"
                elif line.strip().startswith(('1.', '2.', '3.')):
                    formatted += f"  {line.strip()}\n"
                else:
                    formatted += f"    {line.strip()}\n"
        
        # Add study tips section
        formatted += "\n╔══════════════════════════════════════════════════════════╗\n"
        formatted += "║                      Study Tips                           ║\n"
        formatted += "╚══════════════════════════════════════════════════════════╝\n\n"
        formatted += "📚 Review Strategies:\n"
        formatted += "  • Review these notes within 24 hours\n"
        formatted += "  • Create flashcards for key concepts\n"
        formatted += "  • Practice implementing the code examples\n"
        formatted += "  • Connect concepts to real-world applications\n\n"
        formatted += "🎯 Focus Areas:\n"
        formatted += "  • Highlight unclear topics for follow-up\n"
        formatted += "  • Practice with similar problems\n"
        formatted += "  • Discuss concepts with peers\n"
        formatted += "  • Apply concepts in projects\n"
        
        return formatted
        
    def setup_gui(self):
        # Configure root background
        self.root.configure(bg=self.colors["bg_primary"])
        
        # Main container with gradient effect
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["bg_secondary"],
            corner_radius=15
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header frame with logo and title
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent",
            height=80
        )
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Logo (you can replace this with an actual logo image)
        logo_label = ctk.CTkLabel(
            header_frame,
            text="🤖",
            font=("Helvetica", 40),
            text_color=self.colors["accent"]
        )
        logo_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Title with subtitle
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side=tk.LEFT, padx=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="CodeBuddy",
            font=("Helvetica", 36, "bold"),
            text_color=self.colors["text_primary"]
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Your Computer Engineering Study Assistant",
            font=("Helvetica", 14),
            text_color=self.colors["text_secondary"]
        )
        subtitle_label.pack(anchor="w")
        
        # Chat display with custom styling
        self.chat_display = ctk.CTkTextbox(
            main_frame,
            font=("Cascadia Code", 14),  # Using a monospace font
            wrap="word",
            height=450,
            corner_radius=10,
            border_width=1,
            border_color=self.colors["accent"],
            fg_color=self.colors["bg_primary"],
            text_color=self.colors["text_primary"]
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Update the welcome message to be more concise and visually appealing
        welcome_msg = (
            "╔══════════════════════════════════════════════════╗\n"
            "║            Welcome to CodeBuddy! 🚀              ║\n"
            "╚══════════════════════════════════════════════════╝\n\n"
            "I'm your Computer Engineering Study Assistant.\n\n"
            "Here's how I can help you:\n\n"
            "📚  Learn Complex Concepts\n"
            "💻  Debug & Improve Code\n"
            "📑  Analyze Study Materials\n"
            "🔧  Solve Engineering Problems\n\n"
            "Just type your question or upload a file to get started!\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        
        self.chat_display.insert("1.0", welcome_msg)
        self.chat_display.configure(state="disabled")
        
        # Input area with modern design
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.user_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here...",
            height=50,
            font=("Helvetica", 14),
            corner_radius=25,  # Rounded corners
            border_width=2
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', lambda e: self.send_message())
        
        # Button frame with improved layout
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Store button references as class attributes
        self.send_button = ctk.CTkButton(
            button_frame,
            text="➤ Send Message",
            width=140,
            height=45,
            font=("Helvetica", 14),
            corner_radius=22,
            fg_color=self.colors["accent"],
            hover_color=self._adjust_color(self.colors["accent"], -20),
            command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        self.upload_button = ctk.CTkButton(
            button_frame,
            text="📁 Upload File",
            width=140,
            height=45,
            font=("Helvetica", 14),
            corner_radius=22,
            fg_color=self.colors["warning"],
            hover_color=self._adjust_color(self.colors["warning"], -20),
            command=self.upload_file
        )
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ctk.CTkButton(
            button_frame,
            text="💾 Save Notes",
            width=140,
            height=45,
            font=("Helvetica", 14),
            corner_radius=22,
            fg_color=self.colors["success"],
            hover_color=self._adjust_color(self.colors["success"], -20),
            command=self.save_chat
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear Chat",
            width=140,
            height=45,
            font=("Helvetica", 14),
            corner_radius=22,
            fg_color=self.colors["error"],
            hover_color=self._adjust_color(self.colors["error"], -20),
            command=self.clear_chat
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar with modern design
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ctk.CTkLabel(
            main_frame,
            textvariable=self.status_var,
            height=35,
            font=("Helvetica", 12),
            fg_color=self.colors["bg_primary"],
            corner_radius=8,
            text_color=self.colors["text_secondary"]
        )
        self.status_bar.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        # Create processing overlay
        self.overlay = ProcessingOverlay(
            self.root,
            fg_color="#1E1E1E",
            corner_radius=10
        )
        
        # Add typing indicator
        self.typing_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Helvetica", 12),
            text_color="#888888"
        )
        self.typing_label.pack(fill=tk.X, padx=10, pady=(0, 5))
        
    def show_processing(self, message="Processing"):
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")
        self.overlay.loading_text.configure(text=message)
        self.overlay.start()
        self.root.update()
        
    def hide_processing(self):
        self.overlay.stop()
        self.overlay.place_forget()
        self.root.update()
        
    def show_typing(self):
        self.typing_label.configure(text="CodeBuddy is typing...")
        
    def hide_typing(self):
        self.typing_label.configure(text="")
        
    def send_message(self):
        message = self.user_input.get().strip()
        if not message:
            return
            
        self.user_input.delete(0, tk.END)
        self.append_message("You", message)
        
        self.status_var.set("Thinking...")
        self.send_button.configure(state="disabled")
        self.show_typing()
        
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def process_message(self, message):
        try:
            if message.lower() == 'clear':
                self.clear_chat()
                return
                
            # Simulate some processing time for better UX
            time.sleep(0.5)
            response = self.handler.generate_response(message)
            
            # Simulate typing effect
            self.root.after(0, self.show_typing)
            time.sleep(0.5)
            
            self.root.after(0, self.append_message, "CodeBuddy", response)
            self.root.after(0, self.hide_typing)
            self.root.after(0, self.status_var.set, "Ready")
            self.root.after(0, self.send_button.configure, {"state": "normal"})
            
        except Exception as e:
            self.root.after(0, self.append_message, "System", f"❌ Error: {str(e)}")
            self.root.after(0, self.hide_typing)
            self.root.after(0, self.status_var.set, "Ready")
            self.root.after(0, self.send_button.configure, {"state": "normal"})
            
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Documents", "*.pdf;*.pptx;*.ppt"),
                ("PDF files", "*.pdf"),
                ("PowerPoint files", "*.pptx;*.ppt")
            ]
        )
        if file_path:
            self.show_processing("Processing File")
            self.upload_button.configure(state="disabled")
            threading.Thread(target=self.process_file, args=(file_path,), daemon=True).start()
            
    def process_file(self, file_path):
        try:
            # Simulate file processing stages
            stages = [
                "Reading file...",
                "Analyzing content...",
                "Generating summary...",
                "Preparing response..."
            ]
            
            for stage in stages:
                self.root.after(0, self.overlay.loading_text.configure, {"text": stage})
                time.sleep(1)  # Simulate processing time
                
            response = self.handler.process_file(file_path)
            self.root.after(0, self.append_message, "System", f"📄 File loaded: {file_path}")
            self.root.after(0, self.append_message, "CodeBuddy", response)
            
        except Exception as e:
            self.root.after(0, self.append_message, "System", f"❌ Error processing file: {str(e)}")
            
        finally:
            self.root.after(0, self.hide_processing)
            self.root.after(0, self.status_var.set, "Ready")
            self.root.after(0, self.upload_button.configure, {"state": "normal"})
            
    def append_message(self, sender, message):
        self.chat_display.configure(state="normal")
        
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Add separator with timestamp
        separator = f"\n{'─' * 20} {timestamp} {'─' * 20}\n\n"
        self.chat_display.insert("end", separator, "separator")
        
        if sender == "You":
            # User messages
            self.chat_display.insert("end", "You 👤\n", "user_header")
            self.chat_display.insert("end", f"{message}\n\n", "user_message")
            
        elif sender == "System":
            # System messages
            self.chat_display.insert("end", "🔧 System Note:\n", "system_header")
            self.chat_display.insert("end", f"{message}\n\n", "system_message")
            
        else:
            # CodeBuddy messages
            self.chat_display.insert("end", "CodeBuddy 🤖\n", "bot_header")
            
            # Format code blocks and lists
            lines = message.split('\n')
            formatted_message = []
            in_code_block = False
            
            for line in lines:
                if '```' in line:
                    in_code_block = not in_code_block
                    if in_code_block:
                        formatted_message.append("\n📝 Code Example:\n")
                        formatted_message.append("┌" + "─" * 60 + "┐")
                    else:
                        formatted_message.append("└" + "─" * 60 + "┘\n")
                    continue
                
                if in_code_block:
                    # Add padding and syntax highlighting for code
                    formatted_message.append(f"│ {line.ljust(59)}│")
                else:
                    # Format lists and regular text
                    if line.strip().startswith(('•', '-', '*')):
                        formatted_message.append(f"  • {line.strip()[1:].strip()}")
                    elif line.strip().startswith(('1.', '2.', '3.')):
                        formatted_message.append(f"  {line.strip()}")
                    else:
                        # Wrap long lines for better readability
                        words = line.split()
                        current_line = []
                        line_length = 0
                        
                        for word in words:
                            if line_length + len(word) + 1 > 60:
                                formatted_message.append("  " + " ".join(current_line))
                                current_line = [word]
                                line_length = len(word)
                            else:
                                current_line.append(word)
                                line_length += len(word) + 1
                        
                        if current_line:
                            formatted_message.append("  " + " ".join(current_line))
            
            self.chat_display.insert("end", f"{'\n'.join(formatted_message)}\n\n", "bot_message")
        
        # Configure text tags for different message types (without font configuration)
        self.chat_display.tag_config("separator", foreground=self.colors["separator"])
        self.chat_display.tag_config("user_header", foreground=self.colors["accent"])
        self.chat_display.tag_config("system_header", foreground=self.colors["warning"])
        self.chat_display.tag_config("bot_header", foreground=self.colors["success"])
        self.chat_display.tag_config("user_message", foreground=self.colors["text_primary"])
        self.chat_display.tag_config("system_message", foreground=self.colors["warning"])
        self.chat_display.tag_config("bot_message", foreground=self.colors["text_primary"])
        
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
        
    def clear_chat(self):
        self.handler.clear_context()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", tk.END)
        
        # Use the same welcome message format
        welcome_msg = (
            "╔══════════════════════════════════════════════════╗\n"
            "║            Chat Cleared Successfully! 🔄         ║\n"
            "╚═════════════════════════════════════════════════╝\n\n"
            "Ready for new questions!\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        
        self.chat_display.insert("end", welcome_msg)
        self.chat_display.configure(state="disabled")
        self.status_var.set("Ready")
        
    def _adjust_color(self, hex_color: str, amount: int) -> str:
        """Adjust hex color brightness"""
        rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
        
if __name__ == "__main__":
    root = ctk.CTk()
    app = CodeBuddyGUI(root)
    root.mainloop() 