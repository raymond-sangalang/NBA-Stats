from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from playerDB import nbaDatabase
from buildFeature import build_features

db = nbaDatabase()

games = db.get_all_games()

X = []
y = []

for home_team, away_team, home_win in games:

    features = build_features(
        db,
        home_team,
        away_team
    )

    X.append(features)
    y.append(home_win)

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# train model
model = LogisticRegression()

model.fit(X_train, y_train)

# evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy:.3f}")

# sample prediction
sample = [[5.2, 1.1]]

prob = model.predict_proba(sample)[0][1]

print(f"Home team win probability: {prob:.2%}")