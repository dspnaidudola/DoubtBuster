# Machine Learning: Optimization & Gradient Descent
**Course:** CS302 - Foundations of Machine Learning

## 1. Objective Function
In supervised learning, we define an empirical loss function L(w) over the training dataset:
$$L(w) = \frac{1}{n} \sum_{i=1}^n \ell(f(x_i; w), y_i)$$

For linear regression, we typically employ the Mean Squared Error (MSE):
$$MSE(w) = \frac{1}{2n} \sum_{i=1}^n (w^T x_i - y_i)^2$$

## 2. Gradient Descent Update Rule
Gradient descent updates the weight vector w in the opposite direction of the gradient:
$$w := w - \alpha \nabla_w L(w)$$

Where:
- $w$ is the parameter vector.
- $\alpha > 0$ is the learning rate hyperparameter.
- $\nabla_w L(w)$ is the vector of partial derivatives with respect to each weight.

## 3. Learning Rate Effects
- **Optimal Learning Rate:** Smooth convergence toward the minimum.
- **Excessively Large $\alpha$:** Overshooting the minimum, leading to oscillation or divergence.
- **Excessively Small $\alpha$:** Very slow training convergence requiring thousands of epochs.
