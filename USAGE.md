# Usage Guide

This guide provides detailed instructions on how to use the AI-Powered Daily Planning System.

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/ChrisCruze/Timebox-Scheduler.git
cd Timebox-Scheduler

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Interactive CLI

```bash
python scheduler_cli.py
```

This will launch an interactive menu where you can:
- View task analysis
- Generate daily plans
- Get task recommendations
- Export your schedule

### 3. Run the Example

```bash
python example.py
```

This demonstrates all key features with sample tasks.

### 4. Run the Quick Demo

```bash
python demo.py
```

This provides a visual demonstration of the system in action.

## Programmatic Usage

### Creating Tasks

Tasks require comprehensive metadata (15 fields):

```python
from datetime import datetime, timedelta
from task_model import Task, Priority, EnergyLevel, TaskMode, Flexibility

task = Task(
    # Required fields
    title="Write Project Proposal",
    duration=120,  # minutes
    
    # Optional fields with defaults
    description="Draft Q4 project proposal",
    priority=Priority.HIGH,  # LOW, MEDIUM, HIGH, CRITICAL
    deadline=datetime.now() + timedelta(days=2),
    dependencies=["task_id_1", "task_id_2"],
    energy_level=EnergyLevel.HIGH,  # LOW, MEDIUM, HIGH
    location="office",
    participants=["team member 1", "team member 2"],
    mode=TaskMode.SYNC,  # SYNC, ASYNC, HYBRID
    effort=8,  # 1-10 scale
    flexibility=Flexibility.SEMI_FLEXIBLE,  # RIGID, SEMI_FLEXIBLE, FLEXIBLE
    status=TaskStatus.NOT_STARTED,  # NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED, CANCELLED
    reward=9,  # 1-10 scale
    tools=["laptop", "research notes"]
)
```

### Setting Up the Agent

```python
from llm_agent import LLMSchedulingAgent
from energy_scheduling import Chronotype

# Choose your chronotype
agent = LLMSchedulingAgent(
    chronotype=Chronotype.EARLY_BIRD  # EARLY_BIRD, INTERMEDIATE, NIGHT_OWL
)

# Add tasks
agent.add_task(task)
```

### Generating Daily Plans

```python
from datetime import datetime

# Generate plan for today
plan = agent.generate_daily_plan(
    date=datetime.now(),
    working_hours_start=8,  # 8 AM
    working_hours_end=18,   # 6 PM
    break_duration=60,      # 1 hour break
    max_tasks=10            # Optional limit
)

# Access plan details
print(f"Scheduled {plan['scheduled_tasks']} tasks")
print(f"Utilization: {plan['utilization']}")

for task in plan['schedule']:
    print(f"{task['start_time']} - {task['end_time']}: {task['title']}")
    print(f"  Reasoning: {task['reasoning']}")
```

### Getting Task Recommendations

```python
# Get recommendations based on current context
recommendations = agent.get_task_recommendations(
    available_duration=60,     # minutes available
    energy_level="medium",     # current energy: low/medium/high
    location="office",         # optional: current location
    top_n=5                    # number of recommendations
)

for rec in recommendations:
    print(f"{rec['title']}: {rec['reasoning']}")
    print(f"  Priority Score: {rec['priority_score']:.3f}")
    print(f"  Breakdown: {rec['breakdown']}")
```

### Analyzing Task Load

```python
analysis = agent.analyze_task_load()

print(f"Total tasks: {analysis['total_tasks']}")
print(f"Incomplete: {analysis['incomplete_tasks']}")
print(f"Total duration: {analysis['total_duration_hours']:.1f} hours")
print(f"Average effort: {analysis['average_effort']:.1f}/10")
print(f"Overdue tasks: {analysis['overdue_tasks']}")

# Energy distribution
for level, count in analysis['energy_distribution'].items():
    print(f"{level}: {count} tasks")
```

### Custom Prioritization

```python
from prioritization import PrioritizationEngine

# Create engine with custom weights
engine = PrioritizationEngine(
    urgency_weight=0.4,      # 40%
    importance_weight=0.3,   # 30%
    effort_weight=0.2,       # 20%
    wellbeing_weight=0.1     # 10%
)

# Use in agent
agent = LLMSchedulingAgent(
    chronotype=Chronotype.INTERMEDIATE,
    prioritization_engine=engine
)
```

### Filtering Tasks

```python
from prioritization import PrioritizationEngine

engine = PrioritizationEngine()

# Filter tasks by constraints
eligible_tasks = engine.filter_by_constraints(
    tasks,
    available_energy="medium",
    available_location="office",
    available_duration=60
)

# Get top recommendations
recommendations = engine.recommend_next_task(
    tasks,
    available_energy="high",
    available_duration=120,
    top_n=3
)
```

