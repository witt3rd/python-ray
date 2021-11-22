# Learning Ray

## The Cloud Native Distributed Computing Platform

1. A simple and flexible framework for distributed cloud computing
   - Simple: simple annotation to make functions & classes distribute.
   - Flexible: create new distributed function calls & instances. No batching required.
2. A cloud-provider independent compute launcher/autoscaler
3. An ecosystem of distributed computation libraries build with #1

## How does it "fit" with ML?

[3rd generation ML architecture](https://www.anyscale.com/blog/the-third-generation-of-production-ml-architectures): tackling the problem of production ML architecure by making it programmable.

Moves the focus to libraries instead of worried about distributed computation and underlying clusters.

## A simpler way to build 1st/2nd generation ML pipelines

- Flexibility of a programming language to define pipelines
- More easily allows for shared components (e.g., feature transformation during training vs real-time)
- "Out of the box" support for distributed ML

## References

Primary links:

- [ray.io](https://www.ray.io/)
- [docs.ray.io](https://docs.ray.io/)
- [github/ray-project](github.com/ray-project/ray)

Papers and posts:

- [Cloud Programming Simplified: A Berkeley View on Serverless Computing](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2019/EECS-2019-3.pdf)
- [Ray 1.x Architecture](https://docs.google.com/document/d/1lAy0Owi-vPz2jEqBSaHNQcy2IBSDEHyXNOQZlGuj93c/preview)
- [Modern Parallel and Distributed Python: A Quick Tutorial on Ray](https://towardsdatascience.com/modern-parallel-and-distributed-python-a-quick-tutorial-on-ray-99f8d70369b8)
- [Combine the development experience of a laptop with the scale of the cloud](https://gradientflow.com/combine-the-development-experience-of-a-laptop-with-the-scale-of-the-cloud/)

Videos:

- [Ray Core Tutorial](https://youtu.be/_KOlq2C-568) ([source code](https://github.com/derwenai/ray_tutorial)) ([slides](papers/Ray_Core_Tutorial.pdf))
