# from __future__ import annotations
import ast
from typing import Type, Callable
from inspect import signature
from pydoc import locate

import astor


def _pred_check(predicate, lamb, desc=None):
    def check(*args, **kwargs):
        if predicate(*args, **kwargs):
            return lamb(*args, **kwargs)
        else:
            if desc:
                raise AssertionError("Test '{}' failed!".format(desc))
            raise AssertionError("Test failed!")
    return check


def setter(name, orig, predicate, annotation):
    if isinstance(orig, property):
        return _pred_check(predicate, lambda self, x: orig.fset(x, self=self), annotation)
    else:
        return _pred_check(predicate, lambda self, x: setattr(self, '___{}_backing'.format(name), x), annotation)


def getter(name, orig, predicate, annotation):
    if isinstance(orig, property):
        return _pred_check(predicate, lambda self: orig.fget(self=self), annotation)
    else:
        return _pred_check(predicate, lambda self: getattr(self, '___{}_backing'.format(name), None), annotation)


def inject_assertions(type: Type):
    for prop, annotation in type.__annotations__.items():
        predicate = _annotation_to_predicate(prop, annotation)
        orig = getattr(type, prop, None)
        setattr(type, '___{}_backing'.format(prop), orig)
        get = getter(prop, orig, predicate, annotation)
        set = setter(prop, orig, predicate, annotation)
        setattr(type, prop, property(get, set))


def _annotation_to_predicate(name, annotation) -> Callable[[object, object], bool]:
    if annotation is None:
        return lambda self, x: True

    if annotation is bool:
        return lambda self, x: annotation

    if isinstance(annotation, type):
        return lambda self, x: isinstance(x, annotation)

    elif isinstance(annotation, str):  # supports from __future__ import annotations as a result
        tree = ast.parse(annotation, mode='eval')
        root = tree.body
        if isinstance(root, ast.FunctionDef):
            arg_len = len(root.args.args)
            has_self = arg_len >= 1 and root.args.args[0].arg == 'self'
            if arg_len - (1 if has_self else 0) > 1:
                raise AssertionError("Can't handle a function with >1 args!")

            func = eval(compile(tree, filename="<tinkertest_ast>", mode='eval'))
            if has_self:
                if arg_len == 1:
                    return lambda self, x: func(self)

                else:
                    return lambda self, x: func(self, x)

            else:
                if arg_len == 0:
                    return lambda self, x: func()

                else:
                    return lambda self, x: func(x)

        if isinstance(root, ast.Lambda):
            lam = root
            arg_len = len(lam.args.args)
            has_self = arg_len >= 1 and lam.args.args[0].arg == 'self'
            if arg_len - (1 if has_self else 0) > 1:
                raise AssertionError("Can't handle a lambda with >1 args!")

            func = eval(compile(tree, filename="<tinkertest_ast>", mode='eval'))
            if has_self:
                if arg_len == 1:
                    return lambda self, x: func(self)

                else:
                    return lambda self, x: func(self, x)

            else:
                if arg_len == 0:
                    return lambda self, x: func()

                else:
                    return lambda self, x: func(x)

        elif isinstance(root, ast.Call):
            raise NotImplementedError("Calls are not implemented yet!")

        elif isinstance(root, ast.Name):
            prop_type = locate(root.id)
            return lambda self, x: isinstance(x, prop_type)

        elif isinstance(root, ast.Compare):
            compiled = compile(tree, filename="<tinkertest_ast>", mode='eval')

            def check(self, x):
                locs = locals()
                locs[name] = x
                return eval(compiled, globals(), locs)

            return check

        elif isinstance(root, ast.Expr):
            raise AssertionError("Report this to the dev!")

        elif isinstance(root, ast.Expression):
            raise AssertionError("This should never happen!")

        else:
            raise AssertionError("Cannot transform expression of node type {} to a predicate!".format(type(root)))

    # Eagerly loaded expressions now
    elif isinstance(annotation, function):
        sig = signature(annotation)
        param_len = len(sig.parameters)
        if param_len == 0:
            return lambda self, x: annotation()

        elif param_len == 1:
            return lambda self, x: annotation(x)

        else:
            raise AssertionError("Function annotations must accept a max of 1 argument!")

    else:
        raise AssertionError("Unable to handle an annotation of type " + str(type(annotation)))


def _handle_props(type):
    pass


def _handle_func(type, func):
    pass


def main():
    import argparse

    parser = argparse.ArgumentParser(description="TinkerTest is a lightweight testing tool which makes writing tests "
                                                 "easy! It also provides a utility to apply this syntax to runtime "
                                                 "state validation.")

    args = parser.parse_args()


if __name__ == '__main__':
    main()
