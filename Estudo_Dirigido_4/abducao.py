# Algoritmo de Abdução
# obs.: A função abduction_inner() foi feita para que a lista "original" de observações não seja alterada.

import copy

def abduction(kb, observations):
    """
    Realiza o processo de abdução.

    Parâmetros:
    * kb: uma base de conhecimento que contenha o campo 'assumables';
    * observations: uma lista de átomos referentes às observações.
    """
    
    observations_2 = copy.deepcopy(observations)
    return abduction_inner(kb, observations_2)

def abduction_inner(kb, observations, e = set()):
    """
    Função auxiliar da função abduction(), não deve ser chamada explicitamente.
    """

    if observations:
        o = observations[0]

        if o in kb['assumables']:
            if len(observations) > 1:
                return abduction_inner(kb, observations[1:], e | {o})
            else:
                return abduction_inner(kb, [], e | {o})

        else:
            bodies = kb['rules'][o]
            es = []
            for body in bodies:
                if len(observations) > 1:
                    es += abduction_inner(kb, body + observations[1:], e)
                else:
                    es += abduction_inner(kb, body, e)
                
            return es

    else:
        return [e]

def minimal_explanations(explanations):
    """
    Retorna uma lista de explicações mínimas.

    Parâmetros:
    * explanations: lista de explicações;
    """

    m_es = []

    for i in range(len(explanations)):
        isMinimal = True

        for j in range(len(explanations)):

            if i != j and explanations[j].issubset(explanations[i]):
                isMinimal = False
                break

        if isMinimal:
            m_es.append(explanations[i])

    return m_es

if __name__ == '__main__':
    kb = {'rules':{
            'bronchitis':[['influenza'], ['smokes']],
            'coughing':[['bronchitis']],
            'wheezing':[['bronchitis']],
            'fever':[['influenza'], ['infection']],
            'sore_throat':[['influenza']],
            'false':[['smokes', 'nonsmoker']]
            },

        'assumables': ['smokes', 'influenza', 'infection'] }
    
    observations = ['wheezing', 'fever']
    result = abduction(kb, observations)
    minimal = minimal_explanations(result)

    print(f'Processo de abducao para as observacoes {observations}: {result}')
    print(f'Explicacoes minimas: {minimal}')
