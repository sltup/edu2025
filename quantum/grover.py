import cirq


def nonogram_oracle(rows: list, cols: list):
    def _nonogram_oracle(qubits):
        solution = cirq.CircuitOperation(
            cirq.FrozenCircuit(
                cirq.Moment([
                    cirq.X(qubit) if bit else cirq.I(qubit)
                    for qubit, bit in zip(qubits, solution_bits)
                ])
            )
        )

        check_rows = cirq.CircuitOperation(
            cirq.FrozenCircuit(
                cirq.Moment([
                    cirq.X(qubits[row_index * 3 + col_index]) if not is_valid_row(row_index, col_index) else cirq.I(
                        qubits[row_index * 3 + col_index])
                    for row_index in range(3)
                    for col_index in range(3)
                ])
            )
        )

        check_cols = cirq.CircuitOperation(
            cirq.FrozenCircuit(
                cirq.Moment([
                    cirq.X(qubits[row_index * 3 + col_index]) if not is_valid_col(col_index, row_index) else cirq.I(
                        qubits[row_index * 3 + col_index])
                    for col_index in range(3)
                    for row_index in range(3)
                ])
            )
        )

        yield solution, check_rows, check_cols

    def is_valid_row(row_index, col_index):
        row = ''.join(str(int(bit)) for bit in solution_bits[row_index * 3:(row_index + 1) * 3])
        hints = rows[row_index]
        return matches_hints(row, hints)

    def is_valid_col(col_index, row_index):
        col = ''.join(str(int(solution_bits[col_index + row_index * 3])) for row_index in range(3))
        hints = cols[col_index]
        return matches_hints(col, hints)

    def matches_hints(sequence, hints):
        sequence = ''.join('1' if char == '1' else '0' for char in sequence)
        hint_sequence = ''.join(str(hint) + '0' for hint in hints) + '0'
        return sequence in hint_sequence

    return _nonogram_oracle


# Пример параметров для кроссворда
rows = [[1,1], [1], [1,1]]
cols = [[1,1], [1], [1,1]]

# Решение для данного кроссворда
solution_bits = [1, 0, 1,
                 0, 1, 0,
                 1, 0, 1]

# Определение кубитов
qubits = [cirq.GridQubit(i // 3, i % 3) for i in range(9)]

# Создание оракула
oracle = nonogram_oracle(rows, cols)(qubits)

# Проверка решения
circuit = cirq.Circuit(oracle)
simulator = cirq.Simulator()
result = simulator.simulate(circuit)

print(result)
