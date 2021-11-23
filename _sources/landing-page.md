# The Cloud Native Distributed Computing Platform

- [ray.io](https://www.ray.io/) ([docs](https://docs.ray.io/)) ([source](http://github.com/ray-project/ray))
- [Anyscale Academy](https://github.com/anyscale/academy)

![The Ray Vision](images/ray_vision.png)

## Ray is:

1. A simple and flexible framework for distributed cloud computing
   - Simple: simple annotation to make functions & classes distribute.
   - Flexible: create new distributed function calls & instances. No batching required.
2. A cloud-provider independent compute launcher/autoscaler
3. An ecosystem of distributed computation libraries build with #1

Ray represents a [3rd generation ML architecture](https://www.anyscale.com/blog/the-third-generation-of-production-ml-architectures): tackling the problem of production ML architecure by making it programmable.

Ray moves the focus to **libraries** instead of worrying about distributed computation and underlying clusters.

Ray provides a simpler way to build 1st/2nd generation ML pipelines:

- Flexibility of a programming language to define pipelines
- More easily allows for shared components (e.g., feature transformation during training vs real-time)
- "Out of the box" support for distributed ML

## Setting Up Your Python Environment

In order to run the cells and the tutorial projects, you will need a Python environment with required dependencies. These are documented in [Python Setup](python_setup.md).

## References

- [Cloud Programming Simplified: A Berkeley View on Serverless Computing](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2019/EECS-2019-3.pdf)
- [Ray 1.x Architecture](https://docs.google.com/document/d/1lAy0Owi-vPz2jEqBSaHNQcy2IBSDEHyXNOQZlGuj93c/preview)
- [Combine the development experience of a laptop with the scale of the cloud](https://gradientflow.com/combine-the-development-experience-of-a-laptop-with-the-scale-of-the-cloud/)
