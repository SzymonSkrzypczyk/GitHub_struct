from typing import List
from pathlib import Path
import typer
from github_struct.dir_processing import save_repo
from github_struct import __name__

app = typer.Typer(name=__name__)


@app.command('download')
def download_repo(url: str, main_dir: str, saving_path: str = '.', excluded: List[str] = typer.Option([])):
    path = Path(saving_path)
    if not path.exists():
        raise typer.Exit(1)
    save_repo(url, main_dir, excluded)
    typer.secho('Done!', fg='green', bold=True)


if __name__ == '__main__':
    app()
