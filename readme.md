# 1.Introduction
SNBCHS represents a cutting-edge software toolbox dedicated to safety verification in continuous dynamical systems by synthesizing neural barrier certificates. Synthesizing process is an counterexample-guided inductive framework comprising of Learner, Verifier, and Cex Generator components. During counterexample generation, we employ a specific format to transform the process into a polynomial optimization problem, streamlining the acquisition of optimal counterexamples. In the verification phase, the identification of the genuine barrier certificate is addressed by solving Linear Matrix Inequalities (LMI) feasibility problems.

This approach is particularly effective and scalable, outperforming traditional sum-of-squares programming techniques for solving linear or bilinear matrix inequality constraints in barrier certificate generation. Additionally, it surpasses state-of-the-art neural barrier certificate learning methods. Notably, SNBCHS is the pioneering procedure for synthesizing neural barrier certificates tailored for hybrid systems with discrete transitions. The software toolbox provides a comprehensive solution, encompassing crucial elements such as hybrid systems and counterexample (Cex) generation, making it a versatile and powerful tool for safety verification.

The directory in which you install SNBCHS contains nine subdirectories:

* `/ComparativeExperiment`：the code of comparative experiments;
* `/Counterexample`:the counterexamples generator;
* `/benchmarks`: the examples we showed in paper;
* `/learn`: the code of learner;
* `/verify`: the code of verifier;
* `/plot`: the code of plots;
* `/utils`: the configuration of the program;
* `/model`:the neural network models we trained;
* `/result`:the neural barrier certificates we generate;
  

# 2.Configuration

## 2.1 System requirements

To install and run SNBCHS, you need:

* Windows Platform: `Python 3.9.12`;
* Linux Platform: `Python 3.9.12`;
* Mac OS X Platform: `Python 3.9.12`.

## 2.2 Installation instruction

You need install required software packages listed below and setting up a MOSEK license .

1. Download SNBCHS.zip, and unpack it;
2. Install the required software packages for using SynNBC:

    ```python
    pip install cvxopt==1.3.0
    pip install matplotlib==3.5.3
    pip install numpy==1.23.2
    pip install scipy==1.9.0
    pip install SumOfSquares==1.2.1
    pip install sympy==1.11
    pip install torch==1.12.1
    pip install Mosek==10.0.30
    pip install gurobipy==10.0.0
    pip install picos==2.4.11
    ```

3. Obtain a fully featured Trial License if you are from a private or public company, or Academic License if you are a student/professor at a university.

* Free licenses
  * To obtain a trial license go to <https://www.mosek.com/products/trial/>
  * To obtain a personal academic license go to <https://www.mosek.com/products/academic-licenses/>
  * To obtain an institutional academic license go to <https://www.mosek.com/products/academic-licenses/>
  * If you have a custom license go to <https://www.mosek.com/license/request/custom/> and enter the code you received.
