import cirq

def deutsch_jozsa_algorithm(oracle, n_qubits=2):
    """
    Реализация алгоритма Дойча-Йожи для проверки, является ли функция постоянной или сбалансированной.

    :param oracle: Квантовая операция, представляющая оракул.
    :param n_qubits: Количество кубитов, используемых в схеме.
    :return: Результат выполнения алгоритма ('constant' или 'balanced')
    """
    # Создание кубитов
    qubits = [cirq.LineQubit(i) for i in range(n_qubits)]

    # Создание схемы
    circuit = cirq.Circuit()

    # Начальная подготовка состояния |+>
    for qubit in qubits[:-1]:
        circuit.append(cirq.H(qubit))

    # Подготовка дополнительного кубита в состоянии |->
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H(qubits[-1]))

    # Применение оракула
    circuit.append(oracle(*qubits))

    # Обратная подготовка состояний
    for qubit in qubits[:-1]:
        circuit.append(cirq.H(qubit))

    # Измерения
    circuit.append(cirq.measure(*qubits[:-1], key='result'))

    # Выполнение схемы
    simulator = cirq.Simulator()
    result = simulator.run(circuit)

    # Анализ результатов измерений
    if all(result.measurements['result'][i] == 0 for i in range(n_qubits - 1)):
        return 'constant'
    else:
        return 'balanced'

# Пример использования

def constant_oracle(qubits):
    """Оракул для постоянной функции."""
    pass  # Постоянный оракул ничего не делает с состоянием кубитов

def balanced_oracle(qubits):
    """Оракул для сбалансированной функции."""
    circuit = cirq.Circuit()
    circuit.append(cirq.CX(qubits[0], qubits[1]))  # Пример сбалансированного оракула
    return circuit

if __name__ == "__main__":
    print(deutsch_jozsa_algorithm(constant_oracle))  # Должен вернуть 'constant'
    print(deutsch_jozsa_algorithm(balanced_oracle))  # Должен вернуть 'balanced'
    