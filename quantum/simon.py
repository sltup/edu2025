import cirq
import numpy as np

def simons_oracle(period, n_qubits):
    """Создает оракул для функции с периодом period"""
    def _oraculum(qubits):
        input_reg = qubits[:n_qubits]
        output_reg = qubits[n_qubits:]
        for i in range(n_qubits):
            cirq.CXOR(input_reg[i], input_reg[(i + period) % n_qubits], output_reg[i])
        yield
    return _oraculum

def simons_algorithm(n_qubits, oracle):
    """Реализация алгоритма Саймона"""
    qubits = [cirq.GridQubit(i, 0) for i in range(2 * n_qubits)]
    circuit = cirq.Circuit()

    # Инициализация первого регистра в суперпозиции всех возможных значений
    circuit.append(cirq.H.on_each(*qubits[:n_qubits]))

    # Применение оракула
    circuit.append(oracle(qubits))

    # Интерференционный шаг
    circuit.append(cirq.H.on_each(*qubits[:n_qubits]))

    # Измерение первого регистра
    circuit.append(cirq.measure(*qubits[:n_qubits], key='result'))

    return circuit

def find_period(measurements):
    """Использует метод дискретного преобразования Фурье для нахождения периода"""
    n = len(measurements[0])
    frequencies = []
    for measurement in measurements:
        frequency = 0
        for i in range(n):
            frequency += int(measurement[i]) * (2 ** (n - 1 - i))
        frequencies.append(frequency)
    return np.gcd.reduce(frequencies)

def main():
    # Параметры задачи
    n_qubits = 3
    period = 2

    # Создание оракула
    oracle = simons_oracle(period, n_qubits)

    # Запуск алгоритма Саймона
    circuit = simons_algorithm(n_qubits, oracle)
    print("Circuit:\n", circuit)

    # Симуляция
    simulator = cirq.Simulator()
    results = []
    repetitions = 10
    for _ in range(repetitions):
        result = simulator.run(circuit)
        results.append(result.measurements['result'][0])

    # Нахождение периода
    found_period = find_period(results)
    print("Found period:", found_period)

if __name__ == "__main__":
    main()
