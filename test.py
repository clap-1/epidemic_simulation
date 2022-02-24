import numpy as np
x_1 = []
x_2 = []
x_2_anti = []
for i in range(100):
    u = np.random.uniform(0, 1)
    x_1.append(u**2)
    x_2.append(4*(u - 0.5)**2)
    x_2_anti.append(4*((1 - u) - 0.5)**2)

x_1_mean = np.mean(x_1)
x_2_mean = np.mean(x_2)
x_2_anti_mean = np.mean(x_2_anti)
cov1 = np.mean((x_1 - x_1_mean)*(x_2 - x_2_mean))
cov2 = np.mean((x_1 - x_1_mean)*(x_2_anti - x_2_anti_mean))
print(cov1)
print(cov2)