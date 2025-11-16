#!/usr/bin/env python3
"""
Unit tests for the AI-powered daily planning system.
"""
import unittest
from datetime import datetime, timedelta
from task_model import Task, Priority, EnergyLevel, TaskMode, Flexibility, TaskStatus
from prioritization import PrioritizationEngine
from energy_scheduling import EnergyScheduler, Chronotype
from llm_agent import LLMSchedulingAgent


class TestTaskModel(unittest.TestCase):
    """Test task metadata model"""
    
    def test_task_creation_with_all_fields(self):
        """Test creating a task with all 15 fields"""
        task = Task(
            title="Test Task",
            description="Test description",
            duration=60,
            priority=Priority.HIGH,
            deadline=datetime.now() + timedelta(days=1),
            dependencies=["task_1"],
            energy_level=EnergyLevel.HIGH,
            location="office",
            participants=["user1", "user2"],
            mode=TaskMode.SYNC,
            effort=7,
            flexibility=Flexibility.SEMI_FLEXIBLE,
            status=TaskStatus.NOT_STARTED,
            reward=8,
            tools=["laptop", "notebook"]
        )
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.duration, 60)
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.effort, 7)
        self.assertEqual(task.reward, 8)
        self.assertEqual(len(task.tools), 2)
    
    def test_task_urgency_score(self):
        """Test urgency score calculation"""
        # High priority task with near deadline
        task = Task(
            title="Urgent Task",
            duration=30,
            priority=Priority.CRITICAL,
            deadline=datetime.now() + timedelta(hours=12)
        )
        urgency = task.get_urgency_score()
        self.assertGreater(urgency, 0.7)  # Should be high urgency
        
        # Low priority task with distant deadline
        task2 = Task(
            title="Not Urgent",
            duration=30,
            priority=Priority.LOW,
            deadline=datetime.now() + timedelta(days=30)
        )
        urgency2 = task2.get_urgency_score()
        self.assertLess(urgency2, 0.5)  # Should be low urgency
    
    def test_task_importance_score(self):
        """Test importance score calculation"""
        task = Task(
            title="Important Task",
            duration=30,
            priority=Priority.HIGH,
            reward=9
        )
        importance = task.get_importance_score()
        self.assertGreater(importance, 0.6)
    
    def test_task_wellbeing_impact(self):
        """Test well-being impact calculation"""
        # High reward, low effort = high wellbeing
        task = Task(
            title="Easy Win",
            duration=30,
            effort=2,
            reward=9
        )
        wellbeing = task.get_wellbeing_impact()
        self.assertGreater(wellbeing, 0.7)
        
        # Low reward, high effort = low wellbeing
        task2 = Task(
            title="Hard Slog",
            duration=30,
            effort=9,
            reward=2
        )
        wellbeing2 = task2.get_wellbeing_impact()
        self.assertLess(wellbeing2, 0.4)


class TestPrioritizationEngine(unittest.TestCase):
    """Test multi-criteria prioritization engine"""
    
    def setUp(self):
        self.engine = PrioritizationEngine()
    
    def test_priority_score_calculation(self):
        """Test overall priority score calculation"""
        task = Task(
            title="Test Task",
            duration=60,
            priority=Priority.HIGH,
            deadline=datetime.now() + timedelta(days=1),
            effort=5,
            reward=7
        )
        score = self.engine.calculate_priority_score(task)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_prioritize_tasks_ordering(self):
        """Test that tasks are properly ordered by priority"""
        tasks = [
            Task(title="Low Priority", duration=30, priority=Priority.LOW, effort=5, reward=3),
            Task(title="High Priority", duration=30, priority=Priority.CRITICAL, 
                 deadline=datetime.now() + timedelta(hours=12), effort=3, reward=9),
            Task(title="Medium Priority", duration=30, priority=Priority.MEDIUM, effort=5, reward=5)
        ]
        
        prioritized = self.engine.prioritize_tasks(tasks)
        
        # First task should have highest score
        self.assertGreater(prioritized[0][1], prioritized[1][1])
        self.assertGreater(prioritized[1][1], prioritized[2][1])
        
        # High priority task should be first
        self.assertEqual(prioritized[0][0].title, "High Priority")
    
    def test_filter_by_energy_constraint(self):
        """Test filtering tasks by energy level"""
        tasks = [
            Task(title="High Energy Task", duration=30, energy_level=EnergyLevel.HIGH),
            Task(title="Medium Energy Task", duration=30, energy_level=EnergyLevel.MEDIUM),
            Task(title="Low Energy Task", duration=30, energy_level=EnergyLevel.LOW)
        ]
        
        # With low energy, should only get low energy tasks
        filtered = self.engine.filter_by_constraints(tasks, available_energy="low")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "Low Energy Task")
        
        # With high energy, should get all tasks
        filtered = self.engine.filter_by_constraints(tasks, available_energy="high")
        self.assertEqual(len(filtered), 3)
    
    def test_filter_by_duration_constraint(self):
        """Test filtering tasks by available duration"""
        tasks = [
            Task(title="Short Task", duration=30),
            Task(title="Medium Task", duration=60),
            Task(title="Long Task", duration=120)
        ]
        
        filtered = self.engine.filter_by_constraints(tasks, available_duration=60)
        self.assertEqual(len(filtered), 2)  # Only short and medium tasks
    
    def test_get_priority_breakdown(self):
        """Test getting detailed priority breakdown"""
        task = Task(
            title="Test Task",
            duration=60,
            priority=Priority.HIGH,
            effort=5,
            reward=7
        )
        
        breakdown = self.engine.get_priority_breakdown(task)
        
        self.assertIn("urgency", breakdown)
        self.assertIn("importance", breakdown)
        self.assertIn("effort", breakdown)
        self.assertIn("wellbeing", breakdown)
        self.assertIn("total_score", breakdown)


