"""
Command completion logger for tracking patterns and learning
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

class CommandLogger:
    """Tracks command completions and provides usage analytics"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = Path(log_file or Path.home() / ".gemini_command_helper.json")
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load existing log data"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            return {"completions": [], "stats": {}}
        except Exception as e:
            logger.error(f"Error loading log data: {e}")
            return {"completions": [], "stats": {}}
    
    def _save_data(self):
        """Save log data to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving log data: {e}")
    
    def log_completion(self, original_command: str, completed_command: str):
        """Log a command completion event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "original": original_command,
            "completed": completed_command,
            "prefix": original_command.split()[0] if original_command.split() else ""
        }
        
        self.data["completions"].append(entry)
        self._update_stats()
        self._save_data()
        
        logger.info(f"Logged completion: '{original_command}' → '{completed_command}'")
    
    def _update_stats(self):
        """Update usage statistics"""
        completions = self.data["completions"]
        
        # Count prefixes (e.g., 'pnpm', 'git', 'docker')
        prefix_counts = Counter(entry["prefix"] for entry in completions)
        
        # Count full original commands
        original_counts = Counter(entry["original"] for entry in completions)
        
        # Count completions
        completion_counts = Counter(entry["completed"] for entry in completions)
        
        self.data["stats"] = {
            "total_completions": len(completions),
            "most_common_prefixes": dict(prefix_counts.most_common(10)),
            "most_forgotten_commands": dict(original_counts.most_common(10)),
            "most_common_completions": dict(completion_counts.most_common(10)),
            "last_updated": datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return self.data.get("stats", {})
    
    def get_recent_completions(self, limit: int = 10) -> List[Dict]:
        """Get recent completions"""
        completions = self.data.get("completions", [])
        return completions[-limit:] if completions else []
    
    def suggest_completion(self, partial_command: str) -> Optional[str]:
        """Suggest completion based on historical data"""
        completions = self.data.get("completions", [])
        
        # Find historical completions for this partial command
        matches = [
            entry["completed"] 
            for entry in completions 
            if entry["original"] == partial_command
        ]
        
        if matches:
            # Return the most common historical completion
            return Counter(matches).most_common(1)[0][0]
        
        return None
