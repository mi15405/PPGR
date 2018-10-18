import matplotlib.pyplot as plt
import numpy as np

def main():
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x**2)

    # Simple plot
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [1,4,9,16], 'ro')
    ax.set_title("test plot")

    # 2 plots sharing Y AXIS 
    ''' 
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey = True)
    ax1.plot(x, y)
    ax1.set_title('Sharing Y axis')
    ax2.scatter(x, y)
    ''' 

    # 4 Polar plots
    '''
    fig, axes = plt.subplots(2, 2, subplot_kw = dict(polar=True))
    axes[0, 0].plot(x, y)
    axes[1, 1].scatter(x, y)
    '''

    '''
    fig, axes = plt.subplots(2, 2, sharex='col')
    axes[0, 0].plot(x, x**3)
    axes[0, 1].plot(x, np.sin(x))
    '''

     

    fig.show()

    raw_input("%s")


if __name__ == "__main__":
    main()
