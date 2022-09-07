import sys
import functools
import inspect
import re


class CommandLineInterface:

    def __init__(self):
        self.decorated_funcs = {}

    def command(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        print(f.__name__, inspect.getfullargspec(f)[0])
        self.decorated_funcs[f.__name__] = (wrapper,
                                            inspect.getfullargspec(f)[0])
        return wrapper

    def main(self):
        func_name = sys.argv[1] if len(sys.argv) != 1 else None
        func_arg_names = []
        func_arg_values = []
        for cmd_arg in sys.argv[2:]:
            if re.match(".+=.", cmd_arg) is None:
                print('USAGE: arguments must be passed \
                        as key word parameters')
                return 1
            func_arg_names.append(cmd_arg.partition('=')[0])
            func_arg_values.append(cmd_arg.partition('=')[2])
        if func_name in self.decorated_funcs:
            if func_arg_names == self.decorated_funcs[func_name][1]:
                self.decorated_funcs[func_name][0](*func_arg_values)
            else:
                print(f'USAGE: \'{func_name}\' should be called \
                        with the following key word parameters: \
                        {*self.decorated_funcs[func_name][1], }')
                return 1
        else:
            print(f'USAGE: available functions are \
                    {*self.decorated_funcs.keys(), }')
            return 1
        return 0


# cli = CommandLineInterface()

# @cli.command
# def inc(x):
#     print(int(x) + 1)

# @cli.command
# def div(x, y):
#     print(int(x) / int(y))

# if __name__ == "__main__":
#     cli.main()
