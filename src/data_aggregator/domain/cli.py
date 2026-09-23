from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from rich.console import Console
from rich.text import Text
from rich.tree import Tree

_console = Console()



def _style_scalar(value: Any) -> Text:
    """Render a leaf value with a minimal, type-aware colour palette."""
    if value is None:
        return Text("None", style="dim italic")
    if isinstance(value, bool):                 # check before int!
        return Text(str(value), style="bold cyan")
    if isinstance(value, (int, float)):
        return Text(str(value), style="yellow")
    if isinstance(value, str):
        return Text(f'"{value}"', style="green")
    return Text(str(value))


def _is_container(value: Any) -> bool:
    return isinstance(value, (BaseModel, dict, list, tuple, set))



def _render_field(tree: Tree, key: str, value: Any) -> None:
    label = Text(key, style="bold magenta")

    if isinstance(value, BaseModel):
        branch = tree.add(Text.assemble(label, Text(f"  {type(value).__name__}", style="dim")))
        _render(branch, value)
    elif isinstance(value, dict):
        branch = tree.add(Text.assemble(label, Text(f"  {{{len(value)}}}", style="dim")))
        _render(branch, value)
    elif isinstance(value, (list, tuple, set)):
        branch = tree.add(Text.assemble(label, Text(f"  [{len(value)}]", style="dim")))
        _render(branch, value)
    else:
        tree.add(Text.assemble(label, Text(": ", style="dim"), _style_scalar(value)))


def _render(tree: Tree, value: Any) -> None:
    """Recursively fill a rich Tree with any pydantic / python structure."""
    if isinstance(value, BaseModel):
        for name, field_value in value:
            _render_field(tree, name, field_value)

    elif isinstance(value, dict):
        for k, v in value.items():
            _render_field(tree, str(k), v)

    elif isinstance(value, (list, tuple, set)):
        for i, item in enumerate(value):
            if _is_container(item):
                branch = tree.add(Text(f"[{i}]", style="dim"))
                _render(branch, item)
            else:
                tree.add(Text.assemble(Text(f"[{i}] ", style="dim"), _style_scalar(item)))

    else: 
        tree.add(_style_scalar(value))



def display(model: BaseModel, *, title: str | None = None) -> None:
    """
    Pretty-print any pydantic BaseModel to the terminal as a modern tree.

    Handles arbitrarily nested BaseModels, dicts, lists/tuples/sets,
    and any scalar leaves (str / int / float / bool / None / Enum / datetime).
    """
    root = Tree(Text(title or type(model).__name__, style="bold blue"))
    _render(root, model)
    _console.print(root)