import typer
from pathlib import Path
from rich.console import Console
from ..utils import get_token
from datetime import datetime
from ..config import INSTRUCTION_UPLOAD_URL
from alectiocli.src import console
import requests

rich_console = Console()


def upload_instruction_doc(project_id, doc_path: Path):
    if doc_path.is_file() and doc_path.suffix in [".pdf", ".txt", ".text"]:
        with rich_console.status(
            "[bold green]Uploading labeling instruction file..."
        ) as status:
            token = get_token()

            headers = {"Authorization": str(token)}
            files = {"instructions": open(doc_path, "rb")}
            payload = {
                "project_id": project_id,
                "date": datetime.now().strftime("%d/%m/%Y"),
            }
            post_req_result = requests.post(
                INSTRUCTION_UPLOAD_URL,
                headers=headers,
                files=files,
                data=payload,
            )
            if post_req_result.status_code == 200:
                console.success("Instruction uploaded successfully")
            else:
                console.error("Instruction upload failed")
                raise typer.Exit()
    else:
        console.error(
            "Wrong instruction file type: Please Enter a [dot]pdf/[dot]txt/[dot]text file"
        )
        raise typer.Exit()
