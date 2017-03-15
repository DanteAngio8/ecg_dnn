from __future__ import division
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
import plot
import numpy as np
from tabulate import tabulate


def flatten_gt_and_preds(gt, preds):
    def flatten_and_to_list(inp):
        return inp.flatten().tolist()
    return flatten_and_to_list(gt), flatten_and_to_list(preds)


def get_confusion_matrix(gt, preds):
    cnf = confusion_matrix(*flatten_gt_and_preds(gt, preds)).tolist()
    return cnf


def set_score(
        gt,
        preds,
        classes,
        is_binary=False,
        class_name=None,
        threshold=None,
        **params):
    print('Set Score')
    if is_binary is True:
        print(class_name, precision_recall_fscore_support(
            gt, preds, average='binary'), threshold)
    else:
        print(classification_report(
            gt, preds, target_names=classes, digits=3))


def seq_score(
        ground_truth,
        predictions,
        classes,
        confusion_table=False,
        report=False,
        plotting=False,
        is_binary=False,
        class_name=None,
        threshold=None):

    print('Sequence Score')
    cnf = get_confusion_matrix(ground_truth, predictions)

    if plotting is True:
        plot.plot_confusion_matrix(
            np.log10(np.array(cnf) + 1), classes)

    if confusion_table is True:
        for i, row in enumerate(cnf):
            row.insert(0, classes[i])

        print(tabulate(cnf, headers=[c[:1] for c in classes]))

    if report is True:
        gt_flat, preds_flat = flatten_gt_and_preds(
            ground_truth, predictions)
        print(classification_report(
            gt_flat, preds_flat, target_names=classes, digits=3))

    if is_binary is True:
        tn, fp, fn, tp = cnf[0][0], cnf[0][1], cnf[1][0], cnf[1][1]
        scores = (sensitivity, specificity) = tp / (tp+fn), tn / (tn+fp)
        print(class_name, scores, threshold)