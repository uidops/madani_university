import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

sns.set_theme(style="darkgrid")
RANDOM_STATE = 37

diabetes = pd.read_csv("datasets/diabetes.csv")
diabetes.info()

counts = diabetes["Outcome"].map({0: "healthy", 1: "diabetic"}).value_counts().reindex(["diabetic", "healthy"], fill_value=0).rename_axis("Outcome").reset_index(name="Count")
fig, ax = plt.subplots(figsize=(11, 4.5))
sns.barplot(data=counts, x="Count", y="Outcome", hue="Outcome",
    palette={"diabetic": "#E8C629", "healthy": "#80B5D5"},
    dodge=False,
    edgecolor="black",
    legend=False,
    ax=ax
)

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.0f",
        label_type="edge",
        padding=-25
    )

ax.set_title("Count of Outcome variable", loc="left")
ax.set_xlabel("")
ax.set_ylabel("")

plt.tight_layout()
plt.show()

# Pregnancies -> تعداد بارداری‌ها
# Glucose -> قند خون
# BloodPressure -> فشار خون
# SkinThickness -> ضخامت چین پوستی
# Insulin -> انسولین
# BMI -> شاخص توده بدنی
# DiabetesPedigreeFunction -> شاخص سابقه خانوادگی دیابت
# Age -> سن
# Outcome -> نتیجه‌(دیابت دارد یا خیر)

print((diabetes == 0).sum())

zero_features = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
impute_stat = {"Glucose": "mean", "BloodPressure": "median", "SkinThickness": "median", "Insulin": "median", "BMI": "median"}
diabetes[zero_features] = diabetes[zero_features].replace(0, np.nan)
for feature, stat in impute_stat.items():
    diabetes[feature] = diabetes.groupby("Outcome")[feature].transform(lambda s, stat=stat: s.fillna(getattr(s, stat)()))

print(((diabetes == 0) | diabetes.isna()).sum())


# EDA-derived features
def add_extracted_features(df):
    df = df.copy()
    df["HighBP_HighGlucose"] = ((df["BloodPressure"] > 80) & (df["Glucose"] > 105)).astype(int)
    df["HighBP"] = (df["BloodPressure"] > 80).astype(int)
    return df


diabetes = add_extracted_features(diabetes)
print(diabetes.head())

X = diabetes.copy()
y = X.pop("Outcome")

extended_features = list(X.columns)
normal_features = [f for f in extended_features if f not in ("HighBP_HighGlucose", "HighBP")]
reduced_features = [f for f in normal_features if f not in ("SkinThickness", "DiabetesPedigreeFunction")]

SETUP_TITLES = {
    "extended": "Table 3 — all available features and two new extracted features",
    "normal": "Table 4 — without the two new extracted features",
    "reduced": "Table 5 — without SkinThickness, Pedigree and the two new extracted features",
}
FEATURE_SETS = {
    "extended": extended_features,
    "normal": normal_features,
    "reduced": reduced_features,
}

X_scaled = pd.DataFrame(MinMaxScaler().fit_transform(X), columns=X.columns, index=X.index)


def make_split(features):
    return train_test_split(X_scaled[features], y, test_size=0.3, random_state=RANDOM_STATE)


splits = {setup: make_split(features) for setup, features in FEATURE_SETS.items()}

print({setup: (f"train={len(s[0])}", f"test={len(s[1])}") for setup, s in splits.items()})


def plot_confusion_matrix(y_true, y_pred, title="Confusion Matrix"):
    # Paper layout (Table 2): rows = forecasted, columns = actual, positive class first
    cm = confusion_matrix(y_true, y_pred, labels=[1, 0]).T

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu", xticklabels=["Positive (1)", "Negative (0)"], yticklabels=["Positive (1)", "Negative (0)"], annot_kws={"size": 14})
    plt.xlabel("Actual values")
    plt.ylabel("Forecasted values")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def get_metrics(y_true, y_pred, technique):
    return {
        "Classification Technique": technique,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, average="macro"),
        "Recall": recall_score(y_true, y_pred, average="macro"),
        "F1": f1_score(y_true, y_pred, average="macro"),
    }


metrics = {"extended": [], "normal": [], "reduced": []}


def run_model(model, label):
    for setup, (X_train, X_test, y_train, y_test) in splits.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        if setup == "extended":
            plot_confusion_matrix(y_test, y_pred, title=f"Confusion matrix for {label} algorithm")
        metrics[setup].append(get_metrics(y_test, y_pred, label))


print("\n--- KNN (k=29) ---")
knn = KNeighborsClassifier(n_neighbors=29, weights="distance", metric="minkowski", p=1)
run_model(knn, "KNN")

print("\n--- Random forests ---")
rf = RandomForestClassifier(
    n_estimators=100,
    criterion="gini",
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=RANDOM_STATE,
    n_jobs=-1
)
run_model(rf, "RF")

print("\n--- SVM ---")
svm = SVC(kernel="rbf", C=10, gamma="scale", random_state=RANDOM_STATE)
run_model(svm, "SVM")

print("\n--- ANN ---")
ann = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    activation="relu",
    solver="adam",
    alpha=0.01,
    learning_rate_init=0.001,
    max_iter=2000,
    random_state=RANDOM_STATE,
)
run_model(ann, "ANN")

print("\n--- Decision Tree ---")
dt = DecisionTreeClassifier(
    criterion="gini",
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=RANDOM_STATE
)
run_model(dt, "DT")


def format_percent(df):
    return df.map("{:.2%}".format).to_string()


results = {
    setup: pd.DataFrame(rows).set_index("Classification Technique")
    for setup, rows in metrics.items()
}

for setup, title in SETUP_TITLES.items():
    print(f"—— {title} ——")
    print(format_percent(results[setup]))
    print()

accuracy = pd.DataFrame({
    "Accuracy with using two new extracted feature": results["extended"]["Accuracy"],
    "Accuracy without using two new extracted feature": results["normal"]["Accuracy"],
})

with sns.axes_style("white"):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    accuracy.plot(kind="bar", color=["#4472C4", "#C0504D"], width=0.4, ax=ax)
ax.set_ylim(0, 1)
ax.set_yticks(np.arange(0, 1.01, 0.2))
ax.yaxis.grid(True, color="#D9D9D9")
ax.set_axisbelow(True)
sns.despine(ax=ax, left=True)
ax.tick_params(axis="y", length=0)
ax.set_xlabel("Classification Techniques", fontfamily="serif", fontweight="bold", fontsize=12)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=1, frameon=False, fontsize=9)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

print(format_percent(accuracy))
