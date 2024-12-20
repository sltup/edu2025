import cirq
from sympy import symbols


def create_3_cnf_circuit(clauses):
    # Определяем количество переменных
    num_vars = max([max(term) for term in clauses])

    # Создаём qubits
    qubits = [cirq.GridQubit(i, 0) for i in range(num_vars)]

    # Создаем символические переменные для каждого qubit'а
    symbols_map = {q: symbols(f'x{q.x}') for q in qubits}

    # Создаём схему
    circuit = cirq.Circuit()

    # Добавляем CNOT между всеми парами переменных в каждом терме
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                circuit.append(cirq.CNOT(qubits[clause[i] - 1], qubits[clause[j] - 1]))

    return circuit, symbols_map


# Пример входных данных
clauses = [(1, 2, 3), (2, 3, 4)]

circuit, symbols_map = create_3_cnf_circuit(clauses)
print("Circuit:")
print(circuit)
