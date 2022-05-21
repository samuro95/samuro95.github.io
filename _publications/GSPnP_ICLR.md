---
title: "Gradient Step Denoiser for convergent Plug-and-Play"
collection: publications
permalink: 
date: 2021-10-06
venue: 'ICLR 2022'
paperurl: 'https://openreview.net/pdf?id=fPhKeld3Okz'
---
Plug-and-Play methods constitute a class of iterative algorithms for imaging problems where regularization is performed by an off-the-shelf denoiser. Although Plug-and-Play methods can lead to tremendous visual performance for various image problems, the few existing convergence guarantees are based on unrealistic (or suboptimal) hypotheses on the denoiser, or limited to strongly convex data terms. In this work, we propose a new type of Plug-and-Play methods, based on half-quadratic splitting, for which the denoiser is realized as a gradient descent step on a functional parameterized by a deep neural network. Exploiting convergence results for proximal gradient descent algorithms in the non-convex setting, we show that the proposed Plug-and-Play algorithm is a convergent iterative scheme that targets stationary points of an explicit global functional. Besides, experiments show that it is possible to learn such a deep denoiser while not compromising the performance in comparison to other state-of-the-art deep denoisers used in Plug-and-Play schemes. We apply our proximal gradient algorithm to various ill-posed inverse problems, e.g. deblurring, super-resolution and inpainting. For all these applications, numerical results empirically confirm the convergence results. Experiments also show that this new algorithm reaches state-of-the-art performance, both quantitatively and qualitatively. 

Recommended citation: 
```
@inproceedings{
hurault2022gradient,
title={Gradient Step Denoiser for convergent Plug-and-Play},
author={Samuel Hurault and Arthur Leclaire and Nicolas Papadakis},
booktitle={International Conference on Learning Representations},
year={2022},
url={https://openreview.net/forum?id=fPhKeld3Okz}
}
```
