import cirq

def qft(qubits):
    """Функция для квантового преобразования Фурье."""
    circuit = cirq.Circuit()
    for i in range(len(qubits)):
        circuit.append(cirq.H(qubits[i]))
        for j in range(i + 1, len(qubits)):
            angle = cirq.Symbol(f'theta_{i}_{j}')
            circuit.append(cirq.CZPowGate(exponent=-angle / np.pi)(qubits[i], qubits[j]))
            circuit.append(angle.assign(np.pi / 2**(j - i)))
    return circuit

def inverse_qft(qubits):
    """Функция для обратного квантового преобразования Фурье."""
    circuit = cirq.Circuit()
    for i in reversed(range(len(qubits))):
        for j in reversed(range(i + 1, len(qubits))):
            angle = cirq.Symbol(f'theta_{i}_{j}')
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubits[i], qubits[j]))
            circuit.append(angle.assign(-np.pi / 2**(j - i)))
        circuit.append(cirq.H(qubits[i]))
    return circuit

# Пример использования
num_qubits = 3
qubits = [cirq.GridQubit(i, 0) for i in range(num_qubits)]

# Прямое КПФ
qft_circuit = qft(qubits)
print("Прямое КПФ:")
print(qft_circuit)

# Обратное КПФ
iqft_circuit = inverse_qft(qubits)
print("\nОбратное КПФ:")
print(iqft_circuit)
