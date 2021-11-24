#!/usr/bin/env python
# coding: utf-8

# # Remote Functions: Tasks
# 
# - add `@ray.remote` decorator on a regular Python function
# - properties: _data independence_, _stateless_
# - patterns: [Task Parallelism](https://patterns.eecs.berkeley.edu/?page_id=208), [Task Graph](https://patterns.eecs.berkeley.edu/?page_id=609)

# ## Initializing Ray
# 
# Before your code can take advantage of Ray, you must initialize it, specifying any resources you want to use and runtime options.
# 

# In[1]:


import ray
import logging
import time

# Start Ray. If you're connecting to an existing cluster, you would use ray.init(address=<cluster-address>) instead.
ray.init(
    num_cpus=4,
    num_gpus=1,
    resources={'Custom': 2},
    ignore_reinit_error=True,
    logging_level=logging.ERROR,
)
ray.cluster_resources()                    # get the cluster resources


# ## Remote functions (Tasks)
# 
# Simply add a decorator to a normal Python function to indicate that it can be run remotely. It must be stateless (i.e., it does not maintain state between calls). It can take arguments and return values, which are really special object refs (futures) that must be accessed with `ray.get`.
# 

# In[3]:


# A regular Python function can be decorated with @ray.remote
@ray.remote
def f(x):
    return x * x

# The function can be invoked by using the `remote` method
futures = [f.remote(i) for i in range(4)]

# The values it returns can be collected using the `get` method.
result = ray.get(futures)
print(f"{result}")
assert result == [0, 1, 4, 9]


# ## Parallel execution
# 
# Parallel task execution and blocking on futures (object refs).
# 

# In[6]:


# A function simulating a more interesting computation that takes one second.
@ray.remote
def slow_function(i):
    time.sleep(1)
    return i

start_time = time.perf_counter()

results = []
for i in range(4):
  results.append(slow_function.remote(i))

loop_duration = time.perf_counter() - start_time
print(f"{loop_duration=:.3f} seconds")

results = ray.get(results)
print(f"{results=}")

assert results == [0, 1, 2, 3]

duration = time.perf_counter() - start_time
print(f"{duration=:.3f} seconds")


# ```{admonition} Profiling
# :class: tip
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
# **NOTE**: The timeline visualization will only work in **Chrome**.
# ```
# 

# In[5]:


ray.timeline(filename="output/task_parallel_ex_2.json")


# ## Passing object refs to remote functions
# 
# Passing object refs between tasks.
# 

# In[7]:


@ray.remote
def my_function():
    return 1

@ray.remote
def function_with_an_argument(value):
    return value + 1

obj_ref1 = my_function.remote()
result = ray.get(obj_ref1)
print(f"{result=}")
assert result == 1

# You can pass an object ref as an argument to another Ray remote function.
obj_ref2 = function_with_an_argument.remote(obj_ref1)
result = ray.get(obj_ref2)
print(f"{result=}")
assert result == 2


# ## Task dependencies
# 
# Tasks can also depend on other tasks. Below, the multiply_matrices task uses the outputs of the two create_matrix tasks, so it will not begin executing until after the first two tasks have executed. The outputs of the first two tasks will automatically be passed as arguments into the third task and the futures will be replaced with their corresponding values). In this manner, tasks can be composed together with arbitrary [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) dependencies.

# In[3]:


import numpy as np

@ray.remote
def create_matrix(size):
    return np.random.normal(size=size)

@ray.remote
def multiply_matrices(x, y):
    return np.dot(x, y)

x_id = create_matrix.remote([1000, 1000])
y_id = create_matrix.remote([1000, 1000])
z_id = multiply_matrices.remote(x_id, y_id)

# Get the results.
z = ray.get(z_id)
print(f"{z=}")


# ## Specifying required resources
# 
# Ray also allows specifying a task’s resources requirements (e.g., CPU, GPU, and custom resources). The task will only run on a machine if there are enough resources available to execute the task.

# In[3]:


# Specify required resources.
@ray.remote(num_cpus=4, num_gpus=2)
def my_function():
    return 1


# ## Multiple returns
# 
# Python remote functions can return multiple object refs.
# 

# In[8]:


@ray.remote(num_returns=3)
def return_multiple():
    return 1, 2, 3

a, b, c = return_multiple.remote()
result = ray.get([a, b, c])
print(f"{result=}")
assert result == [1, 2, 3]


# ## Cancelling tasks
# 
# Remote functions can be cancelled by calling `ray.cancel` on the returned object ref.  Remote actor functions can be stopped by using the `ray.kill` interface.

# In[5]:


@ray.remote
def blocking_operation():
    time.sleep(10e6)

obj_ref = blocking_operation.remote()
ray.cancel(obj_ref)

from ray.exceptions import TaskCancelledError

try:
    ray.get(obj_ref)
except TaskCancelledError:
    print("Object reference was cancelled.")


# ## References
# 
# - [Ray Core Walkthrough: Remote functions (Tasks)](https://docs.ray.io/en/latest/walkthrough.html#remote-functions-tasks)
# - [Ray Internals: A Peek at `ray.get` - Stephanie Wang, Anyscale](https://www.youtube.com/watch?v=a1kNnQu6vGw)
# - [Ray Internals: Object Management with the Ownership Model](https://youtu.be/1oSBxTayfJc) ([slides](https://speakerdeck.com/anyscale/ray-internals-object-management-with-the-ownership-model-stephanie-wang-and-yi-cheng-anyscale))
# - [Patterns for Parallel Programming](https://www.goodreads.com/book/show/85053.Patterns_for_Parallel_Programming)
# 
