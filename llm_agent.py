"""
LLM Agent for intelligent task scheduling and planning.
"""
import json
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from task_model import Task, Priority, EnergyLevel, TaskMode, Flexibility, TaskStatus
from prioritization import PrioritizationEngine
from energy_scheduling import EnergyScheduler, Chronotype


def _get_enum_value(value):
    """Helper to get string value from enum or string"""
    return value if isinstance(value, str) else value.value


class LLMSchedulingAgent:
    """
    AI-powered scheduling agent that uses rule-based intelligence
    and structured reasoning for task planning and timeboxing.
    """
    
    def __init__(
        self,
        chronotype: Chronotype = Chronotype.INTERMEDIATE,
        prioritization_engine: Optional[PrioritizationEngine] = None,
        energy_scheduler: Optional[EnergyScheduler] = None
    ):
        """
        Initialize LLM scheduling agent.
        
        Args:
            chronotype: User's chronotype preference
            prioritization_engine: Custom prioritization engine (optional)
            energy_scheduler: Custom energy scheduler (optional)
        """
        self.chronotype = chronotype
        self.prioritization_engine = prioritization_engine or PrioritizationEngine()
        self.energy_scheduler = energy_scheduler or EnergyScheduler(chronotype)
        self.schedule: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task to the agent's task list"""
        if task.task_id is None:
            task.task_id = f"task_{len(self.schedule)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.schedule.append(task)
    
    def analyze_task_load(self) -> Dict[str, Any]:
        """
        Analyze the current task load and provide insights.
        
        Returns:
            Dictionary with task load analytics
        """
        total_tasks = len(self.schedule)
        incomplete_tasks = [t for t in self.schedule if t.status != TaskStatus.COMPLETED]
        
        total_duration = sum(t.duration for t in incomplete_tasks)
        total_effort = sum(t.effort for t in incomplete_tasks)
        
        # Energy distribution
        energy_dist = {
            "high": len([t for t in incomplete_tasks if t.energy_level == EnergyLevel.HIGH]),
            "medium": len([t for t in incomplete_tasks if t.energy_level == EnergyLevel.MEDIUM]),
            "low": len([t for t in incomplete_tasks if t.energy_level == EnergyLevel.LOW])
        }
        
        # Priority distribution
        priority_dist = {
            "critical": len([t for t in incomplete_tasks if t.priority == Priority.CRITICAL]),
            "high": len([t for t in incomplete_tasks if t.priority == Priority.HIGH]),
            "medium": len([t for t in incomplete_tasks if t.priority == Priority.MEDIUM]),
            "low": len([t for t in incomplete_tasks if t.priority == Priority.LOW])
        }
        
        # Overdue tasks
        now = datetime.now()
        overdue = [t for t in incomplete_tasks if t.deadline and t.deadline < now]
        
        return {
            "total_tasks": total_tasks,
            "incomplete_tasks": len(incomplete_tasks),
            "completed_tasks": total_tasks - len(incomplete_tasks),
            "total_duration_minutes": total_duration,
            "total_duration_hours": total_duration / 60,
            "average_effort": total_effort / len(incomplete_tasks) if incomplete_tasks else 0,
            "energy_distribution": energy_dist,
            "priority_distribution": priority_dist,
            "overdue_tasks": len(overdue),
            "overdue_task_titles": [t.title for t in overdue]
        }
    
    def generate_daily_plan(
        self,
        date: datetime,
        working_hours_start: int = 8,
        working_hours_end: int = 18,
        break_duration: int = 60,
        max_tasks: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate an optimized daily plan using AI-powered scheduling.
        
        Args:
            date: Date to plan for
            working_hours_start: Start hour (24-hour format)
            working_hours_end: End hour (24-hour format)
            break_duration: Break time in minutes
            max_tasks: Maximum tasks to schedule (optional)
            
        Returns:
            Dictionary with daily plan and reasoning
        """
        from datetime import time
        
        # Get incomplete tasks
        incomplete_tasks = [
            t for t in self.schedule
            if t.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
        ]
        
        # Filter by dependencies
        schedulable_tasks = self._filter_by_dependencies(incomplete_tasks)
        
        # Prioritize tasks
        prioritized = self.prioritization_engine.prioritize_tasks(schedulable_tasks)
        
        # Calculate available time
        available_minutes = (working_hours_end - working_hours_start) * 60 - break_duration
        
        # Select tasks that fit in the day
        selected_tasks = []
        total_scheduled_time = 0
        
        for task, priority_score in prioritized:
            if max_tasks and len(selected_tasks) >= max_tasks:
                break
            
            if total_scheduled_time + task.duration <= available_minutes:
                selected_tasks.append((task, priority_score))
                total_scheduled_time += task.duration
            
            if total_scheduled_time >= available_minutes:
                break
        
        # Schedule tasks in optimal time slots
        scheduled_plan = []
        scheduled_task_objects = []
        
        start_datetime = date.replace(hour=working_hours_start, minute=0, second=0, microsecond=0)
        end_datetime = date.replace(hour=working_hours_end, minute=0, second=0, microsecond=0)
        
        for task, priority_score in selected_tasks:
            slot = self.energy_scheduler.schedule_task(
                task,
                start_datetime,
                end_datetime,
                scheduled_task_objects,
                time(working_hours_start, 0),
                time(working_hours_end, 0)
            )
            
            if slot:
                task.scheduled_start = slot[0]
                task.scheduled_end = slot[1]
                scheduled_task_objects.append(task)
                
                # Get priority breakdown
                breakdown = self.prioritization_engine.get_priority_breakdown(task)
                
                scheduled_plan.append({
                    "task_id": task.task_id,
                    "title": task.title,
                    "start_time": slot[0].strftime("%H:%M"),
                    "end_time": slot[1].strftime("%H:%M"),
                    "duration": task.duration,
                    "priority_score": priority_score,
                    "energy_level": _get_enum_value(task.energy_level),
                    "priority": _get_enum_value(task.priority),
                    "reasoning": self._generate_scheduling_reasoning(task, breakdown)
                })
        
        # Get energy report
        energy_report = self.energy_scheduler.get_energy_report(date)
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "chronotype": _get_enum_value(self.chronotype),
            "working_hours": f"{working_hours_start:02d}:00 - {working_hours_end:02d}:00",
            "available_minutes": available_minutes,
            "scheduled_minutes": total_scheduled_time,
            "utilization": f"{(total_scheduled_time / available_minutes * 100):.1f}%",
            "scheduled_tasks": len(scheduled_plan),
            "energy_blocks": energy_report,
            "schedule": scheduled_plan,
            "unscheduled_tasks": len(incomplete_tasks) - len(scheduled_plan)
        }
    
    def _filter_by_dependencies(self, tasks: List[Task]) -> List[Task]:
        """
        Filter tasks to only include those whose dependencies are met.
        
        Args:
            tasks: List of tasks to filter
            
        Returns:
            List of tasks with met dependencies
        """
        completed_task_ids = {
            t.task_id for t in self.schedule
            if t.status == TaskStatus.COMPLETED
        }
        
        schedulable = []
        for task in tasks:
            dependencies_met = all(
                dep_id in completed_task_ids
                for dep_id in task.dependencies
            )
            if dependencies_met:
                schedulable.append(task)
        
        return schedulable
    
    def _generate_scheduling_reasoning(
        self,
        task: Task,
        breakdown: Dict[str, float]
    ) -> str:
        """
        Generate human-readable reasoning for why a task was scheduled.
        
        Args:
            task: Scheduled task
            breakdown: Priority breakdown
            
        Returns:
            Reasoning string
        """
        reasons = []
        
        # Priority reasoning
        if breakdown["urgency"] > 0.7:
            reasons.append("high urgency")
        if breakdown["importance"] > 0.7:
            reasons.append("high importance")
        if breakdown["wellbeing"] > 0.7:
            reasons.append("positive wellbeing impact")
        if task.effort <= 3:
            reasons.append("low effort required")
        
        # Energy alignment
        energy_time = ""
        if task.energy_level == EnergyLevel.HIGH:
            energy_time = "during peak energy hours"
        elif task.energy_level == EnergyLevel.MEDIUM:
            energy_time = "during moderate energy hours"
        else:
            energy_time = "during low-energy hours"
        
        if reasons:
            return f"Scheduled due to {', '.join(reasons)} {energy_time}"
        else:
            return f"Scheduled {energy_time} based on energy requirements"
    
    def get_task_recommendations(
        self,
        available_duration: int,
        energy_level: str = "medium",
        location: Optional[str] = None,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get AI-powered task recommendations based on current context.
        
        Args:
            available_duration: Available time in minutes
            energy_level: Current energy level (low/medium/high)
            location: Current location (optional)
            top_n: Number of recommendations
            
        Returns:
            List of recommended tasks with reasoning
        """
        incomplete_tasks = [
            t for t in self.schedule
            if t.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
        ]
        
        # Filter by dependencies
        schedulable_tasks = self._filter_by_dependencies(incomplete_tasks)
        
        # Get recommendations
        recommendations = self.prioritization_engine.recommend_next_task(
            schedulable_tasks,
            available_energy=energy_level,
            available_location=location,
            available_duration=available_duration,
            top_n=top_n
        )
        
        result = []
        for task, score, breakdown in recommendations:
            result.append({
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "duration": task.duration,
                "priority_score": score,
                "energy_level": _get_enum_value(task.energy_level),
                "priority": _get_enum_value(task.priority),
                "effort": task.effort,
                "reward": task.reward,
                "breakdown": breakdown,
                "reasoning": self._generate_scheduling_reasoning(task, breakdown)
            })
        
        return result
    
    def replan_on_interruption(
        self,
        current_time: datetime,
        interrupted_task_id: str,
        remaining_duration: int
    ) -> Dict[str, Any]:
        """
        Dynamically replan when a task is interrupted.
        
        Args:
            current_time: Time of interruption
            interrupted_task_id: ID of interrupted task
            remaining_duration: Remaining duration for interrupted task
            
        Returns:
            New plan starting from current time
        """
        # Find interrupted task
        interrupted_task = None
        for task in self.schedule:
            if task.task_id == interrupted_task_id:
                interrupted_task = task
                break
        
        if not interrupted_task:
            return {"error": "Task not found"}
        
        # Create new task for remaining work
        remaining_task = Task(
            title=f"{interrupted_task.title} (continued)",
            description=interrupted_task.description,
            duration=remaining_duration,
            priority=interrupted_task.priority,
            deadline=interrupted_task.deadline,
            dependencies=interrupted_task.dependencies,
            energy_level=interrupted_task.energy_level,
            location=interrupted_task.location,
            participants=interrupted_task.participants,
            mode=interrupted_task.mode,
            effort=interrupted_task.effort,
            flexibility=interrupted_task.flexibility,
            status=TaskStatus.IN_PROGRESS,
            reward=interrupted_task.reward,
            tools=interrupted_task.tools,
            task_id=f"{interrupted_task_id}_continued"
        )
        
        # Add to schedule
        self.add_task(remaining_task)
        
        # Generate new plan for rest of day
        return self.generate_daily_plan(current_time, current_time.hour, 18)
    
    def export_schedule(self, format: str = "json") -> str:
        """
        Export schedule in specified format.
        
        Args:
            format: Export format (json, text)
            
        Returns:
            Formatted schedule string
        """
        if format == "json":
            return json.dumps(
                [task.to_dict() for task in self.schedule],
                indent=2,
                default=str
            )
        else:  # text
            output = "Task Schedule\n" + "="*50 + "\n\n"
            for task in self.schedule:
                output += f"[{_get_enum_value(task.status).upper()}] {task.title}\n"
                output += f"  Duration: {task.duration} min | Priority: {_get_enum_value(task.priority)}\n"
                output += f"  Energy: {_get_enum_value(task.energy_level)} | Effort: {task.effort}/10\n"
                if task.scheduled_start:
                    output += f"  Scheduled: {task.scheduled_start.strftime('%Y-%m-%d %H:%M')}\n"
                output += "\n"
            return output
