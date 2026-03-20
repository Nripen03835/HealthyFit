from app import app, db
from models import Medicine, Exercise

def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if empty
        if Medicine.query.count() == 0:
            meds = [
                Medicine(name='Paracetamol', uses='Fever, mild pain', dosage='500mg every 4-6 hours', side_effects='Nausea, rash', precautions='Avoid alcohol'),
                Medicine(name='Ibuprofen', uses='Inflammation, pain', dosage='200-400mg every 6 hours', side_effects='Stomach upset', precautions='Take with food'),
                Medicine(name='Amoxicillin', uses='Bacterial infections', dosage='500mg every 8 hours', side_effects='Diarrhea, nausea', precautions='Finish full course'),
                Medicine(name='Cetirizine', uses='Allergies', dosage='10mg once daily', side_effects='Drowsiness, dry mouth', precautions='May cause sleepiness'),
            ]
            db.session.bulk_save_objects(meds)
            
        if Exercise.query.count() == 0:
            exercises = [
                Exercise(name='Barbell Bench Press', muscle_group='Chest', equipment='Barbell', description='Lie on bench, lower bar to chest, press up', sets_reps='3x10', posture_tips='Keep shoulders back, feet flat', image_url='', threeD_model_path=''),
                Exercise(name='Push-ups', muscle_group='Chest', equipment='Bodyweight', description='Standard push-ups', sets_reps='3x15', posture_tips='Keep body straight, engage core', image_url='', threeD_model_path=''),
                Exercise(name='Pull-ups', muscle_group='Back', equipment='Pull-up bar', description='Hang and pull up until chin is over bar', sets_reps='3x8', posture_tips='Engage lats, avoid swinging', image_url='', threeD_model_path=''),
                Exercise(name='Barbell Squat', muscle_group='Legs', equipment='Barbell', description='Squat with barbell on upper back', sets_reps='3x12', posture_tips='Keep chest up, knees track over toes', image_url='', threeD_model_path=''),
                Exercise(name='Dumbbell Shoulder Press', muscle_group='Shoulders', equipment='Dumbbell', description='Press dumbbells overhead seated or standing', sets_reps='3x10', posture_tips='Don\'t arch lower back excessively', image_url='', threeD_model_path=''),
                Exercise(name='Bicep Curls', muscle_group='Arms', equipment='Dumbbell', description='Curl dumbbells towards shoulders', sets_reps='3x12', posture_tips='Keep elbows stationary', image_url='', threeD_model_path=''),
            ]
            db.session.bulk_save_objects(exercises)
            
        db.session.commit()
        print("Database initialized with sample data.")

if __name__ == '__main__':
    init_db()
