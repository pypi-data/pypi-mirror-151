import numpy as np
import asyncio
import uvloop

class StandardDeviationCalc:
    def __init__(self):
        self.self = self
    
    async def stdCalc(self, data: list):
        """Calculates the standard deviation of the data

        Args:
            data (list): list of data

        Returns:
            _type_: float
        """
        npArr = np.array(data)
        return np.std(npArr)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
