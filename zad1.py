import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, TextBox, CheckButtons

#------------------------------------------------------------------------------
class Point():
    @staticmethod
    def are_colinear(a, b, c):
        return np.dot(a, np.cross(b, c)) == 0

    @staticmethod
    def has_3_colinear(points):
        if len(points) == 0:
            return False

        for i in range(4):
            k = [k for k in range(4) if k != i]
            if Point.are_colinear(points[k[0]], points[k[1]], points[k[2]]):
                return True
        return False

    @staticmethod
    def normalized(points):
        newPoints = np.array(points)
        for i, point in enumerate(points):
            newPoints[i][0] /= points[i][2]
            newPoints[i][1] /= points[i][2]
            newPoints[i][2] = 1.
        return newPoints

#------------------------------------------------------------------------------
class Mapper(object):
    def __init__(self, 
                 inputPoints, 
                 outputPoints, 
                 axisIn, 
                 axisOut, 
                 inputField,
                 outputField,
                 txtMatrix):
        self.set_input(inputPoints)
        self.set_output(outputPoints)
        self.set_plot_axes(axisIn, axisOut)
        self.inputField = inputField
        self.outputField = outputField
        self.txtMatrix = txtMatrix
        self.gridSnap = False

    def transform_matrix(self):
        # Koeficijenti preslikavanja (Baza --> Input)
        coefsIn = linear_decomposition(self.input)

        # Matrica preslikavanja (Baza --> Input)
        P1 = np.transpose(
                np.delete(self.input, len(self.input)-1, axis = 0)) * coefsIn

        # Koeficijenti preslikavanja (Baza --> Output)
        coefsOut = linear_decomposition(self.output)

        # Matrica preslikavanja (Baza --> Output) 
        P2 = np.transpose(
                np.delete(self.output, len(self.output)-1, axis = 0)) * coefsOut

        # Matrica preslikavanja 
        # (Input --> Output) 
        # (Baza --> Output) o ((Baza --> Input)^(-1))
        # (Baza --> Output) o (Input --> Baza)
        return P2 @ np.linalg.inv(P1)

    def update_transform_matrix(self, event):
        if len(self.input) < 4 or len(self.output) < 4:
            return

        matrix = self.transform_matrix()
        text = ''
        for row in matrix:
            text += ('%.4g  %.4g  %.4g\n' % (row[0], row[1], row[2]))
        self.txtMatrix.set_val(text)

    def plot(self):
        # Brisanje prethodnog sadrzaja
        self.axisIn.cla()
        self.axisOut.cla()

        # Prilagodjavanje granica osa u odnosu na tacke 
        adjust_to_points(self.axisIn, self.input, margin = 0.5)
        adjust_to_points(self.axisOut, self.output, margin = 0.5)

        # Iscrtavanje mreze
        plot_grid(self.axisIn, offset = 1)
        plot_grid(self.axisOut, offset = 1)

        # Vizualni izgled tacaka
        pointMarks = ('rD', 'gD', 'bD', 'yD')

        # Ulazne tacke
        plot_points(self.input, pointMarks, self.axisIn)
        plot_line(self.input, axes = self.axisIn, loop = True)

        # Izlazne tacke
        plot_points(self.output, pointMarks, self.axisOut)
        plot_line(self.output, axes = self.axisOut, loop = True)

        # Ispis tacaka u polja
        display_points(self.input, self.inputField)
        display_points(self.output, self.outputField)

    def onclick(self, event):
        if event.button != 1:
            return

        if self.gridSnap:
            newPoint = np.array([[round(event.xdata), round(event.ydata), 1.]])
        else:
            newPoint = np.array([[event.xdata, event.ydata, 1.]])

        if event.inaxes == self.axisIn:
            if len(self.input) == 0:
                self.input = newPoint
            else:
                self.input = np.append(self.input, newPoint, axis = 0)
        elif event.inaxes == self.axisOut:
            if len(self.output) == 0:
                self.output = newPoint
            else:
                self.output = np.append(self.output, newPoint, axis = 0)
        self.plot()


    def reset(self, event):
        self.input = np.array([])
        self.output = np.array([])

        # Brisanje polja za prikaz tacaka
        for txt1, txt2 in zip(self.inputField, self.outputField):
            txt1.set_val('')
            txt2.set_val('')

        self.txtMatrix.set_val('0 0 0\n0 0 0\n0 0 0')
        self.plot()

    def grid_snap(self, label):
        if label == 'default':
            self.gridSnap = False
        else:
            self.gridSnap = True

    def set_plot_axes(self, axisIn, axisOut):
            self.axisIn = axisIn
            self.axisOut = axisOut

    def set_input(self, points, check_colinear = True):
        if check_colinear:
            if Point.has_3_colinear(points):
                print('Postoje 3 kolinearne tacke')
        self.input = np.array(points)

    def set_output(self, points, check_colinear = False):
        if check_colinear: 
            if Point.has_3_colinear(points): 
                print('Postoje 3 kolinearne tacke')
        self.output = np.array(points)
