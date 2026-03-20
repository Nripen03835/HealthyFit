from models import Exercise
import random

def generate_gym_plan(current_weight, target_weight, body_structure, target_muscles, days_per_week, exercises_per_day=3):
    if not target_muscles:
        target_muscles = ['Chest', 'Back', 'Legs', 'Shoulders', 'Arms']
        
    exercises = Exercise.query.filter(Exercise.muscle_group.in_(target_muscles)).all()
    muscle_exercises = {}
    for ex in exercises:
        muscle_exercises.setdefault(ex.muscle_group, []).append(ex)
        
    days = int(days_per_week)
    ex_count = int(exercises_per_day)
    plan = {'days': []}
    
    # "Every day should consist of different muscle workout"
    # Ensure there are enough unique muscles, or loop them uniquely per day
    muscle_cycle = target_muscles * (days // len(target_muscles) + 1)
    
    for i in range(days):
        muscle = muscle_cycle[i]
        available = muscle_exercises.get(muscle, [])
        # Provide multiple variations
        day_exercises = random.sample(available, min(ex_count, len(available))) if available else []
        plan['days'].append({
            'day': f'Day {i+1}',
            'focus': muscle,
            'exercises': [{'name': ex.name, 'sets_reps': ex.sets_reps, 'tips': ex.posture_tips, 'id': ex.id} for ex in day_exercises]
        })
    return plan

def calculate_water_intake(weight_kg, activity_level='moderate'):
    w = float(weight_kg) if weight_kg else 70.0
    factors = {'low': 1.0, 'moderate': 1.2, 'high': 1.5}
    factor = factors.get(activity_level, 1.2)
    liters = w * 0.033 * factor
    return f"{liters:.1f} liters per day"
