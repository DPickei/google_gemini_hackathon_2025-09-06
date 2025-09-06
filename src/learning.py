"""
Learning module for generating quiz questions from shell commands
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from src import gemini_client

logger = logging.getLogger(__name__)

class LearningManager:
    """Manages quiz question generation and storage from shell commands"""
    
    def __init__(self, storage_file: Optional[str] = None):
        self.storage_file = Path(storage_file or Path.home() / ".gemini_learning_questions.json")
        self.data = self._load_data()
        self.gemini = gemini_client.GeminiClient()
    
    def _load_data(self) -> Dict:
        """Load existing quiz questions"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            return {"questions": [], "stats": {}}
        except Exception as e:
            logger.error(f"Error loading learning data: {e}")
            return {"questions": [], "stats": {}}
    
    def _save_data(self):
        """Save quiz questions to file"""
        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving learning data: {e}")
    
    def generate_question(self, command: str) -> Optional[Dict]:
        """Generate a quiz question from a shell command using Gemini"""
        try:
            prompt = self._create_question_prompt(command)
            
            # Get response from Gemini using the existing CLI interface
            response = self._call_gemini_for_question(prompt)
            if not response:
                return None
            
            # Parse the response to extract question and options
            question_data = self._parse_question_response(response, command)
            return question_data
            
        except Exception as e:
            logger.error(f"Error generating question: {e}")
            return None
    
    def _call_gemini_for_question(self, prompt: str) -> Optional[str]:
        """Call Gemini CLI to generate question content"""
        import subprocess
        import os
        
        try:
            # Call Gemini CLI directly for question generation
            result = subprocess.run(
                ["gemini", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=60,  # Longer timeout for question generation
                env=dict(os.environ)
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Gemini CLI error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Gemini CLI request timed out")
            return None
        except Exception as e:
            logger.error(f"Error calling Gemini CLI: {e}")
            return None
    
    def _create_question_prompt(self, command: str) -> str:
        """Create a prompt for generating a quiz question"""
        return f"""Create a Duolingo-style quiz question where the answer is this shell command: {command}

Generate a question that tests understanding of what this command does or when to use it.

Format your response as JSON with these fields:
- "question": The quiz question (clear and educational)
- "correct_answer": The shell command (exactly: {command})
- "wrong_options": Array of 3 plausible but incorrect commands
- "explanation": Brief explanation of what the correct command does

Example format:
{{
  "question": "How would you find all files named 'main' in the current directory and subdirectories?",
  "correct_answer": "find . -name '*main*'",
  "wrong_options": [
    "grep -r main .",
    "ls -la *main*",
    "locate main"
  ],
  "explanation": "The find command with -name flag searches for files by name pattern recursively"
}}

Command to create question for: {command}
"""
    
    def _parse_question_response(self, response: str, original_command: str) -> Optional[Dict]:
        """Parse Gemini response to extract question data"""
        try:
            # Try to find JSON in the response
            response = response.strip()
            
            # Look for JSON block
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                question_data = json.loads(json_str)
                
                # Validate required fields
                required_fields = ["question", "correct_answer", "wrong_options", "explanation"]
                if all(field in question_data for field in required_fields):
                    # Ensure correct answer matches original command
                    question_data["correct_answer"] = original_command
                    return question_data
            
            return None
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing question response: {e}")
            return None
    
    def store_question(self, command: str) -> bool:
        """Generate and store a quiz question for a command"""
        try:
            # Check if we already have a question for this command
            existing_questions = [q for q in self.data["questions"] if q["correct_answer"] == command]
            if existing_questions:
                logger.info(f"Question already exists for command: {command}")
                return True
            
            # Generate new question
            question_data = self.generate_question(command)
            if not question_data:
                logger.error(f"Failed to generate question for command: {command}")
                return False
            
            # Add metadata
            question_data.update({
                "id": len(self.data["questions"]) + 1,
                "created_at": datetime.now().isoformat(),
                "times_asked": 0,
                "times_correct": 0
            })
            
            # Store the question
            self.data["questions"].append(question_data)
            self._update_stats()
            self._save_data()
            
            logger.info(f"Stored question for command: {command}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing question: {e}")
            return False
    
    def _update_stats(self):
        """Update learning statistics"""
        questions = self.data["questions"]
        
        self.data["stats"] = {
            "total_questions": len(questions),
            "total_attempts": sum(q.get("times_asked", 0) for q in questions),
            "total_correct": sum(q.get("times_correct", 0) for q in questions),
            "accuracy_rate": (
                sum(q.get("times_correct", 0) for q in questions) / max(sum(q.get("times_asked", 0) for q in questions), 1)
            ),
            "last_updated": datetime.now().isoformat()
        }
    
    def get_all_questions(self) -> List[Dict]:
        """Get all stored questions"""
        return self.data.get("questions", [])
    
    def get_stats(self) -> Dict:
        """Get learning statistics"""
        return self.data.get("stats", {})
    
    def update_question_stats(self, question_id: int, was_correct: bool):
        """Update statistics for a specific question"""
        try:
            questions = self.data.get("questions", [])
            for question in questions:
                if question.get("id") == question_id:
                    question["times_asked"] = question.get("times_asked", 0) + 1
                    if was_correct:
                        question["times_correct"] = question.get("times_correct", 0) + 1
                    break
            
            self._update_stats()
            self._save_data()
            
        except Exception as e:
            logger.error(f"Error updating question stats: {e}")
