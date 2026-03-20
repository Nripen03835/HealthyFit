def generate_bodyweight_plan(current_weight, target_weight, body_structure, fitness_level, health_issues):
    plan = {
        'warmup': ['Jumping jacks - 30 seconds', 'Arm circles - 30 seconds', 'Leg swings - 30 seconds'],
        'workout': [],
        'cooldown': ['Quad stretch - 30 seconds each leg', 'Hamstring stretch - 30 seconds', 'Chest stretch - 30 seconds'],
        'nutrition': {}
    }
    if fitness_level == 'beginner':
        plan['workout'] = [
            {'exercise': 'Push-ups', 'sets': 3, 'reps': '8-12'},
            {'exercise': 'Bodyweight squats', 'sets': 3, 'reps': '12-15'},
            {'exercise': 'Plank', 'sets': 3, 'reps': '30 seconds'},
            {'exercise': 'Lunges', 'sets': 3, 'reps': '10 each leg'}
        ]
    elif fitness_level == 'intermediate':
        plan['workout'] = [
            {'exercise': 'Push-ups', 'sets': 4, 'reps': '15-20'},
            {'exercise': 'Jump squats', 'sets': 3, 'reps': '12'},
            {'exercise': 'Mountain climbers', 'sets': 3, 'reps': '30 seconds'},
            {'exercise': 'Pike push-ups', 'sets': 3, 'reps': '8-10'},
            {'exercise': 'Glute bridges', 'sets': 3, 'reps': '15'}
        ]
    else:  # advanced
        plan['workout'] = [
            {'exercise': 'Archer push-ups', 'sets': 3, 'reps': '6-8 each side'},
            {'exercise': 'Pistol squats', 'sets': 3, 'reps': '5-8 each leg'},
            {'exercise': 'Dragon flags', 'sets': 3, 'reps': '6-8'},
            {'exercise': 'Handstand push-ups', 'sets': 3, 'reps': '5-8'},
            {'exercise': 'Bulgarian split squats', 'sets': 3, 'reps': '10 each leg'}
        ]
    
    cw = float(current_weight) if current_weight else 70.0
    tw = float(target_weight) if target_weight else 70.0

    if tw > cw:
        calorie_target = cw * 30 + 500
    elif tw < cw:
        calorie_target = cw * 30 - 500
    else:
        calorie_target = cw * 30
        
    plan['nutrition'] = {
        'calories': f'{calorie_target:.0f} kcal',
        'protein': f'{(calorie_target * 0.3 / 4):.0f} g',
        'carbs': f'{(calorie_target * 0.4 / 4):.0f} g',
        'fats': f'{(calorie_target * 0.3 / 9):.0f} g'
    }
    plan['weekly_schedule'] = ['Day 1: Full Body', 'Day 2: Rest', 'Day 3: Full Body', 'Day 4: Rest', 'Day 5: Full Body', 'Day 6: Rest', 'Day 7: Rest']
    
    ai_advice = "Stay consistent, hydrate, and maintain proper form to see the best results!"
    try:
        from bytez import Bytez
        key = "06bc1ac20911d68d0595ab58eff1e9c7"
        sdk = Bytez(key)
        model = sdk.model("AdityaLavaniya/TinyLlama-Fitness-Instructor")
        
        prompt = f"I am a {fitness_level} level fitness person. Weight: {current_weight}kg. Target: {target_weight}kg. Health issues: {health_issues or 'None'}. Provide a short, direct, motivational 1-sentence fitness tip."
        
        results = model.run([
          {
            "role": "user",
            "content": prompt
          }
        ])
        
        if not results.error:
            output = results.output
            if isinstance(output, list) and len(output) > 0:
                if isinstance(output[0], dict) and 'generated_text' in output[0]:
                    ai_advice = output[0]['generated_text']
                else:
                    ai_advice = str(output[0])
            else:
                ai_advice = str(output)
    except Exception as e:
        print("Bytez API error:", e)
        
    plan['ai_advice'] = ai_advice
    
    return plan
