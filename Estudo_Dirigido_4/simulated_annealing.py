# Problema das N-rainhas: Simulated Annealing

import numpy as np
import math
import copy
import matplotlib.pyplot as plt

def different_column_violations(sol):
    """
    Retorna o número de violações em que duas rainhas estão na mesma coluna.

    Parâmetros:
    * sol: uma solução para o problema das n-rainhas.
    """

    conflicts = 0
    for i in range(len(sol)):
        for j in range(len(sol)):
            if i != j and sol[i] == sol[j]:
                conflicts += 1

    return conflicts

def different_diagonal_violations(sol):
    """
    Retorna o número de violações em que duas rainhas estão na mesma diagonal.

    Parâmetros:
    * sol: uma solução para o problema das n-rainhas.
    """

    conflicts = 0
    for i in range(len(sol)):
        for j in range(len(sol)):
            deltay = abs(sol[i] - sol[j])
            deltax = abs(i - j)
            if i != j and deltay == deltax:
                conflicts += 1

    return conflicts

def obj(sol):
    """
    Retorna o valor da função objetivo para uma solução.

    Parâmetros:
    * sol: uma solução para o problema das n-rainhas.
    """

    return different_diagonal_violations(sol) + different_column_violations(sol)

def random_change(sol):
    """
    Retorna um vizinho para uma solução, onde uma posição aleatória presente nesta solução recebe um outro valor
    aleatório.

    Parâmetros:
    * sol: uma solução para o problema das n-rainhas.
    """

    neighbor = copy.copy(sol)

    idx = np.random.randint(0, len(sol))
    old_value = neighbor[idx]
    value = old_value

    while old_value == value:
        value = np.random.randint(0, len(sol))

    neighbor[idx] = value

    return neighbor

def swap(sol):
    """
    Retorna um vizinho para uma solução, onde duas posições aleatórias presentes nesta solução "trocam de lugar".

    Parâmetros:
    * sol: uma solução para o problema das n-rainhas.
    """

    neighbor = copy.copy(sol)

    idx1 = np.random.randint(0, len(sol))
    idx2 = idx1

    while idx1 == idx2:
        idx2 = np.random.randint(0, len(sol))

    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1] 

    return neighbor

def simmulated_annealing(sol, objective, get_neighbor, maxit = 100, init_T = 10, cooldown_rate = 0.99):
    """
    Simula o algoritmo de Simmulated Annealing (Têmpera Simulada), retornando [best_sol, best_val, vals].

    Parâmetros:
    * sol: uma solução para o problema das n-rainhas;
    * objective: uma função que retorna o valor da função objetivo, e que possui a assinatura: function(sol);
    * get_neighbor: uma função que retorna um vizinho para uma solução, e que possui a assinatura: function(sol);
    * maxit: número máximo de iterações do algoritmo. Valor default definido como 100.
    * init_T: valor inicial da temperatura. Valor default definido como 10.
    * cooldown_rate: valor da taxa de resfriamento, entre 0 e 1, aplicada na temperatura a cada iteração. Valor
    default definido como 0.99.

    Saída:
    * best_sol: melhor solução encontrada pelo algoritmo;
    * best_val: valor da função objetivo referente à best_sol;
    * vals: valores correntes do algoritmo a cada iteração.
    """

    vals = []  # Armazena os valores correntes a cada iteração
    T = init_T # Temperatura inicial

    best_sol = copy.copy(sol)
    best_val = objective(sol)
    curr_val = objective(sol)
    it = 0

    while it <= maxit:
        n = get_neighbor(sol)
        n_val = objective(n)

        if n_val <= best_val:
            best_val = n_val
            best_sol = copy.copy(n)

        if n_val <= curr_val or np.random.rand() < math.exp(-(n_val - curr_val) / T):
            sol = copy.copy(n)
            curr_val = n_val
        
        vals.append(curr_val)
        
        print(f'Iteracao #{it}: {best_val}')

        it += 1
        T *= cooldown_rate # Resfriamento

    return best_sol, best_val, vals

if __name__ == '__main__':
    n = int(input('Digite o valor de n para o problema das n-rainhas: '))
    init_sol = list(range(n))

    best_sol, best_val, vals = simmulated_annealing(init_sol, obj, swap, maxit = 10000)

    print(f'\n=== Simmulated Annealing: Resultados ===')
    print(f'Melhor solucao encontrada: {best_sol}')
    print(f'Seu valor da funcao objetivo: {best_val}')
    
    plt.title('Valores correntes a cada iteração')
    plt.plot(vals)
    plt.show()
