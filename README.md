# Timebox-Scheduler

An intelligent AI-powered day planning system that uses LLM agents for automated task scheduling, timeboxing, and priority management. Built with structured task metadata, energy-aware scheduling, and real-time rescheduling capabilities.

## Overview

Timeboxing transforms intention into action by assigning fixed blocks of time to tasks. This system combines cognitive science, AI inference, and automated scheduling to help individuals achieve clarity, focus, and balanced progress toward their goals.

### Key Benefits

- **Save 40+ hours/week** through intelligent automation
- **60% productivity increase** (MIT study on AI planning agents)
- **Reduce cognitive load** by offloading scheduling logistics to AI
- **Energy-aligned scheduling** that respects your natural rhythms
- **Real-time adaptation** when plans change

## Features

### 1. Structured Task Metadata (15 Essential Fields)

Every task is enriched with comprehensive metadata to enable intelligent scheduling:

1. **Task Title** - Action-oriented description
2. **Description** - Context, intent, and expectations
3. **Estimated Duration** - Focused time needed
4. **Priority** - Urgency and importance ranking
5. **Deadline** - Hard or soft completion date
6. **Dependencies** - Prerequisites and blockers
7. **Energy/Focus Level** - Cognitive intensity required
8. **Location/Context** - Where the task must occur
9. **Participants** - Stakeholders involved
10. **Mode of Work** - Creative, analytical, administrative, etc.
11. **Effort/Complexity** - Mental strain rating (1-5)
12. **Flexibility** - How movable the task is
13. **Status** - Not started, in progress, blocked, completed
14. **Reward/Value** - Intrinsic or extrinsic benefit
15. **Tools & Resources** - Required software and materials

### 2. Multi-Criteria Prioritization

The system applies a structured method that balances:

- **Urgency First** - Time-sensitive deliverables scheduled early
- **Importance Over Activity** - Strategic work prioritized over busywork
- **Effort & Duration Awareness** - Deep work at peak energy times
- **Avoid Overload** - Realistic daily limits with 10-15% buffer time
- **Personal Preference Matching** - Respects working hours and focus periods
- **Task Dependency Handling** - Proper sequencing of prerequisites
- **Adaptive Flexibility** - Dynamic rescheduling when changes occur

### 3. Energy-Aware Scheduling

AI aligns tasks with user energy curves:

- Deep, cognitively demanding tasks → Peak energy windows
- Low-energy tasks → Energy troughs
- Creative work → Personal creative peaks
- Routine admin → Lower-value hours

### 4. Intelligent Agent Capabilities

**Essential Inputs:**
- Task list with metadata
- Calendar data (meetings, events)
- User preferences (working hours, focus times)
- Project metadata (milestones, progress)
- Historical data (completion patterns)
- Availability (free/busy slots)
- Input channels (text, voice, API)

**Essential Outputs:**
- Time-boxed daily schedule
- Task assignments with timing recommendations
- Conflict detection and resolution
- Notifications and reminders
- Progress updates and analytics
- Rescheduling suggestions
- Summary reports

## System Architecture

### Core Components

1. **Data Integration Foundation**
   - Connect calendars (Google, Outlook)
   - Sync to-do and project tools (Todoist, Notion)
   - Normalize data models

2. **Scheduling Engine**
   - Priority-based allocation
   - Constraint satisfaction
   - Energy curve alignment
   - Context clustering

3. **Real-Time Awareness**
   - Monitor calendar and task changes
   - Recalculate schedules dynamically
   - Surface urgent items

4. **User Model**
   - Track working patterns
   - Learn energy cycles
   - Adapt from feedback

5. **Communication Layer**
   - Proactive notifications
   - Rescheduling prompts
   - Progress updates

### Scheduling Algorithm

**Step 1:** Filter mandatory events (fixed meetings)  
**Step 2:** Sort by deadline & importance  
**Step 3:** Align with user energy patterns  
**Step 4:** Fill gaps with quick wins  
**Step 5:** Recalculate as needed

## Task JSON Schema

```json
{
  "title": "Draft Chapter on Sustainable Energy",
  "description": "Write initial 3,000-word draft explaining renewable technology trends",
  "duration_estimate": "3 hours",
  "priority": "high",
  "deadline": "2025-11-20",
  "dependencies": ["Outline approved"],
  "energy_level": "high",
  "location": "home office",
  "participants": [],
  "mode": "creative",
  "effort": 4,
  "flexibility": "medium",
  "status": "not started",
  "reward": "Contributes to book deadline submission",
  "tools": ["Notion", "Google Docs"]
}
```

## Prompt Engineering

### Attribute Extraction Prompt

```
Analyze the following task description. Extract:
- Context
- Estimated duration
- Energy level
- Inferred priority

Return as JSON.

Task: "[TASK_DESCRIPTION]"
```

### Task Enrichment Prompt

```
Rewrite the task to:
- Create a clearer title
- Add a detailed description
- Break into sub-tasks (if complex)

Return as JSON.

Task: "[TASK_DESCRIPTION]"
```

### Scheduling Synthesis Prompt

```
Given analyzed tasks and calendar data:
- Generate an optimized daily schedule
- Respect energy patterns
- Batch similar tasks
- Insert breaks

Return in time-ordered list format.
```

