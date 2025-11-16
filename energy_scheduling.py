"""
Energy-aware scheduling system aligned with user chronotypes.
"""
from datetime import datetime, time, timedelta
from typing import List, Optional, Dict, Tuple
from enum import Enum
from task_model import Task, EnergyLevel


class Chronotype(str, Enum):
    """User chronotype (circadian rhythm preference)"""
    EARLY_BIRD = "early_bird"  # Morning person
    INTERMEDIATE = "intermediate"  # Neutral
    NIGHT_OWL = "night_owl"  # Evening person


class EnergyScheduler:
    """
    Energy-aware task scheduler that aligns task energy requirements
    with user's natural energy patterns based on chronotype.
    """
    
    def __init__(self, chronotype: Chronotype = Chronotype.INTERMEDIATE):
        """
        Initialize energy scheduler with user's chronotype.
        
        Args:
            chronotype: User's chronotype preference
        """
        self.chronotype = chronotype
        self.energy_curve = self._build_energy_curve()
    
    def _build_energy_curve(self) -> Dict[int, str]:
        """
        Build energy curve for the day based on chronotype.
        Returns mapping of hour (0-23) to energy level.
        """
        if self.chronotype == Chronotype.EARLY_BIRD:
            # Peak energy 6am-12pm
            return {
                0: "low", 1: "low", 2: "low", 3: "low", 4: "low", 5: "medium",
                6: "high", 7: "high", 8: "high", 9: "high", 10: "high", 11: "high",
                12: "medium", 13: "medium", 14: "medium", 15: "medium",
                16: "medium", 17: "medium", 18: "low", 19: "low",
                20: "low", 21: "low", 22: "low", 23: "low"
            }
        elif self.chronotype == Chronotype.NIGHT_OWL:
            # Peak energy 2pm-10pm
            return {
                0: "medium", 1: "medium", 2: "low", 3: "low", 4: "low", 5: "low",
                6: "low", 7: "low", 8: "low", 9: "medium", 10: "medium",
                11: "medium", 12: "medium", 13: "medium", 14: "high",
                15: "high", 16: "high", 17: "high", 18: "high", 19: "high",
                20: "high", 21: "medium", 22: "medium", 23: "medium"
            }
        else:  # INTERMEDIATE
            # Peak energy 9am-5pm
            return {
                0: "low", 1: "low", 2: "low", 3: "low", 4: "low", 5: "low",
                6: "medium", 7: "medium", 8: "medium", 9: "high", 10: "high",
                11: "high", 12: "high", 13: "high", 14: "high", 15: "high",
                16: "high", 17: "medium", 18: "medium", 19: "medium",
                20: "low", 21: "low", 22: "low", 23: "low"
            }
    
    def get_energy_level(self, dt: datetime) -> str:
        """
        Get energy level at specific time based on chronotype.
        
        Args:
            dt: Datetime to check
            
        Returns:
            Energy level string (low/medium/high)
        """
        return self.energy_curve[dt.hour]
    
    def find_optimal_time_slots(
        self,
        task: Task,
        start_date: datetime,
        end_date: datetime,
        working_hours_start: time = time(8, 0),
        working_hours_end: time = time(18, 0)
    ) -> List[Tuple[datetime, datetime, float]]:
        """
        Find optimal time slots for a task based on energy requirements.
        
        Args:
            task: Task to schedule
            start_date: Start of search window
            end_date: End of search window
            working_hours_start: Start of working day
            working_hours_end: End of working day
            
        Returns:
            List of (start_time, end_time, fitness_score) tuples sorted by fitness
        """
        slots = []
        current = start_date.replace(
            hour=working_hours_start.hour,
            minute=working_hours_start.minute,
            second=0,
            microsecond=0
        )
        
        # If start_date is after working hours, move to next day
        if current.time() > working_hours_end:
            current = current + timedelta(days=1)
            current = current.replace(
                hour=working_hours_start.hour,
                minute=working_hours_start.minute
            )
        
        while current < end_date:
            # Check if within working hours
            if working_hours_start <= current.time() < working_hours_end:
                slot_end = current + timedelta(minutes=task.duration)
                
                # Ensure slot doesn't exceed working hours
                working_end = current.replace(
                    hour=working_hours_end.hour,
                    minute=working_hours_end.minute
                )
                
                if slot_end <= working_end:
                    # Calculate fitness score
                    fitness = self._calculate_slot_fitness(task, current, slot_end)
                    slots.append((current, slot_end, fitness))
                
                # Move to next potential slot (30-minute intervals)
                current = current + timedelta(minutes=30)
            else:
                # Move to next day's working hours
                current = current + timedelta(days=1)
                current = current.replace(
                    hour=working_hours_start.hour,
                    minute=working_hours_start.minute
                )
        
        # Sort by fitness score (descending)
        slots.sort(key=lambda x: x[2], reverse=True)
        
        return slots
    
    def _calculate_slot_fitness(
        self,
        task: Task,
        slot_start: datetime,
        slot_end: datetime
    ) -> float:
        """
        Calculate how well a time slot matches task energy requirements.
        
        Args:
            task: Task to evaluate
            slot_start: Slot start time
            slot_end: Slot end time
            
        Returns:
            Fitness score (0-1, higher is better)
        """
        energy_map = {"low": 1, "medium": 2, "high": 3}
        # Handle both string and enum values
        energy_level_str = task.energy_level if isinstance(task.energy_level, str) else task.energy_level.value
        task_energy_req = energy_map[energy_level_str]
        
        # Sample energy levels throughout the slot
        samples = 5
        duration = (slot_end - slot_start).total_seconds() / 60  # minutes
        interval = duration / samples
        
        total_fitness = 0.0
        for i in range(samples):
            sample_time = slot_start + timedelta(minutes=i * interval)
            slot_energy = energy_map[self.get_energy_level(sample_time)]
            
            # Calculate match (prefer higher energy for high-energy tasks)
            if slot_energy >= task_energy_req:
                # Perfect match or higher energy available
                match_score = 1.0
            else:
                # Lower energy than required - penalize
                match_score = slot_energy / task_energy_req * 0.5
            
            total_fitness += match_score
        
        avg_fitness = total_fitness / samples
        
        # Bonus for flexibility
        flexibility_str = task.flexibility if isinstance(task.flexibility, str) else task.flexibility.value
        if flexibility_str == "flexible":
            avg_fitness *= 1.0  # No change
        elif flexibility_str == "semi_flexible":
            avg_fitness *= 0.95
        else:  # rigid
            avg_fitness *= 0.9
        
        return min(avg_fitness, 1.0)
    
    def schedule_task(
        self,
        task: Task,
        start_date: datetime,
        end_date: datetime,
        existing_schedule: List[Task] = None,
        working_hours_start: time = time(8, 0),
        working_hours_end: time = time(18, 0)
    ) -> Optional[Tuple[datetime, datetime]]:
        """
        Schedule a task in the optimal time slot considering energy and existing schedule.
        
        Args:
            task: Task to schedule
            start_date: Start of scheduling window
            end_date: End of scheduling window
            existing_schedule: Already scheduled tasks
            working_hours_start: Start of working day
            working_hours_end: End of working day
            
        Returns:
            (start_time, end_time) tuple or None if no slot found
        """
        if existing_schedule is None:
            existing_schedule = []
        
        # Find optimal slots
        optimal_slots = self.find_optimal_time_slots(
            task, start_date, end_date, working_hours_start, working_hours_end
        )
        
        # Find first slot that doesn't conflict with existing schedule
        for slot_start, slot_end, fitness in optimal_slots:
            has_conflict = False
            
            for scheduled_task in existing_schedule:
                if scheduled_task.scheduled_start and scheduled_task.scheduled_end:
                    # Check for overlap
                    if not (slot_end <= scheduled_task.scheduled_start or
                            slot_start >= scheduled_task.scheduled_end):
                        has_conflict = True
                        break
            
            if not has_conflict:
                return (slot_start, slot_end)
        
        return None
    
    def get_energy_report(self, date: datetime) -> Dict[str, List[Tuple[str, str]]]:
        """
        Get energy level report for a specific day.
        
        Args:
            date: Date to get report for
            
        Returns:
            Dictionary with energy blocks: {level: [(start, end), ...]}
        """
        report = {"high": [], "medium": [], "low": []}
        
        current_level = None
        block_start = None
        
        for hour in range(24):
            level = self.energy_curve[hour]
            
            if level != current_level:
                # Save previous block
                if current_level is not None and block_start is not None:
                    report[current_level].append(
                        (f"{block_start:02d}:00", f"{hour:02d}:00")
                    )
                
                # Start new block
                current_level = level
                block_start = hour
        
        # Close last block
        if current_level is not None and block_start is not None:
            report[current_level].append(
                (f"{block_start:02d}:00", "24:00")
            )
        
        return report