#------------------------------------------------------------------------------
    
def main():
    # Kreiranje plotova
    fig, (axisIn, axisOut) = plt.subplots(1,2)

    # Naslovi
    axisIn.set_title("Input")
    axisOut.set_title("Output")

    # Podrazumevane tacke
    inputPoints = np.array([[-1., 0., 1.], 
                            [6., 1., 1.], 
                            [6., 7., 1.], 
                            [-1., 7., 1.]])
    
    # Matrica preslikavanja
    matrixTransform = np.array([[0.3, 0.4, 0.3],
                                [0., 0.4, -0.3],
                                [0., 0.4, 0.3]])
    
    # Slike tacaka
    outputPoints = transform_points(inputPoints, matrixTransform)
    outputPoints = Point.normalized(outputPoints)

    # TextBox
    txtMatrixTransformAxis = plt.axes([0.1, 0.02, 0.25, 0.15])
    txtMatrixTransform = TextBox(txtMatrixTransformAxis, 
                                 'P: ', 
                                 initial = '0 0 0\n0 0 0\n0 0 0')

    # Dimenzije polja za unos tacaka 
    inLeft = 0.05
    inBot = 0.92
    inWidth = 0.15
    inHeight = 0.05
    inColSpace = inWidth + 0.08
    inRowSpace = inHeight + 0.05

    # Ose za polja
    inputAxes = []
    outputAxes = []

    # Polja za unos
    inputField = []
    outputField = []

    pointNum = 4
    # Postavljanje polja za unos tacaka
    for i in range(pointNum):
        inputAxes.append(plt.axes([
            inLeft + i * inColSpace, 
            inBot, 
            inWidth, 
            inHeight]))

        outputAxes.append(plt.axes([
            inLeft + i * inColSpace,
            inBot - inRowSpace,
            inWidth,
            inHeight]))

        inputField.append(TextBox(inputAxes[i], ('p%d: ' % i)))
        outputField.append(TextBox(outputAxes[i], ('p%d\': ' % i)))

    mapper = Mapper(inputPoints, outputPoints, axisIn, axisOut, 
                    inputField, outputField,txtMatrixTransform) 
    mapper.plot()
    
    # Dimenzije dugmica za izracunavanje i izlaz
    btnWidth = 0.15
    btnHeight = 0.05
    btnLeft = 0.4
    btnBot = 0.02
    btnSpace = btnWidth + 0.05

    # Iscrtavanje dugmica
    btnCalcAxis = plt.axes([btnLeft, btnBot, btnWidth, btnHeight])
    btnResetAxis = plt.axes([btnLeft + btnSpace, btnBot, btnWidth, btnHeight])
    btnExitAxis = plt.axes([btnLeft + btnSpace * 2, btnBot, btnWidth, btnHeight])
    btnGridSnapAxis = plt.axes([btnLeft, btnBot + 0.07, 0.20, 0.08])

    # Dugmici
    btnCalc = Button(btnCalcAxis, 'Calculate')
    btnReset = Button(btnResetAxis, 'Reset')
    btnExit = Button(btnExitAxis, 'Exit')
    btnGridSnap = RadioButtons(
                     btnGridSnapAxis, ('default', 'grid snap'))
    
    btnCalc.on_clicked(mapper.update_transform_matrix)
    btnReset.on_clicked(mapper.reset)
    btnExit.on_clicked(sys.exit)
    btnGridSnap.on_clicked(mapper.grid_snap)

    # Mouse click event
    cid = fig.canvas.mpl_connect('button_press_event', mapper.onclick)

    plt.show()

