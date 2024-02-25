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
    month_mapping = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
                     'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
    visitor_mapping = {'Returning_Visitor': 1, 'New_Visitor': 0, 'Other': 0}
    boolean_mapping = {'FALSE': 0, 'TRUE': 1}
    mappings = [month_mapping, visitor_mapping, boolean_mapping]
    with open(filename, newline='') as file:
        evidences = []
        labels = []
        filereader = csv.reader(file, delimiter=',')
        next(filereader)
        for row in filereader:
            evidence = []
            for evidence_elem in row:
                evidence_elem = convert_to_numeric(evidence_elem)
                if isinstance(evidence_elem, int) or isinstance(evidence_elem, float):
                    evidence.append(evidence_elem)
                    continue
                if isinstance(evidence_elem, str):
                    found = False
                    for mapping in mappings:
                        if evidence_elem in mapping:
                            found = True
                            evidence.append(mapping[evidence_elem])
                            break
                    if not found:
                        print(evidence_elem)
            label = [evidence[-1]]
            evidence = evidence[:-1]
            # if len(evidence) != 17:
            #     print(row)
            evidences.append(evidence)
            labels.append(label)
        return evidences, labels


def convert_to_numeric(data):
    try:
        # 尝试将字符串转换为整数
        result = int(data)
        return result
    except ValueError:
        try:
            # 尝试将字符串转换为浮点数
            result = float(data)
            return result
        except ValueError:
            # 如果都失败了，返回原始字符串
            return data


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(evidence, labels)
    return knn


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
    positive_cnt = 0
    true_positive_cnt = 0
    negative_cnt = 0
    true_negative_cnt = 0
    for i in range(len(labels)):
        value = labels[i][0] if isinstance(labels[i], list) else labels[i]
        if value == 0:
            negative_cnt += 1
            if predictions[i] == 0:
                true_negative_cnt += 1
        if value == 1:
            positive_cnt += 1
            if predictions[i] == 1:
                true_positive_cnt += 1
    return true_positive_cnt / positive_cnt, true_negative_cnt / negative_cnt


if __name__ == "__main__":
    main()
