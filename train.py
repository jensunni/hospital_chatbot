import joblib 
# to provide lightweight pipelining and efficient processing, 
# particularly for objects containing large NumPy arrays

import pandas as pd, seaborn as sns, matplotlib
matplotlib.use("Agg") 
# configures Matplotlib to use the Agg (Anti-Grain Geometry) backend.
# Anti-Grain Geometry (AGG) is a high-performance, 
# open-source 2D vector graphics library written in C++ by Maxim Shemanarev.
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer # text to numerical matrix
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB   # like a histogram
from sklearn.svm import LinearSVC  # Support Vector Classification (SVC)
from sklearn.ensemble import RandomForestClassifier

from db_utils import q
from nlp_utils import preprocess
from config import MODEL_PATH

df = pd.DataFrame(q("SELECT p.pattern, i.tag FROM patterns p JOIN intents i USING(intent_id)"))
df["clean"] = df["pattern"].apply(preprocess)
Xtr, Xte, ytr, yte = train_test_split(df.clean, df.tag, test_size=0.25,stratify=df.tag, random_state=42)

candidates = {
    "Logistic Regression": LogisticRegression(max_iter=1000, C=10),
    "Naive Bayes": MultinomialNB(),
    "Linear SVM": LinearSVC(),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
}
results = {}
for name, clf in candidates.items():
    pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), clf).fit(Xtr, ytr)
    results[name] = accuracy_score(yte, pipe.predict(Xte))
    print(f"{name:22s} accuracy = {results[name]:.3f}")

# detailed report for Logistic Regression (used in the bot: gives probabilities)
best = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000, C=10)).fit(Xtr, ytr)
pred = best.predict(Xte)
print("\n", classification_report(yte, pred, zero_division=0))

labels = sorted(df.tag.unique())
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_matrix(yte, pred, labels=labels), annot=True, fmt="d",
xticklabels=labels, yticklabels=labels, cmap="Blues")
plt.title("Confusion matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)

plt.figure(figsize=(6, 4))
sns.barplot(x=list(results.keys()), y=list(results.values()))
plt.xticks(rotation=20); plt.ylim(0, 1.05); plt.title("Model comparison (accuracy)")
plt.tight_layout(); plt.savefig("model_comparison.png", dpi=150)

# final model trained on ALL data
final = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000, C=10))
final.fit(df.clean, df.tag)
joblib.dump(final, MODEL_PATH)
print("Saved", MODEL_PATH)