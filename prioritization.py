"""
Multi-criteria prioritization engine using urgency, importance, effort, and well-being.
"""
from typing import List, Dict, Tuple
from task_model import Task


class PrioritizationEngine:
    """
    Multi-criteria decision engine for task prioritization.
    Uses weighted scoring across four dimensions:
    - Urgency (how soon it needs to be done)
    - Importance (how valuable it is)
    - Effort (how much energy/work required)
    - Well-being (impact on personal satisfaction)
    """
    
    def __init__(
        self,
        urgency_weight: float = 0.3,
        importance_weight: float = 0.35,
        effort_weight: float = 0.15,
        wellbeing_weight: float = 0.2
    ):
        """
        Initialize prioritization engine with configurable weights.
        
        Args:
            urgency_weight: Weight for urgency criterion (default 0.3)
            importance_weight: Weight for importance criterion (default 0.35)
            effort_weight: Weight for effort criterion (default 0.15)
            wellbeing_weight: Weight for well-being criterion (default 0.2)
        """
        # Normalize weights to sum to 1.0
        total = urgency_weight + importance_weight + effort_weight + wellbeing_weight
        self.urgency_weight = urgency_weight / total
        self.importance_weight = importance_weight / total
        self.effort_weight = effort_weight / total
        self.wellbeing_weight = wellbeing_weight / total
    
    def calculate_priority_score(self, task: Task) -> float:
        """
        Calculate overall priority score for a task.
        
        Args:
            task: Task to evaluate
            
        Returns:
            Priority score between 0 and 1 (higher = more priority)
        """
        urgency = task.get_urgency_score()
        importance = task.get_importance_score()
        effort = task.get_effort_score()
        wellbeing = task.get_wellbeing_impact()
        
        # For effort, inverse it (lower effort = higher priority)
        effort_factor = 1.0 - effort
        
        # Weighted sum
        priority_score = (
            urgency * self.urgency_weight +
            importance * self.importance_weight +
            effort_factor * self.effort_weight +
            wellbeing * self.wellbeing_weight
        )
        
        return priority_score
    
    def get_priority_breakdown(self, task: Task) -> Dict[str, float]:
        """
        Get detailed breakdown of priority components.
        
        Args:
            task: Task to evaluate
            
        Returns:
            Dictionary with individual scores and weights
        """
        urgency = task.get_urgency_score()
        importance = task.get_importance_score()
        effort = task.get_effort_score()
        wellbeing = task.get_wellbeing_impact()
        
        return {
            "urgency": urgency,
            "urgency_weighted": urgency * self.urgency_weight,
            "importance": importance,
            "importance_weighted": importance * self.importance_weight,
            "effort": effort,
            "effort_weighted": (1.0 - effort) * self.effort_weight,
            "wellbeing": wellbeing,
            "wellbeing_weighted": wellbeing * self.wellbeing_weight,
            "total_score": self.calculate_priority_score(task)
        }
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Tuple[Task, float]]:
        """
        Sort tasks by priority score (highest first).
        
        Args:
            tasks: List of tasks to prioritize
            
        Returns:
            List of (task, priority_score) tuples sorted by priority
        """
        task_scores = []
        for task in tasks:
            score = self.calculate_priority_score(task)
            task_scores.append((task, score))
        
        # Sort by score descending
        task_scores.sort(key=lambda x: x[1], reverse=True)
        
        return task_scores
    
    def filter_by_constraints(
        self,
        tasks: List[Task],
        available_energy: str = None,
        available_location: str = None,
        available_duration: int = None
    ) -> List[Task]:
        """
        Filter tasks based on current constraints.
        
        Args:
            tasks: List of tasks to filter
            available_energy: Current energy level (low/medium/high)
            available_location: Current location
            available_duration: Available time in minutes
            
        Returns:
            Filtered list of tasks matching constraints
        """
        filtered = tasks
        
        if available_energy:
            # Filter by energy level
            energy_hierarchy = {"low": 0, "medium": 1, "high": 2}
            current_level = energy_hierarchy.get(available_energy, 2)
            filtered = [
                t for t in filtered
                if energy_hierarchy.get(
                    t.energy_level if isinstance(t.energy_level, str) else t.energy_level.value, 
                    0
                ) <= current_level
            ]
        
        if available_location:
            # Filter by location (include tasks with no location or matching location)
            filtered = [
                t for t in filtered
                if t.location is None or t.location == available_location
            ]
        
        if available_duration:
            # Filter by duration
            filtered = [
                t for t in filtered
                if t.duration <= available_duration
            ]
        
        return filtered
    
    def recommend_next_task(
        self,
        tasks: List[Task],
        available_energy: str = None,
        available_location: str = None,
        available_duration: int = None,
        top_n: int = 3
    ) -> List[Tuple[Task, float, Dict[str, float]]]:
        """
        Recommend top N tasks based on priority and constraints.
        
        Args:
            tasks: List of tasks to consider
            available_energy: Current energy level
            available_location: Current location
            available_duration: Available time in minutes
            top_n: Number of recommendations to return
            
        Returns:
            List of (task, score, breakdown) tuples
        """
        # Filter by constraints
        eligible_tasks = self.filter_by_constraints(
            tasks, available_energy, available_location, available_duration
        )
        
        # Prioritize
        prioritized = self.prioritize_tasks(eligible_tasks)
        
        # Get top N with breakdowns
        recommendations = []
        for task, score in prioritized[:top_n]:
            breakdown = self.get_priority_breakdown(task)
            recommendations.append((task, score, breakdown))
        
        return recommendations
