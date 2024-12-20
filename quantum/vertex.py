import networkx as nx
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.aqua.components.optimizers import SPSA
from qiskit.aqua.components.variational_forms import RY
from qiskit.aqua.algorithms import QAOA

# Подключение к IBM Quantum Experience (опционально)
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend = provider.get_backend('ibmq_montreal') # Используем любой доступный провайдер

# Граф и начальная установка
graph = nx.cycle_graph(4)
num_qubits = graph.number_of_nodes()
initial_state = RY(num_qubits)
optimizer = SPSA(maxiter=50)

# Определение квантового гамильтониана
def hamiltonian(qubitOp, graph):
    edges = graph.edges()
    ham = qubitOp.zero()
    for edge in edges:
        i, j = edge
        op = qubitOp.pauli_op("IX"[i], "IX"[j])
        ham += (-1)*op
    return ham

# Настройка QAOA
quantum_instance = Aer.get_backend('qasm_simulator')
algorithm = QAOA(operator=hamiltonian, optimizer=optimizer, initial_state=initial_state, reps=1)
result = algorithm.run(quantum_instance)

# Получение результата
minimal_coverage = result['optimal_value']
print("Минимальное вершинное покрытие:", minimal_coverage)
