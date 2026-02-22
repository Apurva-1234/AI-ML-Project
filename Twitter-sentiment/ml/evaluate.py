import pickle
from sklearn.metrics import classification_report, confusion_matrix

model = pickle.load(open("../model/v1/trained_model.sav", "rb"))
vectorizer = pickle.load(open("../model/v1/vectorizer.pkl", "rb"))


print("Precision / Recall / F1:")
print(classification_report(y_test, model.predict(X_test)))

print("Confusion Matrix:")
print(confusion_matrix(y_test, model.predict(X_test)))
