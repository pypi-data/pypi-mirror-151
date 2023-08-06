# pyundergraduate
This is a module regarding Numerical Analysis with Python comprising the syllabus covered at the undergraduate level in Indian colleges.
# Creator 
Archisman Chakraborti <br>
St. Xavier's College, Kolkata, India

# pyundergraduate
This module is designed on some well known numerical techniques in Python which are commonly taught at the undergraduate college level to students who have taken a course in Computational Physics and Mathematics.

---
## <b>Current version contents:</b>
- <b>Differentiation 
    - Finite differenc</b>es method
      - Forward differences
      - Backward differences
      - Central Differences
    
- <b>Finding roots of linear and non linear equations</b>
  - Newton Raphson method
  - Secant Method
- <b>Numerical Integration</b>
  - Trapezoidal Rule
  - Simpsons one-third rule
  - Simpsons three-eighth rule
  - Composite Integration Rules
    - Composite Trapezoidal Rule
    - Composite Simpson's Rule(Modified Simpsons' one third rule)
- <b>Interpolation</b>
  - Lagrange Interpolation with unequal intervals
  - Newton Forward Interpolation
- <b>Orinary Differential equation Solvers</b>
  - Euler Method for solving ODEs upto 3rd order.
  - Modified Euler method(Runge Kutta 2 Method) for solving ODEs upto 2nd order.
  - Runge Kutta 4 Method for solving ODEs upto 2nd Order.

---
# Example Code and Techniques

## Differentiation 
```python
# Finite differences method
import numpy as np

f = lambda x: np.sin(x)
g = lambda x: np.cos(x)
x_pts = np.linspace(0, 10, 100000)

h = .0005

# Forward differences object
differentiator1_f = FiniteDiff(func= f, h=h)


first_deriv_f = differentiator1_f.Forward_First_Deriv() 
second_deriv_f = differentiator1_f.Forward_Second_Deriv() 
third_deriv_f = differentiator1_f.Forward_Third_Deriv() 
fourth_deriv_f = differentiator1_f.Forward_Fourth_Deriv() 

# Alternately for 'nth' order
# Continue using the 'first deriv' method for consecutive derivatives.

# First derivative
differentiator1_f = FiniteDiff(func= f, h=h)
first_deriv_f = differentiator1_f.Forward_First_Deriv() 

# Second derivative
differentiator2_f = FiniteDiff(func= first_deriv_f, h=h)
second_deriv_f = differentiator2_f.Forward_First_Deriv()

# Third derivative
differentiator3_f = FiniteDiff(func= second_deriv_f, h=h)
third_deriv_f = differentiator3_f.Forward_First_Deriv()

# Fourth derivative
differentiator4_f = FiniteDiff(func= third_deriv_f, h=h)
fourth_deriv_f = differentiator4_f.Forward_First_Deriv()
```
Similarly, for the central difference and the Backward Difference Rules.

---
## Integration
```python
import numpy as np
f = lambda x: x*np.sin(x)
lowerlim = 0
upperlim = 10
intervals = 1000

# Trapezoidal rule
trap_ans = Integration_trapezoidal(f=f, lower_lim=lowerlim, upper_lim=upperlim, intervals=intervals)

# Simpsons one third rule
simp_one_third_ans = Simpson_one_third(f=f, lower_lim=lowerlim, upper_lim=upperlim, intervals=intervals)

# Simpsons three eight rule
simp_three_eight_ans = Simpson_three_eighth(f=f, lower_lim=lowerlim, upper_lim=upperlim, intervals=intervals + 2)

# Composite rules
integrator = CompositeIntegration(func=f, lowerlim=lowerlim, upperlim=upperlim, intervals=intervals)

## Composite Trapezoidal rule
comptrap_ans = integrator.Comp_Trapezoidal_Rule()

## Composite Simpson's rule
compsimp_ans = integrator.Comp_Simpsons_Rule()
```
---
## ODE Solvers

### Solving a 1D ODE

```python
import numpy as np

def dydx(y, x):
    return 1/x
ics1 = [1, 0] # At x = 0, y = 0

# Euler method solutions
y_euler, x_euler = euler(f=dydx, ics=ics1, step_size=0.001, x1=5)

# Modified euler method solutions
y_mod, x_mod = mod_euler(f=dydx, ics=ics1, step_size=0.001, x1=5)

# RK4 solutions
y_rk4, x_rk4 = RK4_solver(f=dydx, ics=ics1, step_size=0.001, x1=5)
```
### Solving a 2D ODE - Equation of a damped harmonis oscillator
```python
def dudt(u, x, t):  # u = dxdt
    b = 0.2  # damping parameter
    k = 20  # Spring constant
    return -b*u - k*x
ics2 = [0, np.pi/50, 0] # At t=0, x = pi/50, vel = 0

# Euler solutions
u_euler, x_euler2, t_euler = euler(f = dudt, ics = ics2, step_size=0.001, x1 = 15)

# Modified euler solutions
u_modeuler, x_modeuler2, t_modeuler = mod_euler(f = dudt, ics = ics2, step_size=0.001, x1 = 15)

# RK4 solutions
u_rk4, x_rk4_2, t_rk4 = RK4_solver(f = dudt, ics = ics2, step_size=0.001, x1 = 15)
```
### Solving a 3rd order ODE using Euler's method
#### RK4 and RK2 methods are under construction
```python
def dvdx(v, u, y, x):
    return 9*v - 15*u - 25*y

# Here, y = dy/dx(1st derivative), v = dv/dx(second derivative)
v, u, y, x = euler(f = dvdx, ics = [0, np.pi/50, 0, 1], step_size = 0.005, x1 = 5)
```
---
## Finding root of linear, non linear and transcendal equations numerically.
```python
def func1(x):
    return x**2 + 4*x + 4
def deriv1(x):
    return 2*x + 2

# Secant method
root_finder = SecantMethod(func = func1, guess1=-5, guess2 = -3, iterations=20000, tolerance=0.00000001)
print(f'Secant root = {root_finder.solve()}')
required_iterations = root_finder.required_iterations
print(required_iterations

# Newton Raphson Method
sol_newton = NewtonRaphson(f = func1, f_deriv= deriv1, x0 = 1, error = 0.0000000001, iterations=20000)
```
---
## Interpolation

```python
# Lagrange Interpolation
def func(x):
        return np.sin(x)

# xlist doesn't need to be evenly spaced
x_list = [1, 2, 2.5, 3.7,  4, 4.6, 5, 6, 6.7, 7.2, 8.5, 9]
y_list = func(x_list)

interpolator = LagrangeInterp(x_list=x_list, y_list=y_list

f = interpolator.GetFunc()  # The interpolatin function


## Lagrange Interpolation points
x_pts = np.linspace(0, 10, 1000)
y_pts = f(x_pts)


# Newton Forward Interpolation
x = np.arange(-5, 6, 1)
y = np.sin(x)

x_pts_NF = np.linspace(-5, 5, 1000)
y_pts_NF = NewtonForward(x_list = x, y_list = y, x = x_pts)