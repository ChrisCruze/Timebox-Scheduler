"""
Task metadata model with 15 structured fields for intelligent scheduling.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum


class EnergyLevel(str, Enum):
    """Energy level required for a task"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Priority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskMode(str, Enum):
    """Mode of task execution"""
    SYNC = "sync"  # Synchronous, in-person
    ASYNC = "async"  # Asynchronous, can be done anytime
    HYBRID = "hybrid"  # Mix of both


class TaskStatus(str, Enum):
    """Current status of task"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class Flexibility(str, Enum):
    """How flexible the task timing is"""
    RIGID = "rigid"  # Must be done at specific time
    SEMI_FLEXIBLE = "semi_flexible"  # Some flexibility
    FLEXIBLE = "flexible"  # Can be done anytime


class Task(BaseModel):
    """
    Comprehensive task model with 15 structured fields for AI-powered scheduling.
    """
    # 1. Title
    title: str = Field(..., description="Task name/title")
    
    # 2. Description
    description: str = Field(default="", description="Detailed task description")
    
    # 3. Duration (in minutes)
    duration: int = Field(..., gt=0, description="Expected duration in minutes")
    
    # 4. Priority
    priority: Priority = Field(default=Priority.MEDIUM, description="Task priority level")
    
    # 5. Deadline
    deadline: Optional[datetime] = Field(default=None, description="Task deadline")
    
    # 6. Dependencies
    dependencies: List[str] = Field(default_factory=list, description="List of task IDs this task depends on")
    
    # 7. Energy Level
    energy_level: EnergyLevel = Field(default=EnergyLevel.MEDIUM, description="Energy required for task")
    
    # 8. Location
    location: Optional[str] = Field(default=None, description="Where task needs to be performed")
    
    # 9. Participants
    participants: List[str] = Field(default_factory=list, description="People involved in the task")
    
    # 10. Mode
    mode: TaskMode = Field(default=TaskMode.SYNC, description="Synchronous or asynchronous task")
    
    # 11. Effort (cognitive/physical effort score 1-10)
    effort: int = Field(default=5, ge=1, le=10, description="Effort level required (1-10)")
    
    # 12. Flexibility
    flexibility: Flexibility = Field(default=Flexibility.FLEXIBLE, description="How flexible the timing is")
    
    # 13. Status
    status: TaskStatus = Field(default=TaskStatus.NOT_STARTED, description="Current task status")
    
    # 14. Reward (motivational value 1-10)
    reward: int = Field(default=5, ge=1, le=10, description="Motivational/reward value (1-10)")
    
    # 15. Tools
    tools: List[str] = Field(default_factory=list, description="Tools/resources needed for task")
    
    # Additional metadata
    task_id: Optional[str] = Field(default=None, description="Unique task identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Task creation timestamp")
    scheduled_start: Optional[datetime] = Field(default=None, description="Scheduled start time")
    scheduled_end: Optional[datetime] = Field(default=None, description="Scheduled end time")
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self):
        """Convert task to dictionary with ISO format dates"""
        data = self.model_dump()
        # Convert datetime objects to ISO format strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data
    
    def get_urgency_score(self) -> float:
        """Calculate urgency score based on deadline and priority"""
        urgency = 0.0
        
        # Priority contributes 50% to urgency
        priority_map = {
            Priority.LOW: 0.25,
            Priority.MEDIUM: 0.5,
            Priority.HIGH: 0.75,
            Priority.CRITICAL: 1.0
        }
        urgency += priority_map[self.priority] * 0.5
        
        # Deadline proximity contributes 50% to urgency
        if self.deadline:
            time_until_deadline = (self.deadline - datetime.now()).total_seconds()
            if time_until_deadline < 0:
                urgency += 0.5  # Overdue
            elif time_until_deadline < 86400:  # Less than 1 day
                urgency += 0.4
            elif time_until_deadline < 259200:  # Less than 3 days
                urgency += 0.3
            elif time_until_deadline < 604800:  # Less than 1 week
                urgency += 0.2
            else:
                urgency += 0.1
        
        return min(urgency, 1.0)
    
    def get_importance_score(self) -> float:
        """Calculate importance based on reward and priority"""
        priority_map = {
            Priority.LOW: 0.25,
            Priority.MEDIUM: 0.5,
            Priority.HIGH: 0.75,
            Priority.CRITICAL: 1.0
        }
        
        # Combine priority (60%) and reward (40%)
        importance = (priority_map[self.priority] * 0.6) + (self.reward / 10.0 * 0.4)
        return min(importance, 1.0)
    
    def get_effort_score(self) -> float:
        """Normalize effort score to 0-1 range"""
        return self.effort / 10.0
    
    def get_wellbeing_impact(self) -> float:
        """Calculate well-being impact (higher reward and lower effort = better)"""
        # High reward and low effort = high wellbeing
        reward_factor = self.reward / 10.0
        effort_factor = 1.0 - (self.effort / 10.0)
        
        wellbeing = (reward_factor * 0.6) + (effort_factor * 0.4)
        return wellbeing