class TestEnergyScheduler(unittest.TestCase):
    """Test energy-aware scheduling system"""
    
    def test_chronotype_energy_curves(self):
        """Test that different chronotypes have different energy curves"""
        early_bird = EnergyScheduler(Chronotype.EARLY_BIRD)
        night_owl = EnergyScheduler(Chronotype.NIGHT_OWL)
        
        morning_time = datetime.now().replace(hour=8, minute=0)
        evening_time = datetime.now().replace(hour=20, minute=0)
        
        # Early bird should have high energy in morning
        self.assertEqual(early_bird.get_energy_level(morning_time), "high")
        # Night owl should have low energy in morning
        self.assertEqual(night_owl.get_energy_level(morning_time), "low")
        
        # Early bird should have low energy in evening
        self.assertEqual(early_bird.get_energy_level(evening_time), "low")
        # Night owl should have high energy in evening
        self.assertEqual(night_owl.get_energy_level(evening_time), "high")
    
    def test_find_optimal_time_slots(self):
        """Test finding optimal time slots for tasks"""
        scheduler = EnergyScheduler(Chronotype.EARLY_BIRD)
        
        task = Task(
            title="High Energy Task",
            duration=60,
            energy_level=EnergyLevel.HIGH
        )
        
        start = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        
        slots = scheduler.find_optimal_time_slots(task, start, end)
        
        # Should find some slots
        self.assertGreater(len(slots), 0)
        
        # Each slot should have start, end, and fitness
        for slot_start, slot_end, fitness in slots:
            self.assertIsInstance(slot_start, datetime)
            self.assertIsInstance(slot_end, datetime)
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertLessEqual(fitness, 1.0)
    
    def test_schedule_task_without_conflicts(self):
        """Test scheduling a task when no conflicts exist"""
        scheduler = EnergyScheduler(Chronotype.INTERMEDIATE)
        
        task = Task(
            title="Test Task",
            duration=60,
            energy_level=EnergyLevel.MEDIUM
        )
        
        start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=8)
        
        result = scheduler.schedule_task(task, start, end)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)  # Should return (start_time, end_time)
    
    def test_energy_report(self):
        """Test energy report generation"""
        scheduler = EnergyScheduler(Chronotype.INTERMEDIATE)
        report = scheduler.get_energy_report(datetime.now())
        
        self.assertIn("high", report)
        self.assertIn("medium", report)
        self.assertIn("low", report)
        
        # Should have some blocks for each level
        self.assertGreater(len(report["high"]), 0)


