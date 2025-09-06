#!/usr/bin/env python3
"""
Interactive quiz runner for practicing shell command questions
"""

import random
import sys
from typing import List, Dict
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from src import learning

console = Console()

class QuizRunner:
    """Interactive quiz runner"""
    
    def __init__(self):
        self.learning_manager = learning.LearningManager()
        self.questions = self.learning_manager.get_all_questions()
        self.session_stats = {"correct": 0, "total": 0}
    
    def run_quiz(self, num_questions: int = None):
        """Run an interactive quiz session"""
        if not self.questions:
            console.print("[yellow]📝 No quiz questions found![/yellow]")
            console.print("[dim]Use './l <command>' to create questions first[/dim]")
            return
        
        console.print(Panel.fit(
            "[bold blue]🧠 Shell Command Quiz[/bold blue]\n"
            f"Available questions: {len(self.questions)}\n"
            "[dim]Choose the correct command for each question[/dim]",
            border_style="blue"
        ))
        
        # Determine number of questions to ask
        if num_questions is None:
            if len(self.questions) <= 5:
                questions_to_ask = self.questions.copy()
            else:
                num_questions = min(10, len(self.questions))
                console.print(f"[dim]Running quiz with {num_questions} questions[/dim]\n")
                questions_to_ask = random.sample(self.questions, num_questions)
        else:
            num_questions = min(num_questions, len(self.questions))
            questions_to_ask = random.sample(self.questions, num_questions)
        
        # Shuffle the questions
        random.shuffle(questions_to_ask)
        
        # Run the quiz
        for i, question in enumerate(questions_to_ask, 1):
            console.print(f"\n[bold]Question {i}/{len(questions_to_ask)}[/bold]")
            self._ask_question(question)
        
        # Show final results
        self._show_results()
    
    def _ask_question(self, question: Dict):
        """Ask a single quiz question"""
        # Prepare options
        options = question["wrong_options"].copy()
        options.append(question["correct_answer"])
        random.shuffle(options)
        
        # Find correct answer index (after shuffle)
        correct_index = options.index(question["correct_answer"]) + 1
        
        # Display question
        console.print(f"\n[yellow]{question['question']}[/yellow]")
        console.print()
        
        # Display options
        for i, option in enumerate(options, 1):
            console.print(f"  [bold]{i}.[/bold] [cyan]{option}[/cyan]")
        
        # Get user answer
        while True:
            try:
                answer = Prompt.ask(
                    "\nYour answer",
                    choices=[str(i) for i in range(1, len(options) + 1)],
                    show_choices=False
                )
                answer_index = int(answer)
                break
            except (ValueError, KeyboardInterrupt):
                console.print("[red]Please enter a valid option number[/red]")
        
        # Check answer
        self.session_stats["total"] += 1
        is_correct = answer_index == correct_index
        
        if is_correct:
            self.session_stats["correct"] += 1
            console.print(f"[green]✅ Correct![/green]")
        else:
            console.print(f"[red]❌ Incorrect![/red]")
            console.print(f"[dim]Correct answer: {question['correct_answer']}[/dim]")
        
        # Show explanation
        console.print(f"[dim]💡 {question['explanation']}[/dim]")
        
        # Update question statistics
        self.learning_manager.update_question_stats(question["id"], is_correct)
    
    def _show_results(self):
        """Display final quiz results"""
        correct = self.session_stats["correct"]
        total = self.session_stats["total"]
        percentage = (correct / total) * 100 if total > 0 else 0
        
        console.print("\n" + "="*50)
        console.print(Panel.fit(
            f"[bold]Quiz Complete![/bold]\n\n"
            f"Correct answers: [green]{correct}[/green] / [blue]{total}[/blue]\n"
            f"Accuracy: [bold]{percentage:.1f}%[/bold]\n\n"
            f"{'🎉 Excellent!' if percentage >= 80 else '📚 Keep practicing!' if percentage >= 60 else '💪 Try again!'}",
            border_style="green" if percentage >= 80 else "yellow" if percentage >= 60 else "red"
        ))
    
    def show_stats(self):
        """Display learning statistics"""
        stats = self.learning_manager.get_stats()
        questions = self.learning_manager.get_all_questions()
        
        if not questions:
            console.print("[yellow]📊 No learning data yet![/yellow]")
            console.print("[dim]Use './l <command>' to create questions first[/dim]")
            return
        
        console.print(Panel.fit(
            "[bold blue]📊 Learning Statistics[/bold blue]",
            border_style="blue"
        ))
        
        # Overall stats table
        table = Table(title="Overall Progress")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Questions", str(stats.get("total_questions", 0)))
        table.add_row("Total Attempts", str(stats.get("total_attempts", 0)))
        table.add_row("Correct Answers", str(stats.get("total_correct", 0)))
        table.add_row("Accuracy Rate", f"{stats.get('accuracy_rate', 0):.1%}")
        
        console.print(table)
        
        # Questions difficulty table
        if questions:
            console.print("\n")
            difficulty_table = Table(title="Question Difficulty")
            difficulty_table.add_column("Command", style="yellow", max_width=40)
            difficulty_table.add_column("Attempts", style="blue")
            difficulty_table.add_column("Correct", style="green")
            difficulty_table.add_column("Accuracy", style="cyan")
            
            for q in sorted(questions, key=lambda x: x.get("times_asked", 0), reverse=True)[:10]:
                attempts = q.get("times_asked", 0)
                correct = q.get("times_correct", 0)
                accuracy = (correct / attempts) if attempts > 0 else 0
                
                difficulty_table.add_row(
                    q["correct_answer"],
                    str(attempts),
                    str(correct),
                    f"{accuracy:.1%}" if attempts > 0 else "N/A"
                )
            
            console.print(difficulty_table)

def main():
    """Main entry point for quiz"""
    quiz_runner = QuizRunner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "stats":
            quiz_runner.show_stats()
            return 0
        elif command.isdigit():
            num_questions = int(command)
            quiz_runner.run_quiz(num_questions)
            return 0
    
    # Interactive mode
    while True:
        console.print("\n[bold blue]🧠 Shell Command Quiz[/bold blue]")
        console.print("1. Start Quiz")
        console.print("2. View Statistics") 
        console.print("3. Exit")
        
        choice = Prompt.ask(
            "\nWhat would you like to do?",
            choices=["1", "2", "3"],
            default="1"
        )
        
        if choice == "1":
            quiz_runner.run_quiz()
        elif choice == "2":
            quiz_runner.show_stats()
        elif choice == "3":
            console.print("[dim]Happy learning! 📚[/dim]")
            break

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n[dim]Goodbye! 👋[/dim]")
        sys.exit(0)
