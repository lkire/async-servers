"""Two async loops. Why?

This module solves a problem: if an async server is running but doesn't
want to be touched, how do you do async programming?

The solution is to start another async loop and put it in a thread.
Now you have to consider race conditions between loops but not within,
so something has been achieved.
"""

import asyncio

from functools import partial
from random import random
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()

async def update(x, y):
    source.stream({
        'x' : [x],
        'y' : [y],
    })
    

import threading
lock = threading.Lock()

async def point_production():
    while True:
        # do some blocking computation
        await asyncio.sleep(0.1)
        x, y = random(), random()
        # but update the document from callback
        lock.acquire()
        try:
            doc.add_next_tick_callback(partial(update, x=x, y=y))
        finally:
            lock.release()
            
def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(point_production())

loop = asyncio.new_event_loop()
t = threading.Thread(target=loop_in_thread, args=(loop,))
t.start()

p = figure(x_range=[0, 1], y_range=[0,1], sizing_mode='stretch_both')
l = p.circle(x='x', y='y', source=source)
p.toolbar.logo = None
doc.add_root(p)

