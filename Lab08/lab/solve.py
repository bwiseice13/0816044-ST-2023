import angr
import sys
import os
import struct

def solve():
    proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
    class my_scanf(angr.SimProcedure):
        def run(self, format_string, scanf0_address):
            simfd = self.state.posix.get_fd(sys.stdin.fileno())
            data, _ = simfd.read_data(4)
            self.state.memory.store(scanf0_address, data)
            return 1
        
    scanf_symbol = '__isoc99_scanf'
    proj.hook_symbol(scanf_symbol, my_scanf(), replace=True)

    state  = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)

    def success(state):
        output = state.posix.dumps(sys.stdout.fileno())
        return b'AC!' in output

    def fail(state):
        output = state.posix.dumps(sys.stdout.fileno())
        return b'WA!' in output
    
    simgr.explore(find=success, avoid=fail)

    if simgr.found:
        input = simgr.found[0].posix.dumps(sys.stdin.fileno())

        file_path = "solve_output"
        if os.path.isfile(file_path):
            os.remove(file_path)

        with open("solve_output", "a") as file:
            for i in range(0, 15):
                integer_value = struct.unpack('<i', input[i*4:i*4+4])[0]
                file.write(str(integer_value) + str('\n'))
    else:
        print('Failed')

if __name__ == '__main__':
  solve()