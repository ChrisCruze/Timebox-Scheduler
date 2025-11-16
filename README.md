# Timebox-Scheduler

An intelligent AI-powered day planning system that uses LLM agents for automated task scheduling, timeboxing, and priority management. Built with structured task metadata, energy-aware scheduling, and real-time rescheduling capabilities.

## Features

### 1. Structured Task Metadata (15 Fields)
Every task includes comprehensive metadata for intelligent scheduling:

1. **Title** - Task name/identifier
2. **Description** - Detailed task information
3. **Duration** - Expected time in minutes
4. **Priority** - Low, Medium, High, or Critical
5. **Deadline** - Optional due date/time
6. **Dependencies** - Tasks that must complete first
7. **Energy Level** - Low, Medium, or High energy required
8. **Location** - Where the task needs to be performed
9. **Participants** - People involved in the task
10. **Mode** - Sync (real-time), Async, or Hybrid
11. **Effort** - Cognitive/physical effort (1-10 scale)
12. **Flexibility** - Rigid, Semi-flexible, or Flexible timing
13. **Status** - Not Started, In Progress, Completed, Blocked, Cancelled
14. **Reward** - Motivational/satisfaction value (1-10 scale)
15. **Tools** - Required resources/equipment

### 2. Multi-Criteria Prioritization
Intelligent task ranking using four weighted dimensions:
- **Urgency** (30%) - Based on deadline proximity and priority level
- **Importance** (35%) - Derived from priority and reward value
- **Effort** (15%) - Inverse scoring (lower effort = higher priority)
- **Well-being** (20%) - Impact on personal satisfaction (high reward, low effort)

### 3. Energy-Aware Scheduling
Tasks are scheduled according to your natural energy patterns:

**Chronotypes Supported:**
- **Early Bird** - Peak energy 6am-12pm
- **Intermediate** - Peak energy 9am-5pm  
- **Night Owl** - Peak energy 2pm-10pm

High-energy tasks are automatically scheduled during your peak hours, low-energy tasks during energy dips.

### 4. AI-Powered Planning
The LLM scheduling agent provides:
- Automated daily plan generation
- Real-time task recommendations based on context
- Dynamic replanning on interruptions
- Dependency-aware scheduling
- Task load analysis and insights

## Installation

```bash
# Clone the repository
git clone https://github.com/ChrisCruze/Timebox-Scheduler.git
cd Timebox-Scheduler

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Run the Interactive CLI
```bash
python scheduler_cli.py
```

### Run the Example
```bash
python example.py
```

### Programmatic Usage
```python
from datetime import datetime, timedelta
from task_model import Task, Priority, EnergyLevel
from llm_agent import LLMSchedulingAgent
from energy_scheduling import Chronotype

# Initialize agent with your chronotype
agent = LLMSchedulingAgent(chronotype=Chronotype.EARLY_BIRD)

# Add a task with structured metadata
task = Task(
    title="Write project proposal",
    description="Draft Q4 project proposal",
    duration=120,
    priority=Priority.HIGH,
    deadline=datetime.now() + timedelta(days=2),
    energy_level=EnergyLevel.HIGH,
    effort=8,
    reward=9,
    tools=["laptop", "research notes"]
)
agent.add_task(task)

# Generate optimized daily plan
plan = agent.generate_daily_plan(datetime.now())
print(f"Scheduled {plan['scheduled_tasks']} tasks")
print(f"Utilization: {plan['utilization']}")

# Get task recommendations for current context
recommendations = agent.get_task_recommendations(
    available_duration=60,
    energy_level="high",
    top_n=3
)

for rec in recommendations:
    print(f"{rec['title']}: {rec['reasoning']}")
```

## Architecture

### Core Components

1. **task_model.py** - Pydantic models for 15-field task metadata
2. **prioritization.py** - Multi-criteria decision engine
3. **energy_scheduling.py** - Chronotype-based energy-aware scheduling
4. **llm_agent.py** - AI scheduling agent with planning logic
5. **scheduler_cli.py** - Interactive command-line interface
6. **example.py** - Demonstration script

### Task Prioritization Algorithm

```
Priority Score = (Urgency × 0.30) + (Importance × 0.35) + 
                 ((1 - Effort) × 0.15) + (Wellbeing × 0.20)

Where:
  Urgency = f(deadline_proximity, priority_level)
  Importance = f(priority_level, reward_value)
  Effort = normalized_effort_score
  Wellbeing = f(reward_value, effort_level)
```

### Energy-Aware Scheduling

Tasks are matched to time slots based on:
1. User's chronotype energy curve
2. Task energy requirements
3. Task flexibility constraints
4. Existing schedule conflicts

## Use Cases

- **Personal Productivity** - Optimize your daily schedule
- **Team Planning** - Coordinate tasks across team members
- **Project Management** - Schedule project tasks intelligently
- **Time Blocking** - Automated timeboxing based on priorities
- **Meeting Scheduling** - Find optimal meeting times
- **Focus Time** - Protect high-energy periods for deep work

## CLI Features

The interactive CLI provides:
1. Task load analysis and insights
2. Daily plan generation
3. Context-aware task recommendations
4. Schedule export (JSON/text formats)
5. Chronotype configuration

## Advanced Features

### Dependency Management
Tasks can specify dependencies that must be completed first:
```python
task = Task(
    title="Write tests",
    dependencies=["task_id_1"],  # Waits for another task
    ...
)
```

### Dynamic Replanning
Handle interruptions gracefully:
```python
new_plan = agent.replan_on_interruption(
    current_time=datetime.now(),
    interrupted_task_id="task_123",
    remaining_duration=45
)
```

### Task Filtering
Filter tasks by constraints:
```python
from prioritization import PrioritizationEngine

engine = PrioritizationEngine()
eligible = engine.filter_by_constraints(
    tasks,
    available_energy="medium",
    available_location="office",
    available_duration=60
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Credits

Built with:
- Pydantic for data validation
- Python datetime for time management
- Structured AI reasoning for intelligent scheduling
