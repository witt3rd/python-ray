#!/usr/bin/env python
# coding: utf-8

# # Example: Calculating Pi
# 
# This example explores how using the Ray API enables horizontal scalability.

# In[1]:


import ray
import logging
import time

# Start Ray. If you're connecting to an existing cluster, you would use ray.init(address=<cluster-address>) instead.
ray.init(
    num_cpus=4,
    num_gpus=1,
    ignore_reinit_error=True,
    logging_level=logging.ERROR,
)
ray.cluster_resources()                    # get the cluster resources


# ```{note}
# There is a lot of Python code used in this notebook, both for calculating Pi and for the graphs. We won't show most of it, but all the code can be found in this directory, pi_calc.py (calculating $\pi$) and task_lesson_util.py (graphics).
# ```

# In[2]:


from task_lesson_util import make_dmaps, run_simulations, stop_simulations
from pi_calc import str_large_n
import numpy as np
import math, statistics, time
from bokeh_util import two_lines_plot, means_stddevs_plot  # Some plotting utilities in `./bokeh_util.py`.
from bokeh.plotting import show, figure
from bokeh.layouts import gridplot


# Let's estimate $\pi$ (~3.14159) using a Monte Carlo technique, where we randomly sampled a uniform distribution, one with equal probably of picking any point in a square.
# 
# It works like this. Imagine each blue square is a piece of paper 2 meters by 2 meters you put on a wall. The circle inside each one has radius 1 meter.
# 
# Now suppose you throw $N$ darts at each paper. We're seeing $N = {\sim}1000, {\sim}10000, {\sim}100000$ examples. (This will be hard on your wall, so don't try this at home...)
# 
# Some darts will land inside the circle, call them $n$, and the rest will land outside, $N-n$. The area of a circle is ${\pi}r^{2}$ and the area of a square is $(2r)^{2} = 4r^{2}$. The ratio of $n/N$ approximately equals the ratio of the circle area over the square area, ${\pi}r^{2}/4r^{2} = {\pi}/4$. (Does it make sense that this ratio is independent of the actual radius value?).
# 
# In other words,
# 
# $\pi/4 \approx n/N$
# 
# $\pi \approx 4n/N$
# 
# So, to approximate $\pi$, we can count the number of darts thrown and the number that land inside the circle.

# In[3]:


Ns = [1000, 10000, 100000]

dmaps = make_dmaps(Ns)

dmaps[0] + dmaps[1] + dmaps[2]


# In[4]:


run_simulations(dmaps)


# In[5]:


# TIP: If you want to stop them, uncomment and run the next line:
# stop_simulations(dmaps)


# You probably noticed three things while the simulations were running or after they finished:
# 
# The accuracy improved for larger $N$... well usually. Sometimes a lower $N$ simulation gets "lucky" and does as well as a higher $N$. In a real experiment, we would do many runs and then compute the average and standard deviation. (We'll do that below.)
# 
# Because each $N$ is 10 times the $N$ to the left, it took roughly 10 times as long for the second to finish compared to the first, etc.
# 
# The updates in the second and third simulations appeared to go faster as the neighbors to the left finished.
# 
# What this means is that if we really want a good estimate of $\pi$, we have to do runs with large $N$, but then we wait longer. Ideally, to get fast and accurate results, we would do as much work as possible in parallel, leveraging all the CPU cores available on our machine ... or our cluster.
# 
# Let's use Ray to achieve this.

# ## Parallelism with Ray
# 
# We did the previous calculation without fully exploiting all available cores.  In a cluster, the rest of the cores _on the rest of the machines_ would be idle, too.
# 
# We can use Ray to parallelize a lof this work.

# In[6]:


num_workers = 8
trials = 20


# Let's define a function to do the Pi calculation that simplifies the code we used above for graphing purposes. We won't do the "dart graphs" from now on, because they add a lot of overhead that would obscure the performance
# 
# This function estimates $\pi$ for the number of samples requested. It uses [NumPy](https://docs.scipy.org/doc/numpy/index.html). If you're not familiar with it, the implementation details aren't essential to understand, but the comments try to explain them.

# In[7]:


def estimate_pi(num_samples):
    xs = np.random.uniform(low=-1.0, high=1.0, size=num_samples)   # Generate num_samples random samples for the x coordinate.
    ys = np.random.uniform(low=-1.0, high=1.0, size=num_samples)   # Generate num_samples random samples for the y coordinate.
    xys = np.stack((xs, ys), axis=-1)                              # Like Python's "zip(a,b)"; creates np.array([(x1,y1), (x2,y2), ...]).
    inside = xs*xs + ys*ys <= 1.0                                  # Creates a predicate over all the array elements.
    xys_inside = xys[inside]                                       # Selects only those "zipped" array elements inside the circle.
    in_circle = xys_inside.shape[0]                                # Return the number of elements inside the circle.
    approx_pi = 4.0*in_circle/num_samples                          # The Pi estimate.
    return approx_pi


# Let's try it:

# In[8]:


Ns = [10000, 50000, 100000, 500000, 1000000] #, 5000000, 10000000]  # Larger values take a long time on small VMs and machines!
maxN = Ns[-1]
maxN


# In[9]:


fmt = '{:10.5f} seconds: pi ~ {:7.6f}, stddev = {:5.4f}, error = {:5.4f}%'


# In[10]:


def try_it(n, trials):
    print('trials = {:3d}, N = {:s}: '.format(trials, str_large_n(n, padding=12)), end='')   # str_large_n imported above.
    start = time.time()
    pis = [estimate_pi(n) for _ in range(trials)]
    approx_pi = statistics.mean(pis)
    stdev = statistics.stdev(pis)
    duration = time.time() - start
    error = (100.0*abs(approx_pi-np.pi)/np.pi)
    print(fmt.format(duration, approx_pi, stdev, error))   # str_large_n imported above.
    return trials, n, duration, approx_pi, stdev, error


# The next cell will take a few seconds to run.
# 
# ```{note}
# If all the following trials finish in under a few seconds for the largest $n$ value in $Ns$ and the largest number of trials, consider changing $Ns$ above to add larger values.
# ```

# In[11]:


data_ns = [try_it(n, trials) for n in Ns]


# In[12]:


data_trials = [try_it(maxN, trials) for trials in range(5,20,2)]


# (We'll graph the results below.)
# 
# The CPU utilization never gets close to 100%.  On a four-core machine, for example, the number will be about 25%.  (The Ray process meters will stay at or near zero until later in this notebook.)
# 
# So, this runs on one core, while the other corse are idle.  Now we'll try with Ray.

# ## From Python Functions to Ray Tasks
# 
# You create a Ray _task_ by decorating around a normal Python function with `@ray.remote`.  Thee tasks will be scheduled across your Ray cluster (or your laptop CPU cores).
# 
# Here is a Ray task for `estimate_pi`.  All we need is a wrapper around the original function.

# In[13]:


@ray.remote
def ray_estimate_pi(num_samples):
    return estimate_pi(num_samples)


# Let's try it.  To invoke a task, you use `function.remote(args)`.  A Ray task is an asynchronous operation that returns a _future_ called an `ObjectRef` that is used to access the value when the function completes.  We use `ray.get(ref)` to get it.

# In[14]:


ref = ray_estimate_pi.remote(100)
print(ray.get(ref))


# We can also work with a list of refs:

# In[15]:


refs = [ray_estimate_pi.remote(n) for n in [100, 1000, 10000]]
print(ray.get(refs))


# Let's try our test run again with our Ray task.  We'l need a new "try it" function, because of the different task invocation logic.  This function doesn't need to be a Ray task, however, so no `@ray.remote` decorator is required.

# In[16]:


def ray_try_it(n, trials):
    print('trials = {:3d}, N = {:s}: '.format(trials, str_large_n(n, padding=12)), end='')   # str_large_n imported above.
    start = time.time()
    refs = [ray_estimate_pi.remote(n) for _ in range(trials)]
    pis = ray.get(refs)
    approx_pi = statistics.mean(pis)
    stdev = statistics.stdev(pis)
    duration = time.time() - start
    error = (100.0*abs(approx_pi-np.pi)/np.pi)
    print(fmt.format(duration, approx_pi, stdev, error))   # str_large_n imported above.
    return trials, n, duration, approx_pi, stdev, error


# In[17]:


ray_data_ns = [ray_try_it(n, trials) for n in Ns]


# In[18]:


ray_data_trials = [ray_try_it(maxN, trials) for trials in range(5,20,2)]


# The durations should be shorter than the non-Ray numbers.  Let's graph our results and see.  It will be easier if we first convert the `*_data_* lists to NumPy arrays so they are easier to slice.

# In[19]:


