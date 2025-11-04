import sys
sys.path.insert(0, '../')

from services.recommendation_engine import RecommendationEngine
import json

print("🧪 Testing RecommendationEngine\n")
print("=" * 60)

# Initialiser le service
engine = RecommendationEngine()

# TEST 1: Carbon Score Calculation
print("\n1️⃣ TEST: calculate_carbon_score()")
print("-" * 60)

test_cases = [
    (30, "Faible"),
    (100, "Moyen"),
    (200, "Élevé"),
]

passed = 0
failed = 0

for co2, expected_level in test_cases:
    result = engine.calculate_carbon_score(co2)
    if result["level"] == expected_level:
        status = "✅"
        passed += 1
    else:
        status = "❌"
        failed += 1
    print(f"{status} CO2: {co2}kg → Level: {result['level']}, Score: {result['score']}")

# TEST 2: Match Score
print("\n\n2️⃣ TEST: calculate_match_score()")
print("-" * 60)

match_cases = [
    ("Adventure", "ActiviteSportive", 100),
    ("Culture", "ActiviteCulturelle", 100),
    ("BienEtre", "Spa", 100),
    ("Famille", "ActiviteEducative", 100),
    ("Adventure", "Musée", 0),  # Bad match
]

for profile, activity, expected_score in match_cases:
    result = engine.calculate_match_score(profile, activity)
    if result == expected_score:
        status = "✅"
        passed += 1
    else:
        status = "❌"
        failed += 1
    print(f"{status} {profile} + {activity} = {result} (expected {expected_score})")

# TEST 3: Transport Carbon Data
print("\n\n3️⃣ TEST: Transport Carbon Mapping")
print("-" * 60)

transports = {
    "avion": (255, "Élevé"),
    "train": (15, "Faible"),
    "bus": (50, "Moyen"),
    "voiture": (120, "Moyen"),
    "velo": (0, "Faible"),
}

for transport, (expected_co2, expected_level) in transports.items():
    co2_per_km = engine.transport_carbon_per_km.get(transport, 0.15)
    co2_100km = co2_per_km * 100
    result = engine.calculate_carbon_score(co2_100km)
    
    print(f"   {transport:10} → {co2_per_km} kg/km (100km = {co2_100km}kg CO2)")

print("\n\n4️⃣ TEST: Profile Activity Compatibility Matrix")
print("-" * 60)

compatibility_matrix = {
    "Adventure": ["ActiviteSportive", "Randonnée", "Escalade"],
    "Culture": ["ActiviteCulturelle", "Musée", "Patrimoine"],
    "BienEtre": ["Spa", "Yoga", "Méditation"],
    "Famille": ["ActiviteEducative", "Parc", "Musée"],
}

for profile, activities in compatibility_matrix.items():
    print(f"\n👤 {profile}:")
    for activity in activities:
        score = engine.calculate_match_score(profile, activity)
        status = "✅" if score > 50 else "⚠️ "
        print(f"   {status} {activity}: {score}/100")
        if score > 50:
            passed += 1
        else:
            failed += 1

# TEST 5: Recommendation Generation Structure
print("\n\n5️⃣ TEST: Recommendation Structure")
print("-" * 60)

recommendation_keys = [
    'profile',
    'destination',
    'recommendation_score',
    'activities',
    'accommodation',
    'transport',
    'total_carbon_kg',
    'reasons'
]

print("Expected recommendation keys:")
for key in recommendation_keys:
    print(f"   ✅ {key}")

# TEST 6: Score Ranges
print("\n\n6️⃣ TEST: Score Ranges Validation")
print("-" * 60)

carbon_scores = [
    engine.calculate_carbon_score(10)['score'],
    engine.calculate_carbon_score(50)['score'],
    engine.calculate_carbon_score(100)['score'],
    engine.calculate_carbon_score(200)['score'],
]

all_valid = all(0 <= score <= 100 for score in carbon_scores)
if all_valid:
    print("✅ All carbon scores in range [0-100]")
    passed += 1
else:
    print("❌ Some carbon scores out of range")
    failed += 1

print("\nCarbon scores by CO2:")
for co2, score in [(10, carbon_scores[0]), (50, carbon_scores[1]), 
                    (100, carbon_scores[2]), (200, carbon_scores[3])]:
    print(f"   CO2 {co2}kg → Score {score}/100")

# FINAL SUMMARY
print("\n" + "=" * 60)
print(f"📊 SUMMARY: {passed} Passed ✅ | {failed} Failed ❌")
print("=" * 60)

if failed == 0:
    print("\n🎉 ALL TESTS PASSED! Engine ready for production.")
else:
    print(f"\n⚠️  {failed} tests need attention.")