class TestLLMSchedulingAgent(unittest.TestCase):
    """Test LLM scheduling agent"""
    
    def setUp(self):
        self.agent = LLMSchedulingAgent(chronotype=Chronotype.INTERMEDIATE)
    
    def test_add_task(self):
        """Test adding tasks to agent"""
        task = Task(title="Test Task", duration=60)
        self.agent.add_task(task)
        
        self.assertEqual(len(self.agent.schedule), 1)
        self.assertIsNotNone(task.task_id)  # Should auto-generate ID
    
    def test_analyze_task_load(self):
        """Test task load analysis"""
        tasks = [
            Task(title="Task 1", duration=60, priority=Priority.HIGH, effort=7),
            Task(title="Task 2", duration=30, priority=Priority.LOW, effort=3),
            Task(title="Task 3", duration=90, priority=Priority.CRITICAL, effort=9,
                 deadline=datetime.now() - timedelta(days=1))  # Overdue
        ]
        
        for task in tasks:
            self.agent.add_task(task)
        
        analysis = self.agent.analyze_task_load()
        
        self.assertEqual(analysis["total_tasks"], 3)
        self.assertEqual(analysis["incomplete_tasks"], 3)
        self.assertEqual(analysis["total_duration_minutes"], 180)
        self.assertEqual(analysis["overdue_tasks"], 1)
    
    def test_generate_daily_plan(self):
        """Test daily plan generation"""
        tasks = [
            Task(title="Morning Task", duration=60, energy_level=EnergyLevel.HIGH),
            Task(title="Afternoon Task", duration=60, energy_level=EnergyLevel.MEDIUM),
            Task(title="Evening Task", duration=60, energy_level=EnergyLevel.LOW)
        ]
        
        for task in tasks:
            self.agent.add_task(task)
        
        plan = self.agent.generate_daily_plan(datetime.now())
        
        self.assertIn("date", plan)
        self.assertIn("schedule", plan)
        self.assertIn("scheduled_tasks", plan)
        self.assertIn("utilization", plan)
        self.assertGreater(len(plan["schedule"]), 0)
    
    def test_get_task_recommendations(self):
        """Test task recommendations"""
        tasks = [
            Task(title="Quick Task", duration=15, energy_level=EnergyLevel.LOW, effort=2),
            Task(title="Medium Task", duration=60, energy_level=EnergyLevel.MEDIUM, effort=5),
            Task(title="Long Task", duration=120, energy_level=EnergyLevel.HIGH, effort=8)
        ]
        
        for task in tasks:
            self.agent.add_task(task)
        
        recommendations = self.agent.get_task_recommendations(
            available_duration=60,
            energy_level="medium",
            top_n=3
        )
        
        # Should only get tasks that fit in 60 minutes with medium energy
        self.assertGreater(len(recommendations), 0)
        for rec in recommendations:
            self.assertLessEqual(rec["duration"], 60)
    
    def test_filter_by_dependencies(self):
        """Test dependency filtering"""
        task1 = Task(title="Task 1", duration=30, task_id="task1", status=TaskStatus.COMPLETED)
        task2 = Task(title="Task 2", duration=30, task_id="task2", dependencies=["task1"])
        task3 = Task(title="Task 3", duration=30, task_id="task3", dependencies=["task_not_exist"])
        
        self.agent.add_task(task1)
        self.agent.add_task(task2)
        self.agent.add_task(task3)
        
        schedulable = self.agent._filter_by_dependencies([task2, task3])
        
        # Task 2 should be schedulable (dependency met)
        # Task 3 should not be schedulable (dependency not met)
        self.assertEqual(len(schedulable), 1)
        self.assertEqual(schedulable[0].title, "Task 2")
    
    def test_export_schedule_json(self):
        """Test JSON export"""
        task = Task(title="Test Task", duration=60)
        self.agent.add_task(task)
        
        json_output = self.agent.export_schedule(format="json")
        
        self.assertIsInstance(json_output, str)
        self.assertIn("Test Task", json_output)
    
    def test_export_schedule_text(self):
        """Test text export"""
        task = Task(title="Test Task", duration=60)
        self.agent.add_task(task)
        
        text_output = self.agent.export_schedule(format="text")
        
        self.assertIsInstance(text_output, str)
        self.assertIn("Test Task", text_output)
        self.assertIn("Task Schedule", text_output)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_scheduling_workflow(self):
        """Test complete workflow from task creation to scheduling"""
        # 1. Create agent
        agent = LLMSchedulingAgent(chronotype=Chronotype.EARLY_BIRD)
        
        # 2. Add tasks with various priorities and energy levels
        tasks = [
            Task(
                title="Critical Project",
                duration=120,
                priority=Priority.CRITICAL,
                deadline=datetime.now() + timedelta(days=1),
                energy_level=EnergyLevel.HIGH,
                effort=9,
                reward=10
            ),
            Task(
                title="Team Meeting",
                duration=30,
                priority=Priority.MEDIUM,
                energy_level=EnergyLevel.MEDIUM,
                effort=3,
                reward=5
            ),
            Task(
                title="Email Cleanup",
                duration=30,
                priority=Priority.LOW,
                energy_level=EnergyLevel.LOW,
                effort=2,
                reward=3
            )
        ]
        
        for task in tasks:
            agent.add_task(task)
        
        # 3. Generate daily plan
        plan = agent.generate_daily_plan(datetime.now())
        
        # 4. Verify plan structure
        self.assertGreater(plan["scheduled_tasks"], 0)
        self.assertIn("schedule", plan)
        
        # 5. Verify high priority task is scheduled
        scheduled_titles = [task["title"] for task in plan["schedule"]]
        self.assertIn("Critical Project", scheduled_titles)
        
        # 6. Get recommendations
        recommendations = agent.get_task_recommendations(
            available_duration=60,
            energy_level="high",
            top_n=2
        )
        
        # 7. Verify recommendations
        self.assertGreater(len(recommendations), 0)
        
        # 8. Analyze task load
        analysis = agent.analyze_task_load()
        self.assertEqual(analysis["total_tasks"], 3)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTaskModel))
    suite.addTests(loader.loadTestsFromTestCase(TestPrioritizationEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEnergyScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMSchedulingAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
