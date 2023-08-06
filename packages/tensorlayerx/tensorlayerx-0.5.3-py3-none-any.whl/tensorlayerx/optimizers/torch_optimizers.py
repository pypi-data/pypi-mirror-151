#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import torch.optim as optimizer

__all__ = ['Adadelta', 'Adagrad', 'Adam', 'Adamax', 'Ftrl', 'Nadam', 'RMSprop', 'SGD', 'Momentum', 'Lamb', 'LARS']


class Adadelta(object):

    def __init__(
        self,
        lr=0.001,
        rho=0.95,
        eps=1e-10,
        weight_decay=0.0,
        grad_clip=None,
    ):
        self.learn_rate = lr
        self.rho = rho
        self.eps = eps
        self.init_optim = False
        self.weight_decay = weight_decay
        self.grad_clip = grad_clip

    def apply_gradients(self, grads_and_vars=None):
        if not self.init_optim:
            raise AttributeError("Can not apply gradients before zero_grad call.")
        self.optimizer_adadelta.step()

    def gradient(self, loss, weights=None, return_grad=True):
        if weights is None:
            raise AttributeError("Parameter train_weights must be entered.")
        if not self.init_optim:
            self.optimizer_adadelta = optimizer.Adadelta(
                params=weights, lr=self.learn_rate, rho=self.rho, eps=self.eps, weight_decay=self.weight_decay
            )
            self.init_optim = True
        self.optimizer_adadelta.zero_grad()
        loss.backward()

        if self.grad_clip is not None:
            self.grad_clip(weights)

        if return_grad ==True:
            return _grads(weights)
        else:
            return None


class Adagrad(object):

    def __init__(
        self,
        lr=0.001,
        initial_accumulator_value=0.1,
        eps=1e-10,
        weight_decay=0.0,
        grad_clip=None,
    ):
        self.learn_rate = lr
        self.initial_accumulator_value = initial_accumulator_value
        self.eps = eps
        self.init_optim = False
        self.weight_decay = weight_decay
        self.grad_clip = grad_clip

    def apply_gradients(self, grads_and_vars=None):
        if not self.init_optim:
            raise AttributeError("Can not apply gradients before zero_grad call.")
        self.optimizer_adagrad.step()

    def gradient(self, loss, weights=None, return_grad=True):
        if weights is None:
            raise AttributeError("Parameter train_weights must be entered.")
        if not self.init_optim:
            self.optimizer_adagrad = optimizer.Adagrad(
                params=weights, lr=self.learn_rate, lr_decay=self.initial_accumulator_value,
                weight_decay=self.weight_decay
            )
            self.init_optim = True
        self.optimizer_adagrad.zero_grad()
        loss.backward()

        if self.grad_clip is not None:
            self.grad_clip(weights)

        if return_grad ==True:
            return _grads(weights)
        else:
            return None


class Adam(object):

    def __init__(
        self,
        lr=0.001,
        beta_1=0.9,
        beta_2=0.999,
        eps=1e-8,
        weight_decay=0.0,
        grad_clip=None,
    ):
        self.learn_rate = lr
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.eps = eps
        self.init_optim = False
        self.weight_decay = weight_decay
        self.grad_clip = grad_clip

    def apply_gradients(self, grads_and_vars=None):
        if not self.init_optim:
            raise AttributeError("Can not apply gradients before zero_grad call.")
        self.optimizer_adam.step()

    def gradient(self, loss, weights=None, return_grad=True):
        if weights is None:
            raise AttributeError("Parameter train_weights must be entered.")
        if not self.init_optim:
            self.optimizer_adam = optimizer.Adam(
                params=weights, lr=self.learn_rate, betas=(self.beta_1, self.beta_2), eps=self.eps,
                weight_decay=self.weight_decay
            )
            self.init_optim = True
        self.optimizer_adam.zero_grad()
        loss.backward()

        if self.grad_clip is not None:
            self.grad_clip(weights)

        if return_grad ==True:
            return _grads(weights)
        else:
            return None


class Adamax(object):

    def __init__(
        self,
        lr=0.001,
        beta_1=0.9,
        beta_2=0.999,
        eps=1e-8,
        weight_decay=0.0,
        grad_clip=None,
    ):
        self.lr = lr
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.eps = eps
        self.init_optim = False
        self.weight_decay = weight_decay
        self.grad_clip = grad_clip

    def apply_gradients(self, grads_and_vars=None):
        if not self.init_optim:
            raise AttributeError("Can not apply gradients before zero_grad call.")
        self.optimizer_adamax.step()

    def gradient(self, loss, weights=None, return_grad=True):
        if weights is None:
            raise AttributeError("Parameter train_weights must be entered.")
        if not self.init_optim:
            self.optimizer_adamax = optimizer.Adamax(
                params=weights, lr=self.lr, betas=(self.beta_1, self.beta_2), eps=self.eps,
                weight_decay=self.weight_decay
            )
            self.init_optim = True
        self.optimizer_adamax.zero_grad()
        loss.backward()

        if self.grad_clip is not None:
            self.grad_clip(weights)

        if return_grad ==True:
            return _grads(weights)
        else:
            return None


