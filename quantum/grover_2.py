import math
import cirq

def grover_oracle(solution, qubits):
    """Оракул для алгоритма Гровера, который инвертирует фазу решения."""
    circuit = cirq.Circuit()
    for index, bit in enumerate(reversed(solution)):
        if bit == '1':
            circuit.append(cirq.X(qubits[index]))
    circuit.append(cirq.Z.on_each(*qubits))
    for index, bit in enumerate(reversed(solution)):
        if bit == '1':
            circuit.append(cirq.X(qubits[index]))
    return circuit

def diffusion_operator(qubits):
    """Диффузионный оператор для усиления амплитуд."""
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.X.on_each(*qubits))
    circuit.append(cirq.Z.controlled_by(*qubits[:-1]).on(qubits[-1]))
    circuit.append(cirq.X.on_each(*qubits))
    circuit.append(cirq.H.on_each(*qubits))
    return circuit

def grovers_algorithm(oracle, num_qubits, iterations=None):
    """Алгоритм Гровера для поиска решения с использованием оракула."""
    qubits = [cirq.GridQubit(i, 0) for i in range(num_qubits)]
    circuit = cirq.Circuit()

    # Начальное состояние
    circuit.append(cirq.H.on_each(*qubits))

    # Циклическое применение оракула и диффузии
    if iterations is None:
        iterations = int(math.pi / 4 * math.sqrt(2 ** num_qubits))
    for _ in range(iterations):
        circuit += oracle(qubits)
        circuit += diffusion_operator(qubits)

    # Измерение
    circuit.append(cirq.measure(*qubits, key='result'))

    return circuit

# Пример использования
def main():
    # Пример решения для оракула
    solution = '101'
    num_qubits = len(solution)

    # Создание оракула
    oracle = grover_oracle(solution, [cirq.GridQubit(i, 0) for i in range(num_qubits)])

    # Запуск алгоритма Гровера
    circuit = grovers_algorithm(oracle, num_qubits)
    print("Circuit:\n", circuit)

    # Симуляция
    simulator = cirq.Simulator()
    result = simulator.run(circuit)
    print("Result:", result)

if __name__ == "__main__":
    main()
