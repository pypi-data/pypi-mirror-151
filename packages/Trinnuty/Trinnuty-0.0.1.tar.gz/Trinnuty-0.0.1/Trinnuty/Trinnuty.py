import math
import numpy as np
import pandas as pd
pd.options.display.max_colwidth = 1800
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"
import plotly.io as pio
pio.templates.default = "plotly_dark"
import sqlite3
from sqlalchemy import create_engine
from matplotlib import pyplot as plt
plt.style.use('dark_background')
from mpl_toolkits import mplot3d
# import sys
# !conda install --yes --prefix {sys.prefix} qgrid
# import qgrid


class KeanuPoint:
    def __init__(self, position, currentVector, reboundForce, matrix_Observer_Interaction, startingSize, flushRadius, colorValue, lineColorValue, startingOpacity):
        self.currentPosition = position
        self.currentVector = currentVector
        self.reboundForce = reboundForce
        self.matrixInteraction = matrix_Observer_Interaction
        self.currentSize = startingSize
        self.flushRadius = flushRadius
        self.currentLineColorValue = lineColorValue
        self.currentColorValue = colorValue
        self.colorValueHistory = [colorValue]
        self.currentOpacity = startingOpacity
        self.OpacityHistory = [startingOpacity]
        self.lineColorValueHistory = [lineColorValue]
        self.positionHistory = [self.currentPosition]
        self.vectorHistory = [self.currentVector]
        self.reboundHistory = [self.reboundForce]
        self.matrixInteractionHistory = [self.matrixInteraction]
        self.sizeHistory = [self.currentSize]
        
    def getCurrent_Position(self):
        return self.currentPosition
    def getCurrent_Vector(self):
        return self.currentVector
    def getCurrent_ColorValue(self):
        return self.currentColorValue
    def getCurrent_Line_ColorValue(self):
        return self.currentLineColorValue
    def getCurrent_Opacity(self):
        return self.currentOpacity
    def get_FlushRadius(self):
        return np.array(self.flushRadius).sum() / len(self.flushRadius)
    def applyCustomForceFunction(self, forceFunction, silent=False, dryRun=False):
        returnData = forceFunction(self)
        if not silent:
            print("returnData: ")
            print(returnData)
        # if not dryRun:
        # NOTE: Apply force here:
        #     self.position = returnData.position
        #     self.currentVector = returnData.currentVector
        #     self.reboundForce = returnData.reboundForce 
        #     self.matrixInteraction = returnData.matrixInteraction
    def returnSaveable(self):
        return {
                "position": self.currentPosition,
                "currentVector": self.currentVector,
                "reboundForce": self.reboundForce,
                "matrixInteraction": self.matrixInteraction,
                "currentSize": self.currentSize,
                "flushRadius": self.flushRadius,
                "lineColorValue": self.currentLineColorValue,
                "colorValue": self.currentColorValue,
                "colorValueHistory": self.colorValueHistory,
                "currentOpacity": self.currentOpacity,
                "OpacityHistory": self.OpacityHistory,
                "lineColorValueHistory": self.lineColorValueHistory,
                "positionHistory": self.positionHistory,
                "vectorHistory": self.vectorHistory,
                "reboundHistory": self.reboundHistory,
                "matrixInteractionHistory": self.matrixInteractionHistory,
                "sizeHistory": self.sizeHistory,
            }
    def get_Distance(self, relativePoint):
        return math.sqrt(abs(relativePoint[0] - self.currentPosition[0]) + abs(relativePoint[1] - self.currentPosition[1]) + abs(relativePoint[2] - self.currentPosition[2]))
    def getCurrent_Size(self):
        return self.currentSize
    def log(self):
        saveable = self.returnSaveable()
        _printArr = [f'{key}: {saveable[key]}' for key in saveable]
        _printArr.append("______________________________________")
        for _p in _printArr:
            print(_p)
    def __str__(self):
        saveable = self.returnSaveable()
        _printArr = [f'{key}: {saveable[key]}' for key in saveable]
        _printArr.append("______________________________________")
        _printString = '\r\n'.join(_printArr)
        return _printString
    def get_sphericalTrace(self):
        theta = np.linspace(0,2*np.pi,100)
        phi = np.linspace(0,np.pi,100)
        x0 = self.currentPosition[0] + self.currentSize * np.outer(np.cos(theta),np.sin(phi))
        y0 = self.currentPosition[1] + self.currentSize * np.outer(np.sin(theta),np.sin(phi))
        z0 = self.currentPosition[2] + self.currentSize * np.outer(np.ones(100),np.cos(phi))
        trace= go.Surface(x=x0, y=y0, z=z0, colorscale="plasma")
        trace.update(showscale=False)
        return trace




