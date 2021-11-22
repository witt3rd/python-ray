#!/usr/bin/env python
# coding: utf-8

# # Pattern: task-parallel (remote functions)
# 
# - add `@ray.remote` decorator on a regular Python function
# - properties: _data independence_, _stateless_
# - patterns: [Task Parallelism](https://patterns.eecs.berkeley.edu/?page_id=208), [Task Graph](https://patterns.eecs.berkeley.edu/?page_id=609)
# - [Ray Internals: A Peek at `ray.get` - Stephanie Wang, Anyscale](https://www.youtube.com/watch?v=a1kNnQu6vGw)
# - [Ray Internals: Object Management with the Ownership Model](https://youtu.be/1oSBxTayfJc) ([slides](https://speakerdeck.com/anyscale/ray-internals-object-management-with-the-ownership-model-stephanie-wang-and-yi-cheng-anyscale))
# - reference: [Patterns for Parallel Programming](https://www.goodreads.com/book/show/85053.Patterns_for_Parallel_Programming)

# In[1]:


import ray
import logging
import time

# Start Ray. If you're connecting to an existing cluster, you would use
# ray.init(address=<cluster-address>) instead.
ray.init(
    num_cpus=4,
    ignore_reinit_error=True,              # Don't print error messages if a Ray instance is already running. Attach to it
    logging_level=logging.ERROR,           
)
ray.cluster_resources()                    # get the cluster resources


# ## Example 1
# 
# Simple remote function (task).

# In[6]:


# A regular Python function can be decorated with @ray.remote
@ray.remote
def f(x):
    return x * x

# The function can be invoked by using the `remote` method
futures = [f.remote(i) for i in range(4)]

# The values it returns can be collected using the `get` method.
print(ray.get(futures))  # [0, 1, 4, 9]


# ## Example 2
# 
# Parallel task execution and blocking on futures (object refs).

# In[23]:


# A function simulating a more interesting computation that takes one second.
@ray.remote
def slow_function(i):
    time.sleep(1)
    return i

start_time = time.perf_counter()

results = []
for i in range(4):
  results.append(slow_function.remote(i))

duration = time.perf_counter() - start_time
print('Executing the for loop took {:.3f} seconds.'.format(duration))

results = ray.get(results)
print('The results are:', results)

assert results == [0, 1, 2, 3], 'Did you remember to call ray.get?'

duration = time.perf_counter() - start_time
print('Executing the example took {:.3f} seconds.'.format(duration))


# ## Exercise 
# 
# Use the UI to view the task timeline and to verify that the four tasks were executed in parallel. You can do this as follows.
# 
# 1. Run the following cell to generate a JSON file containing the profiling data.
# 2. Download the timeline file by right clicking on `task_parallel_ex_2.json` in the **Files** tab in the navigator to the left, right clicking, and selecting  **"Download"**.
# 3. Enter **chrome://tracing** into the Chrome web browser, click on the **"Load"** button, and select the downloaded JSON file.
# 
# To navigate within the timeline:
# - Move around by clicking and dragging.
# - Zoom in and out by holding **alt** on Windows or **option** on Mac and scrolling.
# 
# **NOTE:** The timeline visualization will only work in **Chrome**.

# In[5]:


ray.timeline(filename="output/task_parallel_ex_2.json")


# ## Example 3
# 
# Passing object refs between tasks.

# In[ ]:


@ray.remote
def my_function():
    return 1

@ray.remote
def function_with_an_argument(value):
    return value + 1

obj_ref1 = my_function.remote()
assert ray.get(obj_ref1) == 1

# You can pass an object ref as an argument to another Ray remote function.
obj_ref2 = function_with_an_argument.remote(obj_ref1)
assert ray.get(obj_ref2) == 2