#------------------------------------------------------------------------------
def are_coplanar(a, b, c):
    return np.dot(a, np.cross(b, c)) == 0;
#------------------------------------------------------------------------------
def plot_line(points, color = 'r', axes = plt, loop = False):
    if (len(points) == 0):
        return

    if loop:
        pointsLoop = np.insert(points, len(points), points[0], axis = 0)
        axes.plot(pointsLoop[:,0], pointsLoop[:,1], color)
    else:
        axes.plot(points[:,0], points[:,1], color)
#------------------------------------------------------------------------------
def plot_grid(axis = plt, offset = 1):
    minX, maxX = axis.get_xlim()
    minY, maxY = axis.get_ylim()

    left = int(min(minX, minY)) - 1
    right = int(max(maxX, maxY)) + 1
    size = (right - left) + 1 

    # Broj cvorova ose
    nodes = int(size / offset) + 1
    grid = np.linspace(left, left + size, nodes)

    for i in range(nodes):
        axis.plot(grid, np.repeat(grid[i], nodes), 'c-')
        axis.plot(np.repeat(grid[i], nodes), grid, 'c-')
#------------------------------------------------------------------------------
def adjust_to_points(axis, points, aspect = 'equal', margin = 0.5):
    if (len(points) > 1):
        x = points[:,0]
        y = points[:,1]
    else:
        x = [0, 5]
        y = [0, 5]

    xMin, xMax = min(x), max(x)
    yMin, yMax = min(y), max(y)

    xRange = xMax - xMin
    yRange = yMax - yMin

    # Rastojanje najdalje tacke od ivice canvasa
    maxRange = xRange if xRange > yRange else yRange
    padding = maxRange * margin

    left = xMin - padding
    right = left + maxRange + 2 * padding
    bot = yMin - padding
    top = bot + maxRange + 2 * padding
    
    # Postavljanje granica i razmera osa
    axis.set_xlim(left, right)
    axis.set_ylim(bot, top)
    axis.set_aspect(aspect, adjustable='box')
#------------------------------------------------------------------------------
def transform_points(points, transform):
    return np.array([transform @ np.transpose(x) for x in points])
#------------------------------------------------------------------------------
def plot_points(points, colors, axis = plt):
    for point, color in zip(points, colors):
        axis.plot(point[0], point[1], color)
#------------------------------------------------------------------------------
def linear_decomposition(points):
    matrix = np.transpose(np.delete(points, len(points)-1, axis = 0))
    result = np.transpose(points[-1])

    xMatrix = substitute_column(matrix, 0, result) 
    yMatrix = substitute_column(matrix, 1, result)
    zMatrix = substitute_column(matrix, 2, result)

    det = np.linalg.det(matrix)
    detX = np.linalg.det(xMatrix)
    detY = np.linalg.det(yMatrix)
    detZ = np.linalg.det(zMatrix)

    return np.array([detX/det, detY/det, detZ/det])
#------------------------------------------------------------------------------
def substitute_column(matrix, column, value):
    return np.insert(np.delete(matrix, column, axis = 1), column, value, axis = 1)
#------------------------------------------------------------------------------
def display_points(points, field):
    for point, text in zip(points, field):
        text.set_val('(%.2g : %.2g : %.2g)' % (point[0], point[1], point[2]))
#------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
