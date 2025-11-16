#!/usr/bin/env python3
"""
Command-line interface for the AI-powered daily planning system.
"""
import json
from datetime import datetime, timedelta
from typing import Optional
from task_model import Task, Priority, EnergyLevel, TaskMode, Flexibility, TaskStatus
from llm_agent import LLMSchedulingAgent
from energy_scheduling import Chronotype


class SchedulerCLI:
    """Interactive CLI for the scheduling system"""
    
    def __init__(self):
        self.agent: Optional[LLMSchedulingAgent] = None
    
    def setup_agent(self):
        """Setup the scheduling agent with user preferences"""
        print("\n" + "="*60)
        print("AI-Powered Daily Planning System")
        print("="*60)
        print("\nWelcome! Let's set up your personalized scheduler.\n")
        
        # Get chronotype
        print("What's your chronotype (circadian rhythm)?")
        print("1. Early Bird (peak energy: morning)")
        print("2. Intermediate (peak energy: midday)")
        print("3. Night Owl (peak energy: evening)")
        choice = input("\nEnter choice (1-3) [default: 2]: ").strip() or "2"
        
        chronotype_map = {
            "1": Chronotype.EARLY_BIRD,
            "2": Chronotype.INTERMEDIATE,
            "3": Chronotype.NIGHT_OWL
        }
        chronotype = chronotype_map.get(choice, Chronotype.INTERMEDIATE)
        
        self.agent = LLMSchedulingAgent(chronotype=chronotype)
        print(f"\n✓ Agent configured with chronotype: {chronotype.value}")
    
    def add_sample_tasks(self):
        """Add sample tasks for demonstration"""
        sample_tasks = [
            Task(
                title="Write project proposal",
                description="Draft Q4 project proposal for new feature",
                duration=120,
                priority=Priority.HIGH,
                deadline=datetime.now() + timedelta(days=2),
                energy_level=EnergyLevel.HIGH,
                effort=8,
                reward=9,
                flexibility=Flexibility.SEMI_FLEXIBLE,
                tools=["laptop", "research notes"]
            ),
            Task(
                title="Team standup meeting",
                description="Daily sync with development team",
                duration=30,
                priority=Priority.MEDIUM,
                energy_level=EnergyLevel.MEDIUM,
                mode=TaskMode.SYNC,
                effort=3,
                reward=5,
                flexibility=Flexibility.RIGID,
                participants=["team"],
                location="office"
            ),
            Task(
                title="Code review",
                description="Review pull requests from team members",
                duration=60,
                priority=Priority.MEDIUM,
                energy_level=EnergyLevel.MEDIUM,
                effort=6,
                reward=6,
                flexibility=Flexibility.FLEXIBLE,
                tools=["laptop"]
            ),
            Task(
                title="Email responses",
                description="Clear inbox and respond to urgent emails",
                duration=45,
                priority=Priority.LOW,
                energy_level=EnergyLevel.LOW,
                effort=3,
                reward=4,
                flexibility=Flexibility.FLEXIBLE,
                tools=["laptop", "phone"]
            ),
            Task(
                title="Strategic planning session",
                description="Plan roadmap for next quarter",
                duration=90,
                priority=Priority.CRITICAL,
                deadline=datetime.now() + timedelta(days=1),
                energy_level=EnergyLevel.HIGH,
                effort=9,
                reward=10,
                flexibility=Flexibility.SEMI_FLEXIBLE,
                participants=["leadership team"],
                tools=["laptop", "whiteboard"]
            ),
            Task(
                title="Update documentation",
                description="Document recent API changes",
                duration=60,
                priority=Priority.MEDIUM,
                energy_level=EnergyLevel.MEDIUM,
                effort=5,
                reward=5,
                flexibility=Flexibility.FLEXIBLE,
                tools=["laptop"]
            ),
            Task(
                title="1-on-1 with direct report",
                description="Weekly check-in with team member",
                duration=30,
                priority=Priority.HIGH,
                energy_level=EnergyLevel.MEDIUM,
                mode=TaskMode.SYNC,
                effort=4,
                reward=7,
                flexibility=Flexibility.RIGID,
                participants=["direct report"],
                location="office"
            ),
            Task(
                title="Exercise break",
                description="Quick workout or walk",
                duration=30,
                priority=Priority.MEDIUM,
                energy_level=EnergyLevel.MEDIUM,
                effort=4,
                reward=8,
                flexibility=Flexibility.FLEXIBLE
            )
        ]
        
        for task in sample_tasks:
            self.agent.add_task(task)
        
        print(f"\n✓ Added {len(sample_tasks)} sample tasks to your schedule")
    
    def show_task_analysis(self):
        """Display task load analysis"""
        print("\n" + "="*60)
        print("Task Load Analysis")
        print("="*60)
        
        analysis = self.agent.analyze_task_load()
        
        print(f"\nTotal Tasks: {analysis['total_tasks']}")
        print(f"  - Incomplete: {analysis['incomplete_tasks']}")
        print(f"  - Completed: {analysis['completed_tasks']}")
        print(f"  - Overdue: {analysis['overdue_tasks']}")
        
        if analysis['overdue_task_titles']:
            print(f"\n⚠️  Overdue tasks: {', '.join(analysis['overdue_task_titles'])}")
        
        print(f"\nTotal Duration: {analysis['total_duration_hours']:.1f} hours")
        print(f"Average Effort: {analysis['average_effort']:.1f}/10")
        
        print("\nEnergy Distribution:")
        for level, count in analysis['energy_distribution'].items():
            print(f"  - {level.capitalize()}: {count} tasks")
        
        print("\nPriority Distribution:")
        for priority, count in analysis['priority_distribution'].items():
            print(f"  - {priority.capitalize()}: {count} tasks")
    
    def generate_daily_plan(self):
        """Generate and display daily plan"""
        print("\n" + "="*60)
        print("Generate Daily Plan")
        print("="*60)
        
        # Get date
        date_input = input("\nEnter date (YYYY-MM-DD) [default: today]: ").strip()
        if date_input:
            try:
                date = datetime.strptime(date_input, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Using today.")
                date = datetime.now()
        else:
            date = datetime.now()
        
        # Generate plan
        plan = self.agent.generate_daily_plan(date)
        
        print(f"\n{'='*60}")
        print(f"Daily Plan for {plan['date']}")
        print(f"{'='*60}")
        print(f"\nChronotype: {plan['chronotype'].replace('_', ' ').title()}")
        print(f"Working Hours: {plan['working_hours']}")
        print(f"Utilization: {plan['utilization']}")
        print(f"Scheduled Tasks: {plan['scheduled_tasks']}")
        print(f"Unscheduled Tasks: {plan['unscheduled_tasks']}")
        
        print(f"\n{'─'*60}")
        print("Energy Blocks for Your Chronotype:")
        print(f"{'─'*60}")
        for level in ['high', 'medium', 'low']:
            blocks = plan['energy_blocks'][level]
            if blocks:
                print(f"\n{level.upper()} Energy:")
                for start, end in blocks:
                    print(f"  {start} - {end}")
        
        print(f"\n{'─'*60}")
        print("Scheduled Tasks:")
        print(f"{'─'*60}")
        
        if plan['schedule']:
            for i, task in enumerate(plan['schedule'], 1):
                print(f"\n{i}. {task['title']}")
                print(f"   Time: {task['start_time']} - {task['end_time']} ({task['duration']} min)")
                print(f"   Priority: {task['priority'].upper()} | Energy: {task['energy_level'].upper()}")
                print(f"   Score: {task['priority_score']:.3f}")
                print(f"   Reasoning: {task['reasoning']}")
        else:
            print("\nNo tasks scheduled for this day.")
    
    def get_recommendations(self):
        """Get task recommendations"""
        print("\n" + "="*60)
        print("Task Recommendations")
        print("="*60)
        
        # Get context
        duration = input("\nHow much time do you have? (minutes) [default: 60]: ").strip()
        duration = int(duration) if duration else 60
        
        print("\nWhat's your current energy level?")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        energy_choice = input("Enter choice (1-3) [default: 2]: ").strip() or "2"
        energy_map = {"1": "low", "2": "medium", "3": "high"}
        energy = energy_map.get(energy_choice, "medium")
        
        # Get recommendations
        recommendations = self.agent.get_task_recommendations(
            available_duration=duration,
            energy_level=energy,
            top_n=5
        )
        
        print(f"\n{'─'*60}")
        print(f"Top Recommendations ({duration} min available, {energy} energy)")
        print(f"{'─'*60}")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['title']}")
                print(f"   Duration: {rec['duration']} min")
                print(f"   Priority: {rec['priority'].upper()} | Effort: {rec['effort']}/10 | Reward: {rec['reward']}/10")
                print(f"   Score: {rec['priority_score']:.3f}")
                print(f"   {rec['reasoning']}")
        else:
            print("\nNo tasks match your current criteria.")
    
    def export_schedule(self):
        """Export schedule"""
        print("\n" + "="*60)
        print("Export Schedule")
        print("="*60)
        
        print("\nSelect format:")
        print("1. JSON")
        print("2. Text")
        choice = input("Enter choice (1-2) [default: 2]: ").strip() or "2"
        
        format_map = {"1": "json", "2": "text"}
        format_type = format_map.get(choice, "text")
        
        output = self.agent.export_schedule(format=format_type)
        
        # Save to file
        filename = f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type[:4]}"
        with open(filename, 'w') as f:
            f.write(output)
        
        print(f"\n✓ Schedule exported to: {filename}")
        print("\nPreview:")
        print("─"*60)
        print(output[:500] + "..." if len(output) > 500 else output)
    
    def run(self):
        """Run the interactive CLI"""
        self.setup_agent()
        self.add_sample_tasks()
        
        while True:
            print("\n" + "="*60)
            print("Main Menu")
            print("="*60)
            print("\n1. View Task Analysis")
            print("2. Generate Daily Plan")
            print("3. Get Task Recommendations")
            print("4. Export Schedule")
            print("5. Exit")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == "1":
                self.show_task_analysis()
            elif choice == "2":
                self.generate_daily_plan()
            elif choice == "3":
                self.get_recommendations()
            elif choice == "4":
                self.export_schedule()
            elif choice == "5":
                print("\n✓ Thank you for using the AI-Powered Daily Planning System!")
                break
            else:
                print("\n⚠️  Invalid choice. Please try again.")


def main():
    """Main entry point"""
    cli = SchedulerCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n✓ Exiting... Goodbye!")
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
