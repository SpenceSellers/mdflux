from dataclasses import dataclass
import subprocess
import os

@dataclass
class ExecResult:
    stdout: str
    stderr: str

def exec(cmd: str, file_path: str) -> ExecResult:
    file_path = os.path.abspath(file_path)
    cwd = os.path.dirname(file_path)
    res = subprocess.run(cmd, shell=True, check=True, capture_output=True, cwd=cwd)
    return ExecResult(stdout=res.stdout.decode("utf-8"), stderr=res.stderr.decode('utf-8'))