np_data_ns         = np.array(data_ns)
np_data_trials     = np.array(data_trials)
np_ray_data_ns     = np.array(ray_data_ns)
np_ray_data_trials = np.array(ray_data_trials)


# First, a linear plot of the results:

# In[20]:


two_lines = two_lines_plot(
    "N vs. Execution Times (Smaller Is Better)", 'N', 'Time', 'No Ray', 'Ray', 
    np_data_ns[:,1], np_data_ns[:,2], np_ray_data_ns[:,1], np_ray_data_ns[:,2],
    x_axis_type='linear', y_axis_type='linear')
show(two_lines, plot_width=800, plot_height=400)


# For relatively small $N$ values, the performance overhead of Ray is a larger percentage of the calculation, so the overall performance benefit is less.  However, as $N$ increases, the advantage of Ray increases.  Both plots are roughly linear, because we are CPU bound, but Ray's execution time/$N$ is lower.  On a full clusster, the times could be dramatically better for larger $N$.
# 
# A log-log plot shows the lower-$N$ behavior more clearly:

# In[21]:


two_lines = two_lines_plot(
    "N vs. Execution Times (Smaller Is Better)", 'N', 'Time', 'No Ray', 'Ray', 
    np_data_ns[:,1], np_data_ns[:,2], np_ray_data_ns[:,1], np_ray_data_ns[:,2])
show(two_lines, plot_width=800, plot_height=400)


# What about execution times as a function of the number of trials for a fixed $N$?

# In[22]:


two_lines = two_lines_plot(
    "Trials (N=10,000,000) vs. Execution Times (Smaller Is Better)", 'Trials', 'Time', 'No Ray', 'Ray', 
    np_data_trials[:,0], np_data_trials[:,2], np_ray_data_trials[:,0], np_ray_data_trials[:,2], 
    x_axis_type='linear', y_axis_type='linear')
show(two_lines, plot_width=800, plot_height=400)


# Let's plot the approximate mean values and the standard deviations over the `num_workers` trials for each $N$:

# In[23]:


pi_without_ray_plot = means_stddevs_plot(
  np_data_ns[:,1], np_data_ns[:,3], np_data_ns[:,4], title = 'π Results without Ray')
# Use a grid to make it layout better.
pi_without_ray_grid = gridplot([[pi_without_ray_plot]], width=1000, height=400)
show(pi_without_ray_grid)


# As you might expect, for low $N$ values, the error bars are large and the mean estimate is poor, but for higher $N$, the errors grow smaller and results converge to the correct value.
# 
# With Ray, the plot will look similar, because w did the same calculation, just faster:

# In[24]:


pi_with_ray_plot = means_stddevs_plot(
  np_ray_data_ns[:,1], np_ray_data_ns[:,3], np_ray_data_ns[:,4], title = 'π Results with Ray')
# Use a grid to make it layout better.
pi_with_ray_grid = gridplot([[pi_with_ray_plot]], width=1000, height=400)
show(pi_with_ray_grid)


# ## ray.get() vs ray.wait()
# 
# Calling `ray.get(ids)` blocks until all the tasks have completed that correspond to the input `ids`.  That has been fine for this tutorial so far, but what if you're waiting for a number of tasks, where some will finish more quickly than others?  What if you would like to process the completed results as they become available, even while other tasks are still running?  That's where `ray.wait()` is recommended.  Here we'll provide a brief example.  For more detailed, see the [Advanced Ray: Tasks Revisited](tasks_advanced.ipynb).

# In[25]:


@ray.remote
def ray_estimate_pi2(n, trial):
    time.sleep(trial)
    return n, trial, estimate_pi(n)


# In[26]:


def ray_try_it2(ns, trials):
    start = time.time()
    refs = [ray_estimate_pi2.remote(n, trial) for trial in trials for n in ns]
    still_running = list(refs)
    while len(still_running) > 0:
        finished, still_running = ray.wait(still_running)
        ns_trials_pis = ray.get(finished)   # won't block
        print(f'{ns_trials_pis}, elapsed time = {time.time() - start} secs')


# In[27]:


ray_try_it2([100000,1000000,1000000], [2,4,6])


# In[28]:


ray.shutdown()  # "Undo ray.init()". Terminate all the processes started in this notebook.


# ## References
# 
# - [Ray Crash Course - Tasks](https://github.com/anyscale/academy/blob/main/ray-crash-course/01-Ray-Tasks.ipynb)
