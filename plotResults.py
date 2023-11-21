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
    """
    Plot multiple curves on a single graph.

    Parameters:
    - y (array-like): The y-values to be plotted on the vertical axis.
    - plots (list of array-like): List containing arrays of x-values for each curve to be plotted.
    - names (list of str): List containing labels for each curve to be plotted.
    - title (str): Title of the plot.

    Returns:
    None

    Example:
    severalPlots(y_values, [x_values1, x_values2], ['Curve 1', 'Curve 2'], 'Multiple Curves Plot')
    """
    # Create a new figure
    fig = plt.figure()
    fig.clf()

    # Create a subplot with one row and one column
    ax = fig.subplots(1, 1)

    # Plot each curve with corresponding x-values and labels
    for i in range(len(plots)):
        ax.plot(plots[i], y, label=names[i])

    # Set x and y axis labels
    ax.set_xlabel('x - time spent')
    ax.set_ylabel('y - text length')

    # Display the legend to distinguish between curves
    ax.legend()

    # Adjust layout to prevent clipping of labels
    fig.tight_layout()

    # Set the title of the plot
    fig.suptitle(title)

    # Display the plot
    fig.show()
