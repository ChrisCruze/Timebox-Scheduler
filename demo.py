#!/usr/bin/env python3
"""
Quick demonstration of the AI-powered daily planning system.
"""
from datetime import datetime, timedelta
from task_model import Task, Priority, EnergyLevel, Flexibility
from llm_agent import LLMSchedulingAgent
from energy_scheduling import Chronotype


def demo():
    """Quick demo showing key features"""
    
    print("\n" + "="*70)
    print("🤖 AI-POWERED DAILY PLANNING SYSTEM - Quick Demo")
    print("="*70)
    
    # Setup
    print("\n📋 Setting up AI scheduling agent (Early Bird chronotype)...")
    agent = LLMSchedulingAgent(chronotype=Chronotype.EARLY_BIRD)
    
    # Add diverse tasks
    print("➕ Adding tasks with 15-field structured metadata...")
    tasks = [
        Task(
            title="🎯 Strategic Planning Session",
            description="Q4 roadmap planning",
            duration=90,
            priority=Priority.CRITICAL,
            deadline=datetime.now() + timedelta(hours=24),
            energy_level=EnergyLevel.HIGH,
            effort=9,
            reward=10,
            flexibility=Flexibility.SEMI_FLEXIBLE
        ),
        Task(
            title="👥 Daily Standup",
            duration=15,
            priority=Priority.MEDIUM,
            energy_level=EnergyLevel.MEDIUM,
            effort=2,
            reward=5,
            flexibility=Flexibility.RIGID
        ),
        Task(
            title="✉️ Email Triage",
            duration=30,
            priority=Priority.LOW,
            energy_level=EnergyLevel.LOW,
            effort=3,
            reward=4,
            flexibility=Flexibility.FLEXIBLE
        ),
        Task(
            title="💻 Code Review",
            duration=45,
            priority=Priority.MEDIUM,
            energy_level=EnergyLevel.MEDIUM,
            effort=6,
            reward=7,
            flexibility=Flexibility.FLEXIBLE
        ),
        Task(
            title="📝 Write Documentation",
            duration=60,
            priority=Priority.HIGH,
            energy_level=EnergyLevel.MEDIUM,
            effort=5,
            reward=6,
            flexibility=Flexibility.FLEXIBLE
        )
    ]
    
    for task in tasks:
        agent.add_task(task)
    
    print(f"   ✅ Added {len(tasks)} tasks")
    
    # Generate plan
    print("\n⚡ Generating energy-aware daily plan...")
    plan = agent.generate_daily_plan(datetime.now())
    
    print(f"\n{'='*70}")
    print(f"📅 Daily Schedule for {plan['date']}")
    print(f"{'='*70}")
    print(f"⏰ Working Hours: {plan['working_hours']}")
    print(f"📊 Utilization: {plan['utilization']}")
    print(f"✅ Tasks Scheduled: {plan['scheduled_tasks']}")
    
    print(f"\n{'─'*70}")
    print("🔋 Energy Blocks (Early Bird Optimized):")
    print(f"{'─'*70}")
    print("⚡ HIGH Energy: 06:00-12:00 (peak productivity)")
    print("⚡ MED Energy:  05:00-06:00, 12:00-18:00")
    print("⚡ LOW Energy:  00:00-05:00, 18:00-24:00")
    
    print(f"\n{'─'*70}")
    print("📋 Optimized Schedule:")
    print(f"{'─'*70}")
    
    for i, task in enumerate(plan['schedule'], 1):
        icon = "🎯" if task['priority'] == "critical" else "📝" if task['priority'] == "high" else "👤"
        energy_icon = "⚡⚡⚡" if task['energy_level'] == "high" else "⚡⚡" if task['energy_level'] == "medium" else "⚡"
        
        print(f"\n{i}. {icon} {task['title']}")
        print(f"   ⏰ {task['start_time']} - {task['end_time']}")
        print(f"   {energy_icon} Energy: {task['energy_level'].upper()}")
        print(f"   📊 Priority Score: {task['priority_score']:.3f}")
        print(f"   💡 {task['reasoning']}")
    
    # Get recommendations
    print(f"\n{'='*70}")
    print("🎯 AI Recommendations (60 min available, medium energy)")
    print(f"{'='*70}")
    
    recs = agent.get_task_recommendations(
        available_duration=60,
        energy_level="medium",
        top_n=3
    )
    
    for i, rec in enumerate(recs, 1):
        print(f"\n{i}. {rec['title']}")
        print(f"   ⏱️  {rec['duration']} min | Effort: {rec['effort']}/10 | Reward: {rec['reward']}/10")
        print(f"   📊 Score: {rec['priority_score']:.3f}")
    
    # Multi-criteria breakdown
    if recs:
        print(f"\n{'='*70}")
        print("🔍 Multi-Criteria Analysis (Top Task)")
        print(f"{'='*70}")
        breakdown = recs[0]['breakdown']
        print(f"\n📌 {recs[0]['title']}")
        print(f"\n   Urgency:    {breakdown['urgency']:.3f} (weighted: {breakdown['urgency_weighted']:.3f})")
        print(f"   Importance: {breakdown['importance']:.3f} (weighted: {breakdown['importance_weighted']:.3f})")
        print(f"   Effort:     {breakdown['effort']:.3f} (weighted: {breakdown['effort_weighted']:.3f})")
        print(f"   Wellbeing:  {breakdown['wellbeing']:.3f} (weighted: {breakdown['wellbeing_weighted']:.3f})")
        print(f"   ────────────────────────────────")
        print(f"   TOTAL:      {breakdown['total_score']:.3f}")
    
    print(f"\n{'='*70}")
    print("✨ Key Features Demonstrated:")
    print(f"{'='*70}")
    print("✅ 15-field structured task metadata")
    print("✅ Multi-criteria prioritization (urgency, importance, effort, wellbeing)")
    print("✅ Energy-aware scheduling aligned with chronotype")
    print("✅ Intelligent timeboxing and task placement")
    print("✅ Real-time task recommendations")
    print("✅ AI-powered daily planning")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    demo()
