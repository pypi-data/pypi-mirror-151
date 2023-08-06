import asyncio
import numpy as np
import uvloop
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path


class IchikaUtils:
    def __init__(self):
        self.self = self
        
    async def calcMean(self, array: list):
        a = np.array(array)
        return np.mean(a)
    
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def calcStats(self, array: list):
        npyArray = np.array(array)
        return {"mean": np.mean(npyArray), "median": np.median(npyArray), "std": np.std(npyArray), "variances": np.var(npyArray)
                , "spread": np.ptp(npyArray)}
    
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def calc2VarStats(self, xList: list):
        xListArray = np.array(xList)
        rowShape = xListArray[:, np.newaxis]
        return rowShape.shape
        
    async def graphHistoRandn(self, amount: int):
        fig, ax = plt.subplots()

# Fixing random state for reproducibility
        np.random.seed(19680801)


# histogram our data with numpy
        n, bins = np.histogram(amount, 50)
        
        left = bins[:-1]
        right = bins[1:]
        bottom = np.zeros(len(left))
        top = bottom + n


        # we need a (numrects x numsides x 2) numpy array for the path helper
        # function to build a compound path
        XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

        # get the Path object
        barpath = path.Path.make_compound_path_from_polys(XY)

        # make a patch out of it
        patch = patches.PathPatch(barpath)
        ax.add_patch(patch)

        # update the view limits
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), top.max())

        plt.show()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def graphSetHistogram(self, data: list):
# for one dimensional data
        fig, ax = plt.subplots()

        (hist, bin_edges) = np.histogram(data)
        left = bin_edges[:-1]
        right = bin_edges[1:]
        bottom = np.zeros(len(left))
        top = bottom + hist


        # we need a (numrects x numsides x 2) numpy array for the path helper
        # function to build a compound path
        XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

        # get the Path object
        barpath = path.Path.make_compound_path_from_polys(XY)

        # make a patch out of it
        patch = patches.PathPatch(barpath)
        ax.add_patch(patch)

        # update the view limits
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), top.max())

        plt.show()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())        
        
        
    
    
    
    
