import typer


def error(msg: str):
    msg = "❌  " + msg + "\n"
    message = typer.style(msg, fg=typer.colors.RED)
    typer.echo(message)


def success(msg: str):
    msg = "✅  " + msg + "\n"
    message = typer.style(msg, fg=typer.colors.GREEN)
    typer.echo(message)


def info(msg: str):
    msg = "ℹ️  " + msg + "\n"
    message = typer.style(msg, fg=typer.colors.BLUE)
    typer.echo(message)


def warning(msg: str):
    msg = "⚠️  " + msg + "\n"
    message = typer.style(msg, fg=typer.colors.YELLOW)
    typer.echo(message)


def message(msg: str):
    message = typer.style(msg, fg=typer.colors.CYAN)
    typer.echo(message)
