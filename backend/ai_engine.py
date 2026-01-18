from backend.ml_model import predict_burnout_with_confidence

def generate_plan(data):
    sleep=data.sleep
    screen=data.screen
    study=data.study
    travel=data.travel

    score=100

    if sleep<5: score-=25
    elif sleep<7: score-=10

    if screen>8: score-=25
    elif screen>6: score-=15

    if study>8: score-=20
    elif study<3: score-=10

    travel_penalty={
        "Walking":0,
        "Bicycle":5,
        "Public Transport":10,
        "Two-wheeler":15,
        "Car":25
    }

    score-=travel_penalty.get(travel,10)
    score=max(0,min(score,100))

    if score>=75: level="High"
    elif score>=45: level="Moderate"
    else: level="Low"

    burnout,confidence,drivers=predict_burnout_with_confidence(
        sleep,screen,study
    )

    plan=[
        ["06:30–07:00","Wake Up","Use natural light"],
        ["09:00–15:00","Classes","Avoid idle screen usage"],
        ["16:00–17:00","Walk / Break","Mental refresh"],
        ["18:00–20:00","Study","Peak focus hours"],
        ["23:00–06:30","Sleep","Cognitive recovery"]
    ]

    tips=[]

    if sleep<6: tips.append("Increase sleep to improve focus and mental health.")
    if screen>7: tips.append("Reduce screen time to avoid digital fatigue.")
    if study>8: tips.append("Break study time into focused sessions.")
    if travel in ["Car","Two-wheeler"]:
        tips.append("Consider eco-friendly travel options.")

    return{
        "score":score,
        "level":level,
        "burnout":burnout,
        "burnout_confidence":round(confidence*100,1),
        "burnout_drivers":drivers,
        "plan":plan,
        "tips":tips
    }
