import cirq
import numpy as np
from scipy.optimize import minimize


# Коэффициенты гамильтониана
a = 0.5
b = 0.7

# Гамильтонова матрица
hamiltonian_matrix = (
    a * np.kron(cirq.X, cirq.X) +
    b * np.kron(cirq.Z, cirq.Z)
)

def generate_ansatz(parameters, qubits):
    circuit = cirq.Circuit()
    for layer in range(4):
        for qubit in qubits:
            circuit.append(cirq.ry(parameters[layer * 2]).on(qubit))
            circuit.append(cirq.rz(parameters[layer * 2 + 1]).on(qubit))
        circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    return circuit


def energy_expectation(parameters, hamiltonian_matrix, qubits):
    circuit = generate_ansatz(parameters, qubits)
    simulator = cirq.Simulator()
    final_state_vector = simulator.simulate(circuit).final_state_vector
    expectation_value = np.real(np.vdot(final_state_vector, np.dot(hamiltonian_matrix, final_state_vector)))
    return expectation_value


def optimize_energy(hamiltonian_matrix, initial_parameters, qubits):
    def objective_function(parameters):
        return energy_expectation(parameters, hamiltonian_matrix, qubits)

    result = minimize(objective_function, initial_parameters, method='COBYLA', options={'maxiter': 10000})
    return result


# Число кубитов
num_qubits = 2
qubits = [cirq.GridQubit(i, 0) for i in range(num_qubits)]

# Начальные параметры
initial_parameters = np.random.rand(8)

# Оптимизация
opt_result = optimize_energy(hamiltonian_matrix, initial_parameters, qubits)

# Минимизированное значение энергии
optimal_energy = opt_result.fun
optimal_parameters = opt_result.x

print(f"Оптимальная энергия: {optimal_energy}")
print(f"Оптимальные параметры: {optimal_parameters}")
