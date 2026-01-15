"""Script contains launch-file-related utility python functions."""

from launch import LaunchContext
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration, PythonExpression


def create_arg_get_value(
    arg_name: str,
    description: str,
    default_value: str | None = None,
    choices: list[str] | None = None,
    add_to_arguments: list[tuple[str, LaunchConfiguration]] | None = None,
):
    """
    Add an argument to the launch file and returns (DeclareLaunchArgument, LaunchConfiguration).

    :param arg_name:
    :param description:
    :param default_value:
    :param choices:
    :param add_to_arguments: optional list to append (name, LaunchConfiguration) tuples to
    :return: (DeclareLaunchArgument, LaunchConfiguration)
    """
    if default_value is not None:
        if choices is not None:
            launch_arg = DeclareLaunchArgument(
                arg_name,
                default_value=default_value,
                description=description,
                choices=choices,
            )
        else:
            launch_arg = DeclareLaunchArgument(
                arg_name, default_value=default_value, description=description
            )
    elif choices is not None:
        launch_arg = DeclareLaunchArgument(arg_name, description=description, choices=choices)
    else:
        launch_arg = DeclareLaunchArgument(arg_name, description=description)

    launch_arg_val = LaunchConfiguration(arg_name)
    if add_to_arguments is not None and isinstance(add_to_arguments, list):
        add_to_arguments.append((arg_name, launch_arg_val, launch_arg))
    return launch_arg, launch_arg_val


def conditional_delayed_execution(data, condition, delay) -> TimerAction:
    """
    Create a launch action that conditionally delays the execution of 'data' by 'delay' seconds.

    Returns a TimerAction that:
      - starts `data` delayed by `delay` if `condition` is true,
      - starts `data` immediately (period 0.0) if `condition` is false.

    `condition` may be:
      - a bool
      - a string (e.g. "true" / "false")
      - a Substitution (e.g. LaunchConfiguration)

    `delay` may be:
      - a float/int
      - a string
      - a Substitution

    `data` may be a single Action or a list of Actions.
    """
    if not isinstance(data, list):
        data = [data]

    # Build expression parts (PythonExpression accepts a list of strings/substitutions)
    expr_parts = []

    # delay part
    if isinstance(delay, int | float):
        expr_parts.append(str(float(delay)))
    else:
        # assume it's a string or a Substitution (e.g. LaunchConfiguration)
        expr_parts.append(delay)

    # conditional: we build: <delay_expr> if "<cond_val>" == "true" else 0.0
    expr_parts.append(' if "')
    if isinstance(condition, bool):
        expr_parts.append(str(condition).lower())
    else:
        expr_parts.append(condition)
    expr_parts.append('" == "true" else 0.0')

    return TimerAction(period=PythonExpression(expr_parts), actions=data)


def print_arg(context: LaunchContext, *args) -> list:
    """
    Output the value of LaunchConfiguration arguments.

    Each arg in args should be a tuple (name, LaunchConfiguration).
    This function is suitable for use via OpaqueFunction(function=print_arg, args=[...]).
    """
    for arg in args:
        name, subst = arg[:2]
        try:
            val = subst.perform(context)
        except Exception:
            val = "<unable to evaluate>"
        print(f"[LAUNCH] {name} = {val}")
    return []


def launch_value_if(condition, if_true, if_false, cast_to_string: bool = True):
    """Compute an inline-if condition depending on a launch-runtime argument."""
    condition_expr = []
    if cast_to_string:
        condition_expr += ['"']
    condition_expr += [if_true, ('"' if cast_to_string else "") + " if "]
    if isinstance(condition, bool):
        condition_expr += ["true" if condition else "false"]
    else:
        condition_expr += ['"', condition, '".lower()']
    condition_expr += [' == "true" else ' + ('"' if cast_to_string else ""), if_false]
    if cast_to_string:
        condition_expr.append('"')
    return PythonExpression(condition_expr)
