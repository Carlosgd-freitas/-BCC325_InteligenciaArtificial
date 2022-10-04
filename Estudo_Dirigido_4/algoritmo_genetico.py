# Problema das N-rainhas: Algoritmo Genético

import numpy as np
import copy
import math

### Funções retiradas do simulated_annealing.py
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
###

def pop_init(n, k):
    """
    Retorna uma população para o problema das n-rainhas (lista de soluções).

    Parâmetros:
    * n: valor de n para o problema das n-rainhas;
    * k: tamanho da população que será mantida a cada geração pelo algoritmo genetico;
    """

    return [np.random.permutation(n) for i in range(k)]

def mutation(sol):
    """
    Implementa a operação de mutação para o algoritmo genético: duas posições aleatórias presentes nesta solução
    "trocam de lugar".

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

def crossover(sol1, sol2):
    """
    Implementa a operação de crossover para o algoritmo genético: cada índice da nova solução gerada terá o mesmo
    valor presente neste mesmo índice na primeira solução ou na segunda, sendo esta decisão aleatória. Retorna
    [f1, f2].

    Parâmetros:
    * sol1: uma solução para o problema das n-rainhas;
    * sol2: uma solução para o problema das n-rainhas.

    Saída:
    * f1: uma solução para o problema das n-rainhas;
    * f2: uma solução para o problema das n-rainhas.
    """

    mask = np.random.randint(2, size=len(sol1))

    f1 = copy.copy(sol1)
    for i in range(len(sol1)):
        if mask[i] == 0:
            f1[i] = sol2[i]

    f2 = copy.copy(sol2)
    for i in range(len(sol2)):
        if mask[i] == 0:
            f2[i] = sol1[i]

    return f1, f2

def select_parents(pop):
    """
    Seleciona o índice de duas soluções presentes em pop, retornando [idx1, idx2].

    Parâmetros:
    * pop: uma população para o problema das n-rainhas (lista de soluções).

    Saída:
    * idx1: um índice de algum indivíduo de pop;
    * idx2: um índice de algum indivíduo de pop.
    """

    idx1 = np.random.randint(0, len(pop))
    idx2 = idx1

    while idx1 == idx2:
        idx2 = np.random.randint(0, len(pop))
    
    return idx1, idx2

def genetic_algorithm(n, pop_size, objective, gen_max = 1000):
    """
    Simula um algoritmo genético, retornando [pop, best_ind, best_val].

    Parâmetros:
    * n: valor de n para o problema das n-rainhas;
    * pop_size: tamanho da população que será mantida a cada geração;
    * objective: uma função que retorna o valor da função objetivo, e que possui a assinatura: function(sol);
    * gen_max: número máximo de gerações do algoritmo. Valor default definido como 1000.

    Saída:
    * pop: população da última geração do algoritmo;
    * best_ind: índice do melhor indivíduo da população;
    * best_val: valor da função objetivo referente à pop[best_ind];
    """

    # Generate population
    pop = pop_init(n, pop_size)
    gen = 0 # Contador de gerações
    best_ind = 0

    while gen < gen_max:

        for i in range(math.floor(len(pop) / 2)):
            # Seleção para reprodução
            idx_P1, idx_P2 = select_parents(pop)

            # Crossover
            f1, f2 = crossover(pop[idx_P1],pop[idx_P2])

            # Mutação + atualização da população
            pop[idx_P1] = mutation(f1)
            pop[idx_P2] = mutation(f2)

        gen += 1

        for (i, p) in enumerate(pop):
            if obj(p) <= objective(pop[best_ind]):
                best_ind = i

    best_val = obj(pop[best_ind])

    print(f'População final (Gen #{gen}):')
    for (i, p) in enumerate(pop):
        print(f'Indivíduo #{i}: {p}')

    # Encontrar o melhor indivíduo da população
    return pop, best_ind, best_val
    
if __name__ == '__main__':
    n = int(input('Digite o valor de n para o problema das n-rainhas: '))
    k = int(input('Digite o tamanho k da populacao que sera mantida pelo algoritmo genetico: '))

    pop = pop_init(n, k)

    print('População inicial (Gen #0):')
    for (i, p) in enumerate(pop):
        print(f'Indivíduo #{i}: {p}')

    print(f'\n=== Algoritmo Genetico: Operador de Mutação ===')
    print(f'Indivíduo #0: {pop[0]}')
    print(f'Possível mutação para o indivíduo #0: {mutation(pop[0])}')

    print(f'\n=== Algoritmo Genetico: Operador de Crossover ===')
    print(f'Indivíduo #0: {pop[0]}')
    print(f'Indivíduo #1: {pop[1]}')
    print(f'Possíveis crossing-overs para os indivíduos #0 e #1:')
    co = crossover(pop[0], pop[1])
    for sol in co:
        print(f'  > {sol}')
    print('')

    pop, best_ind, best_val = genetic_algorithm(n, k, obj, gen_max = 1000)

    print(f'\n=== Algoritmo Genetico: Resultados ===')
    print(f'Melhor solucao encontrada: {pop[best_ind]}')
    print(f'Seu valor da funcao objetivo: {best_val}')
