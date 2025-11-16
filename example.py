#!/usr/bin/env python3
"""
Example usage of the AI-powered daily planning system.
"""
from datetime import datetime, timedelta
from task_model import Task, Priority, EnergyLevel, TaskMode, Flexibility
from llm_agent import LLMSchedulingAgent
from energy_scheduling import Chronotype


def main():
    """Demonstrate the scheduling system with a practical example"""
    
    print("\n" + "="*70)
    print("AI-Powered Daily Planning System - Example Usage")
    print("="*70)
    
    # Step 1: Initialize the agent with user chronotype
    print("\n1. Initializing scheduling agent...")
    agent = LLMSchedulingAgent(chronotype=Chronotype.EARLY_BIRD)
    print("   ✓ Agent configured as Early Bird (peak energy: mornings)")
    
    # Step 2: Add tasks with comprehensive metadata
    print("\n2. Adding tasks with 15-field structured metadata...")
    
    tasks = [
        Task(
            title="Deep work: Algorithm optimization",
            description="Optimize core algorithm for 20% performance improvement",
            duration=120,
            priority=Priority.CRITICAL,
            deadline=datetime.now() + timedelta(days=1),
            energy_level=EnergyLevel.HIGH,
            effort=9,
            reward=10,
            flexibility=Flexibility.SEMI_FLEXIBLE,
            tools=["laptop", "profiling tools", "IDE"]
        ),
        Task(
            title="Team standup",
            description="Daily team synchronization",
            duration=15,
            priority=Priority.MEDIUM,
            energy_level=EnergyLevel.MEDIUM,
            mode=TaskMode.SYNC,
            effort=2,
            reward=5,
            flexibility=Flexibility.RIGID,
            participants=["dev team"],
            location="office"
        ),
        Task(
            title="Email triage",
            description="Process and respond to emails",
            duration=30,
            priority=Priority.LOW,
            energy_level=EnergyLevel.LOW,
            effort=3,
            reward=4,
            flexibility=Flexibility.FLEXIBLE
        ),
        Task(
            title="Client presentation prep",
            description="Prepare slides for client demo",
            duration=90,
            priority=Priority.HIGH,
            deadline=datetime.now() + timedelta(days=2),
            energy_level=EnergyLevel.HIGH,
            effort=7,
            reward=9,
            flexibility=Flexibility.SEMI_FLEXIBLE,
            tools=["laptop", "presentation software"],
            participants=["client", "sales team"]
        ),
        Task(
            title="Code review cycle",
            description="Review team PRs and provide feedback",
            duration=45,
            priority=Priority.MEDIUM,
            energy_level=EnergyLevel.MEDIUM,
            effort=5,
            reward=6,
            flexibility=Flexibility.FLEXIBLE,
            tools=["laptop"]
        ),
    ]
    
    for task in tasks:
        agent.add_task(task)
    
    print(f"   ✓ Added {len(tasks)} tasks to schedule")
    
    # Step 3: Analyze task load
    print("\n3. Analyzing task load...")
    analysis = agent.analyze_task_load()
    
    print(f"\n   Task Load Summary:")
    print(f"   • Total duration: {analysis['total_duration_hours']:.1f} hours")
    print(f"   • Average effort: {analysis['average_effort']:.1f}/10")
    print(f"   • Energy distribution:")
    for level, count in analysis['energy_distribution'].items():
        print(f"     - {level.capitalize()}: {count} tasks")
    
    # Step 4: Generate optimized daily plan
    print("\n4. Generating AI-powered daily plan...")
    today = datetime.now()
    plan = agent.generate_daily_plan(today, working_hours_start=8, working_hours_end=18)
    
    print(f"\n   Daily Plan for {plan['date']}")
    print(f"   {'─'*66}")
    print(f"   Working hours: {plan['working_hours']}")
    print(f"   Time utilization: {plan['utilization']}")
    print(f"   Tasks scheduled: {plan['scheduled_tasks']}")
    
    # Step 5: Show energy-aware schedule
    print("\n5. Energy-aware schedule (optimized for Early Bird):")
    print(f"   {'─'*66}")
    
    if plan['schedule']:
        for i, task in enumerate(plan['schedule'], 1):
            print(f"\n   {i}. {task['title']}")
            print(f"      ⏰ {task['start_time']} - {task['end_time']}")
            print(f"      ⚡ Energy: {task['energy_level'].upper()}")
            print(f"      📊 Priority: {task['priority'].upper()} (score: {task['priority_score']:.3f})")
            print(f"      💡 {task['reasoning']}")
    
    # Step 6: Get real-time recommendations
    print("\n6. Getting AI recommendations for current context...")
    recommendations = agent.get_task_recommendations(
        available_duration=60,
        energy_level="medium",
        top_n=3
    )
    
    print(f"\n   Top 3 recommendations (60 min available, medium energy):")
    print(f"   {'─'*66}")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n   {i}. {rec['title']}")
        print(f"      Duration: {rec['duration']} min")
        print(f"      Effort: {rec['effort']}/10 | Reward: {rec['reward']}/10")
        print(f"      Score: {rec['priority_score']:.3f}")
        print(f"      Why: {rec['reasoning']}")
    
    # Step 7: Show multi-criteria prioritization breakdown
    print("\n7. Multi-criteria prioritization breakdown for top task:")
    print(f"   {'─'*66}")
    
    if recommendations:
        top_task = recommendations[0]
        breakdown = top_task['breakdown']
        
        print(f"\n   Task: {top_task['title']}")
        print(f"\n   Component Scores:")
        print(f"   • Urgency:    {breakdown['urgency']:.3f} (weighted: {breakdown['urgency_weighted']:.3f})")
        print(f"   • Importance: {breakdown['importance']:.3f} (weighted: {breakdown['importance_weighted']:.3f})")
        print(f"   • Effort:     {breakdown['effort']:.3f} (weighted: {breakdown['effort_weighted']:.3f})")
        print(f"   • Wellbeing:  {breakdown['wellbeing']:.3f} (weighted: {breakdown['wellbeing_weighted']:.3f})")
        print(f"   • TOTAL:      {breakdown['total_score']:.3f}")
    
    # Step 8: Demonstrate energy curve
    print("\n8. Energy curve for Early Bird chronotype:")
    print(f"   {'─'*66}")
    
    energy_report = plan['energy_blocks']
    for level in ['high', 'medium', 'low']:
        if energy_report[level]:
            print(f"\n   {level.upper()} Energy Blocks:")
            for start, end in energy_report[level]:
                print(f"   • {start} - {end}")
    
    print("\n" + "="*70)
    print("✓ Example completed successfully!")
    print("="*70)
    print("\nKey Features Demonstrated:")
    print("  1. ✓ 15-field structured task metadata")
    print("  2. ✓ Multi-criteria prioritization (urgency, importance, effort, wellbeing)")
    print("  3. ✓ Energy-aware scheduling aligned with chronotype")
    print("  4. ✓ AI-powered daily planning")
    print("  5. ✓ Real-time task recommendations")
    print("  6. ✓ Intelligent timeboxing")
    print("\n")


if __name__ == "__main__":
    main()
