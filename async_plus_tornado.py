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

#This background threading of an asyncio loop is a really nice organization.
#It is not necessary here but other tools require an asyncio loop
#but so does bokeh 5.0+ so there is a conflict that is resolved here.
#The fact that this works is probably also the solution for nearly
#every async upgrade headache python 3.4,5,6 -> 3.7
#The lock works great in this environment!
t = threading.Thread(target=loop_in_thread, args=(loop,))
t.start()

p = figure(x_range=[0, 1], y_range=[0,1], sizing_mode='stretch_both')
l = p.circle(x='x', y='y', source=source)
p.toolbar.logo = None
#, output_backend="webgl"
doc.add_root(p)