class KeanuReeves:
    def __init__(self, accuracy=20, dimensions=[10, 10, 10], startingVector=[12, 0, 0], reboundParticleForce=0.05, matrix_Observer_InteractionForce=0.2, pointScaleFactor=1, 
matrixFlush=False, startingColorValue=0.5, startingLineColorValue=0.5, startingOpacity=0.8, gridPadding=0):
        self.accuracy = accuracy
        self.dimensions = dimensions
        self.startingVector = startingVector
        self.startingReboundForce = reboundParticleForce
        self.pointScaleFactor = pointScaleFactor
        self.startingColorValue = startingColorValue
        self.startingLineColorValue = startingLineColorValue
        self.startingMatrixInteraction = matrix_Observer_InteractionForce
        self.startingOpacity = startingOpacity
        self.gridPadding = gridPadding
        self.radius = [self.dimensions[0] / 2, self.dimensions[1] / 2, self.dimensions[2] / 2]
        self.matrixFlush = matrixFlush
        self.databaseName = "Matrix-exploratory"
        self.updateDFCount = 0
        self.datastore_target_directory = "/Users/bigsexy/Desktop/python/books/DashAppFuckkkkJupyterHard/dataBank/"
        self.sqlConnectionString = f"{self.datastore_target_directory}KeanuReeves.db"
        self.tableName = f"KeanuReeves_dimensions{self.dimensions[0]}_{self.dimensions[1]}_{self.dimensions[2]}_accuracy{self.accuracy}_startingVector{self.startingVector[0]}_{self.startingVector[1]}_{self.startingVector[2]}"
        self.csvSaveTarget = f"{self.datastore_target_directory}{self.tableName}.csv"
        self.npSaveTarget = f"{self.datastore_target_directory}{self.tableName}"
        self.Matrix_Array = self.genMatrix()
        self.Matrix_DataFrame = self.updateDataFrame()
        self.database = self.generate_DBengine()
        
        
    def defaultFunction(self, valueArray):
        for v in valueArray:
            print(v)
    def updateDataFrame(self):
        _save = self.get_saveableMatrix()
        dictKeys = {"accuracy": self.accuracy, "dimensions": self.dimensions, "startingVector": self.startingVector, "startingReboundForce": self.startingReboundForce, 
"startingMatrixInteraction": self.startingMatrixInteraction, "updateDFCount": self.updateDFCount, "Matrix_Array": [s["position"] for s in _save], "currentVector": 
[s["currentVector"] for s in _save], "reboundForce": [s["reboundForce"] for s in _save], "matrixInteraction": [s["matrixInteraction"] for s in _save], 
"datastore_target_directory": self.datastore_target_directory, "sqlConnectionString": self.sqlConnectionString}
        _df = pd.DataFrame({ key:pd.Series(value) for key, value in dictKeys.items()})
        self.Matrix_DataFrame = _df
        self.updateDFCount = self.updateDFCount + 1
        print(f"Updated DataFrame {self.updateDFCount} times")
        return _df
    def generate_DBengine(self):
        connection = sqlite3.connect(self.sqlConnectionString)
        # engine = create_engine(f'sqlite:////Users/bigsexy/Desktop/python/books/DashAppFuckkkkJupyterHard/dataBank/{self.databaseName}.db')
        return connection
    def saveToDatabase(self):
        np.savez(self.npSaveTarget, matrix=self.Matrix_Array, dimensions=self.dimensions, startingVector=self.startingVector)
        self.Matrix_DataFrame.to_csv(self.csvSaveTarget)
        print('Saved to Database')
        return
    def genMatrix(self, _print=False):
        vals = []
        _x = np.linspace(-self.radius[1], self.radius[0], self.accuracy)
        _y = np.linspace(-self.radius[1], self.radius[1], self.accuracy)
        _z = np.linspace(-self.radius[2], self.radius[2], self.accuracy)
        for x in _x:
            for y in _y:
                for z in _z:
                    pointScaleAdjusted = (self.radius[0] / self.accuracy)
                    flushRadius = np.divide(np.multiply(self.radius, 2), self.accuracy)  * self.pointScaleFactor
                    _keanu = KeanuPoint([x, y, z], self.startingVector, self.startingReboundForce, self.startingMatrixInteraction, pointScaleAdjusted, flushRadius, 
self.startingColorValue, self.startingLineColorValue, self.startingOpacity)
                    vals.append(_keanu)
        return np.array(vals)
    def get_saveableMatrix(self):
        __vals = [_p.returnSaveable() for _p in self.Matrix_Array]
        return np.array(__vals)
    def get_PositionArray(self):
        __vals = [_p.getCurrent_Position() for _p in self.Matrix_Array]
        return np.column_stack(__vals)
    def get_OpacityArray(self):
        __vals = [_p.getCurrent_Opacity() for _p in self.Matrix_Array]
        return np.array(__vals)
    def get_ColorArray(self):
        __vals = [_p.getCurrent_ColorValue() for _p in self.Matrix_Array]
        return np.array(__vals)
    def get_Line_ColorArray(self):
        __vals = [_p.getCurrent_Line_ColorValue() for _p in self.Matrix_Array]
        return np.array(__vals)
    def get_SizeArray(self):
        __vals = [_p.getCurrent_Size() for _p in self.Matrix_Array]
        return np.array(__vals)
    def get_FlushRadiusArray(self):
        __vals = [_p.get_FlushRadius() for _p in self.Matrix_Array]
        return np.array(__vals)
    def describe(self):
        return self.Matrix_DataFrame.describe()
    def head(self, __n=10):
        for n in range(__n):
            self.Matrix_Array[n].log()
    def tail(self, __n=10):
        for n in range(__n):
            print(self.Matrix_Array.shape[0] - (n + 1))
            print(self.Matrix_Array[self.Matrix_Array.shape[0] - (n + 1)])
    def print_Details(self):
        printValues = ["Dimensions: ", self.dimensions, "Starting Vector: ", self.startingVector, "Starting Rebound: ", self.startingReboundForce, "Starting Matrix Interaction: ", self.startingMatrixInteraction, "Accuracy: ", self.accuracy]
        for _p in printValues:
            print(_p)
    def print_Matrix(self):
        print("Matrix Size: ")
        print(self.Matrix_Array.size)
        print("Matrix Shape: ")
        print(self.Matrix_Array.shape)
        for _m in self.Matrix_Array:
            print(_m)
    def get_SphericalTraceArray(self):
        __vals = [_p.get_sphericalTrace() for _p in self.Matrix_Array]
        return __vals
    def plot_Scatter3d(self):
        fig = go.Figure()
        points = self.get_PositionArray()
        sizes = self.get_SizeArray() if not self.matrixFlush else self.get_FlushRadiusArray()
        lineColors = self.get_Line_ColorArray()
        _colors = self.get_ColorArray()
        _opacities = self.get_OpacityArray()
        sphericalDistance = [c.get_Distance([0, 0, 0]) for c in self.Matrix_Array]
        fig.add_trace(go.Scatter3d(
        x=points[0],
        y=points[1],
        z=points[2],
        mode='markers',
        marker=dict(
        autocolorscale=False,
        cauto=False,
        cmax=_colors.max(),
        cmin=_colors.min(),
        color=_colors,
        size=sizes,
        sizemode="area",
        # size=36,
        colorscale='Plasma',
        opacity=self.startingOpacity,
        line=dict(
            # color='purple',
            autocolorscale=False,
            cauto=False,
            cmax=lineColors.max(),
            cmin=lineColors.min(),
            color=lineColors,
            width=3
            ),
        )))
        fig.update_layout(
        title='$\\text{Matrix } \Omega$', autosize=True,
                            height=700,
                            margin=dict(l=65, r=50, b=65, t=90),
                            scene=dict(
                                xaxis_title='x',
                                yaxis_title="y",
                                zaxis_title="z",
                                aspectmode='manual',
                                xaxis = dict(nticks=int(self.radius[0] * 4), range=[-self.radius[0] - self.gridPadding, self.radius[0] + self.gridPadding]),
                                yaxis = dict(nticks=int(self.radius[1] * 4), range=[-self.radius[1] - self.gridPadding, self.radius[1] + self.gridPadding]),
                                zaxis = dict(nticks=int(self.radius[2] * 4), range=[-self.radius[2] - self.gridPadding, self.radius[2] + self.gridPadding]),
                                aspectratio=dict(x=1, y=1, z=1),
                            ),
                            hoverlabel=dict(
                                align="auto",
                                bgcolor="#651fff",
                            ),
                        )
        return fig
    # BUG: (unfinished) Plot as series of spherical traces:
    def plot_sphericalTraces(self):
        print("This method is unfinished")
        fig = go.Figure()
        points = self.get_PositionArray()
        sizes = self.get_SizeArray() if not self.matrixFlush else self.get_FlushRadiusArray()
        lineColors = self.get_Line_ColorArray()
        _colors = self.get_ColorArray()
        # print("_colors.max()")
        # print(_colors)
        _opacities = self.get_OpacityArray()
        sphericalDistance = [c.get_Distance([0, 0, 0]) for c in self.Matrix_Array]
        sphericalTraces = self.get_SphericalTraceArray()
        for _s in sphericalTraces:
            fig.add_trace(_s)
        fig.update_layout(
        title='$\\text{Matrix } \Omega$', autosize=True,
                            height=700,
                            margin=dict(l=65, r=50, b=65, t=90),
                            scene=dict(
                                xaxis_title='x',
                                yaxis_title="y",
                                zaxis_title="z",
                                aspectmode='manual',
                                xaxis = dict(nticks=int(self.radius[0] * 4), range=[-self.radius[0] - self.gridPadding, self.radius[0] + self.gridPadding]),
                                yaxis = dict(nticks=int(self.radius[1] * 4), range=[-self.radius[1] - self.gridPadding, self.radius[1] + self.gridPadding]),
                                zaxis = dict(nticks=int(self.radius[2] * 4), range=[-self.radius[2] - self.gridPadding, self.radius[2] + self.gridPadding]),
                                aspectratio=dict(x=1, y=1, z=1),
                            ),
                            hoverlabel=dict(
                                align="auto",
                                bgcolor="#651fff",
                            ),
                        )
        return fig
    def plot_matplotlib3dScatter(self):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        points = self.get_PositionArray()
        colors = self.get_ColorArray()
        # s = points[2] / ((points[1] * 0.01) ** 2)
        sizes = self.get_SizeArray() if not self.matrixFlush else self.get_FlushRadiusArray()
        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        ax = plt.axes(projection="3d")
        print(sizes)
        ax.scatter(points[1], points[2], points[0], s=sizes, c=colors, cmap='copper')
        # ax2 = fig.add_subplot(211, project="3d")
        # pcm = ax[0].pcolor(points[0], points[1], points[2],
        #            norm=colors.LogNorm(vmin=colors.min(), vmax=colors.max()),
        #            cmap='PuBu_r', shading='auto')
        # fig.colorbar(pcm, ax=ax[0], extend='max')        
        # pcm = ax[1].pcolor(points[0], points[1], points[2], cmap='PuBu_r', shading='auto')
        # fig.colorbar(pcm, ax=ax[1], extend='max')
        # plt.show()
        plt.show()
        return plt
    # def applyInverseSquareForce(self, originPoint, forceFunction=defaultFunction):