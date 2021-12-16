   
import matplotlib.pyplot as plt
from IPython import display
import sys, os

def plot(scores, mean_scores, epsilon):
    my_dpi = 125
    plt.figure(figsize=(500/my_dpi, 500/my_dpi), dpi=my_dpi)
    plt.clf()
    plt.title(f'Epsilon: {epsilon:.2f}')
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(scores, label = 'Current Score')
    plt.plot(mean_scores, label = 'Mean Score (last 100)')
    plt.legend(loc="lower right")
    plt.ylim(ymin=-6)
    plt.text(len(scores)-1, scores[-1], '{:.2f}'.format(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], '{:.2f}'.format(mean_scores[-1]))
    plt.grid(True)
    plt.savefig("assets/plot.png", bbox_inches='tight', dpi = my_dpi)
    plt.close()