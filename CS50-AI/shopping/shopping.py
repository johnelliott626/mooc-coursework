import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Dictionary mapping month abbreviations to numbers
    months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }

    evidence = []
    labels = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_list = []
            row_list.append(int(row["Administrative"]))
            row_list.append(float(row["Administrative_Duration"]))
            row_list.append(int(row["Informational"]))
            row_list.append(float(row["Informational_Duration"]))
            row_list.append(int(row["ProductRelated"]))
            row_list.append(float(row["ProductRelated_Duration"]))
            row_list.append(float(row["BounceRates"]))
            row_list.append(float(row["ExitRates"]))
            row_list.append(float(row["PageValues"]))
            row_list.append(float(row["SpecialDay"]))
            row_list.append(months[row["Month"]])
            row_list.append(int(row["OperatingSystems"]))
            row_list.append(int(row["Browser"]))
            row_list.append(int(row["Region"]))
            row_list.append(int(row["TrafficType"]))
            row_list.append(0 if row["VisitorType"] == "New_Visitor" else 1)
            row_list.append(1 if row["Weekend"] == "TRUE" else 0)
            evidence.append(row_list)
            labels.append(1 if row["Revenue"] == "TRUE" else 0)
    return evidence, labels





def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    count_positive_labels = count_negative_labels = 0
    correct_positive = correct_negative = 0
    n = len(predictions)
    for i in range(n):
        if labels[i] == 1:
            count_positive_labels += 1
        else: 
            count_negative_labels += 1

        if predictions[i] == 1 and labels[i] == 1:
            correct_positive += 1
        elif predictions[i] == 0 and labels[i] == 0:
            correct_negative += 1

    sensitivity = correct_positive / count_positive_labels
    specificity = correct_negative / count_negative_labels
    return sensitivity, specificity


if __name__ == "__main__":
    main()
