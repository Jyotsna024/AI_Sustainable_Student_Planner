def analyze_schedule(classes,study,screen,sleep,travel):
    score=100
    feedback=[]

    if sleep<7:
        score-=15
        feedback.append("Increase sleep to improve focus and mental health.")

    if screen>7:
        score-=15
        feedback.append("Reduce screen time to save energy and reduce eye strain.")

    if study>5:
        feedback.append("Good dedication! Consider short breaks to avoid burnout.")

    if travel in ["Car","Two-wheeler"]:
        score-=10
        feedback.append("Switching to public transport or cycling can reduce carbon footprint.")

    if travel=="Bicycle" or travel=="Walking":
        feedback.append("Great choice! Eco-friendly and healthy travel method.")

    sustainability_level="High" if score>75 else "Moderate" if score>50 else "Low"

    return {
        "Sustainability Score":f"{score}/100",
        "Level":sustainability_level,
        "AI Insights":feedback
    }
