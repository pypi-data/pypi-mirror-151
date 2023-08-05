from rich import box, print_json
from rich.table import Table

from servicefoundry.build.console import console
from servicefoundry.cli.config import CliConfig


def get_table(title):
    return Table(title=title, show_lines=False, safe_box=True, box=box.MINIMAL)


def stringify(x):
    if type(x) == str:
        return x
    else:
        return str(x)


def print_list(title, items, columns=None):
    if CliConfig.get("json"):
        print_json(data=items)
        return

    table = get_table(title)

    if items:
        if not columns:
            columns = items[0].keys()
        for column in columns:
            no_wrap = False
            overflow = "ellipsis"
            if column == "id":
                no_wrap = True
                overflow = "fold"
            table.add_column(column, justify="left", overflow=overflow, no_wrap=no_wrap)

    for item in items:
        row = []
        for c in columns:
            row.append(stringify(item[c]))
        table.add_row(*row)
    console.print(table)


def print_obj(title, item, columns=None):
    if CliConfig.get("json"):
        print_json(data=item)
        return

    table = get_table(title)

    if not columns:
        columns = item.keys()

    # transpose
    keys, columns = columns, ["key", "value"]

    for column in columns:
        table.add_column(column, justify="left", overflow="fold", no_wrap=False)
    for key in keys:
        table.add_row(f"[bold]{stringify(key)}[/]", stringify(item[key]))
    console.print(table)