## Research & Evidence

- **MIT Study**: Up to 60% productivity improvement with AI planning agents
- **Team Results**: ~40 hours/week saved using LLM scheduling agents
- **LEAP & LEAN**: >30 percentage point increase in task completion rates
- **Meta-Task Planning (MTP)**: Marked improvements in itinerary planning success

## Implementation Blueprint

### MVP Feature Set

1. Task import and parsing
2. Calendar sync (Google, Outlook)
3. Automatic scheduling algorithm
4. Priority and deadline handling
5. Basic rescheduling logic
6. Notifications and reminders

### Development Roadmap

**Phase 1** - Core Integration  
- Calendar and to-do system APIs
- Data normalization
- Basic UI

**Phase 2** - Intelligent Scheduling  
- Priority-based allocation
- Energy curve modeling
- Drag-and-drop manual adjustments

**Phase 3** - Real-Time Awareness  
- Event listeners for changes
- Dynamic recalculation
- Conflict detection

**Phase 4** - Personalization  
- User pattern learning
- Preference adaptation
- Feedback loops

**Phase 5** - Advanced Features  
- Weekly reflections
- Analytics dashboard
- Habit tracking

**Phase 6** - Team Collaboration  
- Shared visibility
- Workload balancing
- Multi-user coordination

## UI Generation (Mercury Dashboard Style)

Built with:
- **Tailwind CSS** for styling
- **Firebase Realtime Database** for data storage
- **Chart.js** for visualizations
- **Lucide Icons** for UI elements
- Clean white/off-white backgrounds
- Lavender-to-purple gradients
- Two-column layout with fixed sidebar
- Cards with 12-16px radius
- Subtle <150ms animations

### Firebase Configuration

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyCsT8RKgb9Ya4zW8SfMrUY4ovxLS6n39v8",
  authDomain: "chriscruz-d62ea.firebaseapp.com",
  databaseURL: "https://chriscruz-d62ea-default-rtdb.firebaseio.com",
  projectId: "chriscruz-d62ea",
  storageBucket: "chriscruz-d62ea.firebasestorage.app",
  messagingSenderId: "817856028090",
  appId: "1:817856028090:web:983d8c52bb3c7202dc5183",
  measurementId: "G-LVHF0VP8RM"
};
```

## Example Daily Schedule

| Time | Task | Context |
|------|------|------|
| 8:00-8:30 | Morning run | Physical health |
| 8:30-9:00 | Breakfast / reflection | Buffer |
| 9:00-10:00 | Write report (Part 1) | Deep work |
| 10:00-11:00 | Design review meeting | Collaboration |
| 11:00-12:00 | Write report (Part 2) | Deep work |
| 12:00-12:30 | Lunch | Recovery |
| 12:30-14:30 | Prepare team slides | Creative session |
| 14:30-15:00 | Break | Buffer |
| 15:00-16:00 | Reply to client emails | Administrative |
| 16:00-17:00 | Review schedule for tomorrow | Planning |

## Best Practices

### For Users

1. **Provide rich task metadata** - More context enables better scheduling
2. **Review and adjust** - Keep the AI informed about changes
3. **Track energy patterns** - Help the system learn your rhythms
4. **Set realistic buffers** - Allow 10-15% slack for interruptions
5. **Give feedback** - Rate scheduling decisions to improve accuracy

### For Developers

1. **Start with integrations** - Calendar and to-do sync first
2. **Track user edits** - Learn preferences from manual adjustments
3. **Prioritize transparency** - Explain why tasks are scheduled when they are
4. **Enable undo** - All automated changes should be reversible
5. **Implement gradual rollout** - Ship features incrementally with clear success metrics

## Human-AI Collaboration

The most effective systems balance automation with control:

- **AI handles logistics** - Constraint solving, optimization, monitoring
- **Human maintains intent** - Goals, priorities, values, preferences
- **AI proposes updates** - Suggestions based on changes
- **Human approves changes** - Final say on schedule modifications

This partnership ensures productivity gains while maintaining user agency.

## Contributing

Contributions are welcome! Areas of interest:

- Additional calendar integrations
- Enhanced energy modeling algorithms
- Mobile app development
- Team collaboration features
- Analytics and insights
- Natural language task parsing

## License

MIT License - see LICENSE file for details

## References

- [What Is an AI Planner? (Morgen)](https://www.morgen.so/blog-posts/what-is-an-ai-planner-and-why-youll-want-one)
- [Plan My Day (BeforeSunset AI)](https://www.beforesunset.ai/post/plan-my-day)
- [Best AI Daily Planners (BeforeSunset AI)](https://www.beforesunset.ai/post/ai-daily-planners-you-must-try)
- [The 10 Best AI Tools for Time Management (Slack)](https://slack.com/blog/productivity/the-10-best-ai-tools-for-time-management)
- MIT Research on AI Agents and Productivity

## Acknowledgments

Built on research in cognitive science, productivity systems (GTD, Deep Work, Pomodoro), and modern LLM agent architectures. Inspired by the need to transform planning from a chore into a seamless, intelligent partnership between humans and AI.

---

**Status**: Active Development  
**Last Updated**: November 2025