* Commercial licenses
  * Assuming you purchased a product ( <https://www.mosek.com/sales/order/>) you will obtain a license file.

# 3.Automated Synthesis of Neural Barrier Certificates

Main steps to synthesize verified barrier certificates:

1. Create a new example and confirm its number;
2. Input dimension `n`, three domains: `local,init and unsafe` and differential equations `f`;
3. Define the example’s name, call function `get_example_by_name`, input parameters of opts and get verified barrier functions.

## 3.1 New examples

In SYNHBC, if we want to synthesize a barrier certificate, at first we need create a new example in the examples dictionary in `Exampler_A.py`. Then we should confirm its number. In an example, its number is the key and value is the new example constructed by Example function.

```python
>>  1 : Example ()
```

## 3.2 Inputs for new examples

At first, we should confirm the dimension `n` and three basic domains: `local,init and unsafe`. There will be more inputs when the example is a hybrid system.For each domain, the number of the ranges must match the dimension `n` input.Here we show a hybrid system example to illustrate.

**Example 1** &emsp; Suppose we wish to input the following domains:

$$
\begin{split}
    The\  local\ condition:&
\Psi \left(\ell_1\right)=\left\{\mathbf{x} \in \mathbb{R}^{2} \mid -5 \leq x_{1}\leq 0,-5 \leq x_{2} \leq 5\right\}.\\&
\Psi \left(\ell_2\right)=\left\{\mathbf{x} \in \mathbb{R}^{2} \mid 0 \leq x_{1}\leq 5,-5 \leq x_{2} \leq 5\right\}.
\end{split}

$$

$$
The\ initial\ set: \mathcal{X}_{0}=\left\{\mathbf{x} \in \mathbb{R}^{2} \mid (x_{1}+2)^2+(x_{2}-2)^2 \leq 0.25\right\}.
$$

$$
The\ unsafe\ set: \mathcal{X}_{u}=\left\{\mathbf{x} \in \mathbb{R}^{2} \mid (x_{1}-2)^2+(x_{2}-2)^2 \leq 0.25\right\}. 
$$
$$
\begin{split}
    The\ guard\ condition: &G_{\ell_1,\ell_2}=\left\{\mathbf{x} \in \mathbb{R}^{2} \mid x_{1}^2+x_{2}^2 \leq 0.5625\right\}.\\&G_{\ell_2,\ell_1}=\left\{\mathbf{x} \in \mathbb{R}^{2} \mid x_{1}^2+x_{2}^2 \leq 0.25\right\}.
\end{split}
$$
$$
\begin{split}
    The reset condition: &R_{\ell_1,\ell_2}=\left\{x_{1}'=-x_{1},x_{2}'=x_{2}\right\}.\\&
    R_{\ell_2,\ell_1}=\left\{x_{1}'=x_{1}-2,x_{2}'=x_{2}+1\right\}.
\end{split}
$$

This can be instantiated as follows:

```python
>>  n=2,
>>  local_1=Zone(shape='box', low=[-5, -5], up=[0, 5], verify_zone=[lambda x: -x[0]]),
>>  local_2=Zone(shape='box', low=[0, -5], up=[5, 5], verify_zone=[lambda x: x[0]]),
>>  init=Zone(shape='ball', center=[-2, 2], r=0.5 ** 2),
>>  unsafe=Zone(shape='ball', center=[2, 2], r=0.5 ** 2),
>>  guard_1=Zone(shape='ball', center=[0, 0], r=0.75 ** 2),
>>  guard_2=Zone(shape='ball', center=[0, 0], r=0.5 ** 2),
>>  reset_1=[lambda x: -x[0], lambda x: x[1]],
>>  reset_2=[lambda x: x[0] - 2, lambda x: x[1] + 1],
```

Then, the dynamical system should be confirmed in the Example function. The dynamical system is modelled as differential equations `f`. We define the differential equations through lambda expressions. The variables $x_1,x_2,x_3,\cdots,x_n$ should be typed as $x[0], x[1], x[2], \cdots, x[n-1]$ in code. All differential equations are input into the *f* list.

For Example 1, we consider the following differential equations:
$$
\begin{equation*}
\mathbf{f_{1}}=\left[\begin{array}{c}
-x_{1}+x_{1}x_{2}\\
-x_{2}\\
\end{array}\right],
\mathbf{f_{2}}=\left[\begin{array}{c}
-x_{1}+2x_{1}^2x_{2}\\
-x_{2}\\
\end{array}\right].
\end{equation*}
$$
Construct the differential equations by setting

```python
>>  f_1=[lambda x: -x[0] + x[0] * x[1],
             lambda x: -x[1]],
>>  f_2=[lambda x: -x[0] + 2 * x[0] ** 2 * x[1],
             lambda x: -x[1]],
```

## 3.3 Generating neural barrier certificates

After inputting the dimension, domains and `f`, we should define the example’s name. For instance, to create an example named `H_2`, you need type:

```python
>> name = 'H2'
```

The completed example is following:

```python
>> 2: Example(
        n=2,
        local_1=Zone(shape='box', low=[-5, -5], up=[0, 5], verify_zone=[lambda x: -x[0]]),
        local_2=Zone(shape='box', low=[0, -5], up=[5, 5], verify_zone=[lambda x: x[0]]),
        init=Zone(shape='ball', center=[-2, 2], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[2, 2], r=0.5 ** 2),
        guard_1=Zone(shape='ball', center=[0, 0], r=0.75 ** 2),
        guard_2=Zone(shape='ball', center=[0, 0], r=0.5 ** 2),
        reset_1=[lambda x: -x[0], lambda x: x[1]],
        reset_2=[lambda x: x[0] - 2, lambda x: x[1] + 1],
        f_1=[lambda x: -x[0] + x[0] * x[1],
             lambda x: -x[1]],
        f_2=[lambda x: -x[0] + 2 * x[0] ** 2 * x[1],
             lambda x: -x[1]],
        name='H2'  
    ),
```

Then we should update the code of `barrier_template.py` or create a new python file by imitating its code. For generating a barrier cerficate,we should input the parameter name to call function `get_example_by_name` and set the parameters of opts.

For Example 1, the code example is as follows:

```python
>>  b2_activations = ['SKIP']
>>  b2_hidden_neurons = [10] * len(b1_activations)

>>  example = get_example_by_name('H2')

>>  start = timeit.default_timer()
>>  opts = {
        'b1_act': b1_activations,
        'b1_hidden': b1_hidden_neurons,
        'b2_act': b2_activations,
        'b2_hidden': b2_hidden_neurons,
        "example": example,
        'bm1_hidden': [10],
        'bm2_hidden': [10],
        'bm1_act': ['SKIP'],
        'bm2_act': ['SKIP'],
        'rm1_hidden': [],
        'rm2_hidden': [],
        'rm1_act': [],
        'rm2_act': [],
        "batch_size": 1000,
        'lr': 0.1,
        'loss_weight': (1, 1, 1, 1, 1, 1, 1, 1),
        'R_b': 0.5,
        'margin': 1,
        "DEG": [2, 0, 2, 2, 2, 2, 2, 2],
        "learning_loops": 100,
        'max_iter': 10,
        'counterexample_nums': 10
    }
```

At last, run the current file and we can get verified barrier certificates. For Example 1, the result is as follows:

```python
B1=2.07235393581884*x1**2 - 5.56682068288062*x1*x2 - 1.40131613527626*x1 + 8.00384275188518*x2**2 - 5.24091994748168*x2 + 1.08556270178307
B2=-0.646692658317694*x1**2 + 3.10991221573759*x1*x2 - 10.6640742736045*x1 - 7.29779423752359*x2**2 - 4.14366009911728*x2 + 13.9155044691098
```

At the same time, if the dimension `n` is 2, then a three-dimensional image of the `Barrier Certificate` and a two-dimensional image of the `Barrier Border` will be generated.For example 1, the image is as follows:

![Barrier Certificate](https://github.com/blliu6/Hybrid_system/blob/main/benchmarks/picture/H2_3d.png)
![Barrier Border](https://github.com/blliu6/Hybrid_system/blob/main/benchmarks/picture/H2_2d.png)