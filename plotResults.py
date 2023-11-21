import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

def plotData(data, overallLength, algorithm):
    """
    Plots the given data on a 2D graph with time spent on the x-axis and text length on the y-axis.

    Parameters:
    - data (list or array): The data points to be plotted, representing the time spent.
    - overallLength (list or array): The corresponding data points for the text length.
    - algorithm (str): The name of the algorithm or process being visualized.

    Returns:
    None

    Example:
    >>> plotData([1, 2, 3], [10, 15, 20], "Algorithm A")
    """
    # plotting the points
    plt.plot(data, overallLength)

    # naming the x axis
    plt.xlabel('x - time spent')
    # naming the y axis
    plt.ylabel('y - text length')

    # giving a title to the graph
    plt.title(algorithm)

    # function to show the plot
    plt.show()

    # store the plot
    plt.savefig("plots/"+algorithm+'.png')


def severalPlots(y, plots, names, title):
    fig = plt.figure()
    fig.clf()
    ax = fig.subplots(1,1)
    for i in range(0, len(plots)):
        ax.plot(plots[i], y, names[i])
    ax.set_xlabel('x - time spent')
    ax.set_ylabel('y - text length')

    ax.legend()
    fig.tight_layout()
    fig.title(title)
    fig.show()            