class Ftrl(object):

    def __init__(self):
        raise NotImplementedError("Ftrl optimizer is not implemented")

    def apply_gradients(self):
        pass

    def gradient(self, train_weights=None):
        pass


class Nadam(object):

    def __init__(self):
        raise NotImplementedError("Nadam optimizer is not implemented")

    def apply_gradients(self):
        pass

    def gradient(self, train_weights=None):
        pass


class RMSprop(object):

    def __init__(
        self,
        lr=0.001,
        rho=0.99,
        momentum=0.0,
        eps=1e-08,
        centered=False,
        weight_decay=0.0,
        grad_clip=None,
    ):
        self.learn_rate = lr
        self.rho = rho
        self.momentum = momentum
        self.eps = eps
        self.centered = centered
        self.init_optim = False
        self.weight_decay = weight_decay
        self.grad_clip = grad_clip

    def apply_gradients(self, grads_and_vars=None):
        if not self.init_optim:
            raise AttributeError("Can not apply gradients before zero_grad call.")
        self.optimizer_rmsprop.step()

    def gradient(self, loss, weights=None, return_grad=True):
        if weights is None:
            raise AttributeError("Parameter train_weights must be entered.")
        if not self.init_optim:
            self.optimizer_rmsprop = optimizer.RMSprop(
                params=weights, lr=self.learn_rate, alpha=self.rho, eps=self.eps, momentum=self.momentum,
                centered=self.centered, weight_decay=self.weight_decay
            )
            self.init_optim = True
        self.optimizer_rmsprop.zero_grad()
        loss.backward()

        if self.grad_clip is not None:
            self.grad_clip(weights)

        if return_grad ==True:
            return _grads(weights)
        else:
            return None


class SGD(object):

    def __init__(
        self,
        lr=0.001,
        momentum=0,
        weight_decay=0.0,
        grad_clip=None,
    ):
        self.learn_rate = lr
        self.momentum = momentum
        self.init_optim = False
        self.weight_decay = weight_decay
        self.grad_clip = grad_clip

    def apply_gradients(self, grads_and_vars=None):
        if not self.init_optim:
            raise AttributeError("Can not apply gradients before zero_grad call.")
        self.optimizer_sgd.step()

    def gradient(self, loss, weights=None, return_grad=True):
        if weights is None:
            raise AttributeError("Parameter train_weights must be entered.")
        if not self.init_optim:
            self.optimizer_sgd = optimizer.SGD(
                params=weights, lr=self.learn_rate, momentum=self.momentum, weight_decay=self.weight_decay
            )
            self.init_optim = True
        self.optimizer_sgd.zero_grad()
        loss.backward()

        if self.grad_clip is not None:
            self.grad_clip(weights)

        if return_grad ==True:
            return _grads(weights)
        else:
            return None


class Momentum(object):

    def __init__(
        self,
        lr=0.001,
        momentum=0,
        weight_decay=0.0,
        grad_clip=None,
    ):
        self.learn_rate = lr
        self.momentum = momentum
        self.init_optim = False
        self.weight_decay = weight_decay
        self.grad_clip = grad_clip

    def apply_gradients(self, grads_and_vars=None):
        if not self.init_optim:
            raise AttributeError("Can not apply gradients before zero_grad call.")
        self.optimizer_momentum.step()

    def gradient(self, loss, weights=None, return_grad=True):
        if weights is None:
            raise AttributeError("Parameter train_weights must be entered.")
        if not self.init_optim:
            self.optimizer_momentum = optimizer.SGD(
                params=weights, lr=self.learn_rate, momentum=self.momentum, weight_decay=self.weight_decay
            )
            self.init_optim = True
        self.optimizer_momentum.zero_grad()
        loss.backward()

        if self.grad_clip is not None:
            self.grad_clip(weights)

        if return_grad ==True:
            return _grads(weights)
        else:
            return None


def Lamb(**kwargs):
    raise Exception('Lamb optimizer function not implemented')


def LARS(**kwargs):
    raise Exception('LARS optimizer function not implemented')


def _grads(weights):
    grads = []
    for w in weights:
        grads.append(w.grad)
    return grads