### Exporting Schedule

```python
# Export as JSON
json_schedule = agent.export_schedule(format="json")

# Export as text
text_schedule = agent.export_schedule(format="text")

# Save to file
with open("schedule.json", "w") as f:
    f.write(json_schedule)
```

## Understanding Chronotypes

### Early Bird (Morning Person)
- **Peak Energy**: 6:00 AM - 12:00 PM
- **Medium Energy**: 5:00 AM - 6:00 AM, 12:00 PM - 6:00 PM
- **Low Energy**: 6:00 PM - 5:00 AM
- **Best for**: High-energy tasks scheduled in the morning

### Intermediate (Neutral)
- **Peak Energy**: 9:00 AM - 5:00 PM
- **Medium Energy**: 6:00 AM - 9:00 AM, 5:00 PM - 8:00 PM
- **Low Energy**: 8:00 PM - 6:00 AM
- **Best for**: Standard work schedule alignment

### Night Owl (Evening Person)
- **Peak Energy**: 2:00 PM - 10:00 PM
- **Medium Energy**: 9:00 AM - 2:00 PM, 10:00 PM - 1:00 AM
- **Low Energy**: 1:00 AM - 9:00 AM
- **Best for**: High-energy tasks scheduled in the afternoon/evening

## Multi-Criteria Prioritization

The system uses a weighted scoring algorithm:

```
Priority Score = (Urgency × 0.30) + (Importance × 0.35) + 
                 ((1 - Effort) × 0.15) + (Wellbeing × 0.20)
```

### Component Breakdown

1. **Urgency (30% weight)**
   - Deadline proximity
   - Priority level (LOW, MEDIUM, HIGH, CRITICAL)
   
2. **Importance (35% weight)**
   - Priority level
   - Reward value (1-10)
   
3. **Effort (15% weight)**
   - Inverted: Lower effort = higher priority
   - Effort level (1-10)
   
4. **Well-being (20% weight)**
   - High reward + Low effort = High well-being
   - Combines reward (60%) and inverted effort (40%)

## Advanced Features

### Dependency Management

```python
# Task B depends on Task A
task_a = Task(title="Design API", duration=60, task_id="task_a")
task_b = Task(title="Implement API", duration=120, dependencies=["task_a"])

agent.add_task(task_a)
agent.add_task(task_b)

# Mark task A as completed
task_a.status = TaskStatus.COMPLETED

# Now task B can be scheduled
plan = agent.generate_daily_plan(datetime.now())
```

### Dynamic Replanning

```python
# Handle interruption
new_plan = agent.replan_on_interruption(
    current_time=datetime.now(),
    interrupted_task_id="task_123",
    remaining_duration=45  # minutes remaining
)
```

### Energy-Aware Scheduling

```python
from energy_scheduling import EnergyScheduler

scheduler = EnergyScheduler(Chronotype.EARLY_BIRD)

# Find optimal time slots
slots = scheduler.find_optimal_time_slots(
    task,
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=1)
)

# Schedule with conflict detection
slot = scheduler.schedule_task(
    task,
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=1),
    existing_schedule=scheduled_tasks
)
```

## Tips for Effective Use

1. **Be Accurate with Metadata**: The more accurate your task metadata, the better the scheduling decisions.

2. **Choose the Right Chronotype**: Select the chronotype that matches your natural energy patterns for optimal scheduling.

3. **Set Realistic Durations**: Estimate task durations conservatively to avoid over-scheduling.

4. **Use Dependencies**: Link related tasks to ensure proper sequencing.

5. **Adjust Flexibility**: Mark time-sensitive meetings as RIGID, flexible tasks as FLEXIBLE.

6. **Review Energy Levels**: Assign appropriate energy levels to ensure tasks are scheduled during suitable times.

7. **Leverage Recommendations**: Use the recommendation feature when you have unexpected free time.

8. **Regular Updates**: Update task statuses regularly to keep the schedule accurate.

## Troubleshooting

### Tasks Not Being Scheduled

- Check if dependencies are met
- Verify task duration fits in available time
- Ensure energy level matches available energy blocks
- Check if deadline has passed

### Low Utilization

- Add more tasks to the schedule
- Increase working hours
- Reduce break duration
- Check task flexibility settings

### Unexpected Ordering

- Review priority scores and breakdowns
- Adjust prioritization weights if needed
- Verify task metadata (effort, reward, priority)
- Check energy level alignment

## Running Tests

```bash
# Run all tests
python test_scheduler.py

# Run with verbose output
python -m unittest test_scheduler.py -v
```

## Next Steps

- Explore the example.py and demo.py scripts
- Customize prioritization weights for your workflow
- Experiment with different chronotypes
- Build your own task sets
- Integrate with calendar systems
- Add persistence (save/load schedules)
