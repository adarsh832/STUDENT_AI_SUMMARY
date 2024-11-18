import subprocess
import json
from typing import Optional, Dict, List
from file_handler import FileHandler
import os

class GenerationHandler:
    def __init__(self):
        """
        Initialize the generation handler with llama3.2 model
        """
        self.model = "llama3.2"
        self.context_history = []
        self.max_context_length = 5
        self.current_file_content = None  # Store current file content
        
    def generate_response(self, query: str, context: Optional[Dict] = None) -> str:
        """Generate a response for the given query using llama3.2"""
        try:
            # If there's a file loaded and the query isn't a file processing request
            if self.current_file_content and not query.startswith("Please analyze this document"):
                # Modify the query to include file context
                query = f"Based on the document content: {query}\nDocument content: {self.current_file_content[:2000]}"

            prompt = self._format_prompt(query)
            cmd = ["ollama", "run", "llama3.2", prompt]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                return self._format_response(result.stdout.strip())
            else:
                return f"Error generating response: {result.stderr}"

        except Exception as e:
            return f"Failed to generate response: {str(e)}"

    def _format_prompt(self, query: str) -> str:
        """Format the prompt with context history and system instructions"""
        prompt = (
            "<<SYS>>\n"
            "You are CodeBuddy, a friendly AI study assistant specialized in Computer Engineering. "
            "You're here to help students understand complex topics, debug code, and learn effectively. "
            "Follow these guidelines:\n"
            "1. Teaching style:\n"
            "   - Break down complex concepts into simple explanations\n"
            "   - Use relevant examples from computer engineering\n"
            "   - Provide code snippets when helpful\n"
            "   - Encourage learning by asking thought-provoking questions\n"
            "2. When analyzing documents:\n"
            "   - Focus on key technical concepts\n"
            "   - Explain difficult terms in simple language\n"
            "   - Connect topics to real-world applications\n"
            "   - Highlight important formulas and algorithms\n"
            "3. For programming questions:\n"
            "   - Explain the logic step by step\n"
            "   - Suggest best practices and optimizations\n"
            "   - Point out common pitfalls to avoid\n"
            "   - Include helpful comments in code examples\n"
            "4. Personality:\n"
            "   - Be encouraging and supportive\n"
            "   - Use casual, friendly language\n"
            "   - Add relevant emojis occasionally\n"
            "   - Share interesting facts about tech when relevant\n"
            "<</SYS>>\n\n"
        )

        if self.context_history:
            prompt += "Previous context:\n"
            for item in self.context_history:
                prompt += f"Human: {item['query']}\n"
                if item['context']:
                    prompt += f"Context: {json.dumps(item['context'])}\n"
            prompt += "\n"

        prompt += f"Human: {query}\n\nAssistant: "
        return prompt

    def _format_response(self, response: str) -> str:
        """Format the response for better readability"""
        # Remove any system or formatting artifacts
        response = response.replace("<<SYS>>", "").replace("<</SYS>>", "")
        lines = response.split('\n')
        cleaned_lines = [
            line.strip() for line in lines 
            if not line.strip().startswith(('Human:', 'Assistant:', 'System:'))
            and line.strip()
        ]
        return '\n'.join(cleaned_lines)

    def handle_specific_queries(self, query_type: str, query: str) -> str:
        """Handle specific types of queries"""
        prompts = {
            'code': (
                "Write code for this request. Include:\n"
                "1. Implementation\n"
                "2. Comments explaining the code\n"
                "3. Example usage\n"
            ),
            'explanation': (
                "Explain this concept. Include:\n"
                "1. Simple explanation\n"
                "2. Key points\n"
                "3. Examples if relevant\n"
            ),
            'general': "Provide a clear and helpful response to this query:\n"
        }

        prompt_prefix = prompts.get(query_type, prompts['general'])
        formatted_query = f"{prompt_prefix}{query}"
        return self.generate_response(formatted_query)

    def clear_context(self):
        """Clear the context history and file content"""
        self.context_history = []
        self.current_file_content = None
        print("Context and file content cleared!")

    def process_file(self, file_path: str) -> str:
        """Process a file and generate a response about its contents"""
        try:
            file_handler = FileHandler()
            self.current_file_content = file_handler.read_file(file_path)
            
            # Create a study-focused summary prompt
            prompt = (
                "Please analyze this computer engineering document and help me understand it better. Include:\n"
                "1. Main technical concepts covered\n"
                "2. Key algorithms or methods discussed\n"
                "3. Important formulas or principles\n"
                "4. Practical applications\n"
                "5. Prerequisites needed to understand this topic\n"
                "6. Study tips or areas to focus on\n\n"
                f"Document content:\n{self.current_file_content[:2000]}"
            )
            
            # Add file content to context
            self.context_history.append({
                "query": "Analyze this document",
                "context": {"file_content": self.current_file_content[:2000]}
            })
            
            return self.generate_response(prompt)
            
        except Exception as e:
            return f"Error processing file: {str(e)}"

if __name__ == "__main__":
    handler = GenerationHandler()
    print("Welcome to CodeBuddy - Your Computer Engineering Study Assistant! 🚀")
    print("\nI can help you with:")
    print("- Understanding technical concepts")
    print("- Analyzing your study materials")
    print("- Programming questions and debugging")
    print("- Computer engineering topics")
    print("\nCommands:")
    print("- 'file: <path>' to upload study materials (PDF/PPT)")
    print("- 'clear' to start fresh")
    print("- 'exit' to quit")
    print("\nFeel free to ask anything about computer engineering!")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                handler.clear_context()
                continue
            elif user_input.lower().startswith('file:'):
                file_path = user_input[5:].strip()
                print("\nProcessing file...")
                response = handler.process_file(file_path)
                print("\nAssistant:", response)
                print("\n(File loaded - you can now ask questions about its contents)")
            elif not user_input:
                continue
            else:
                print("\nAssistant:", end=" ")
                response = handler.generate_response(user_input)
                print(response)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")