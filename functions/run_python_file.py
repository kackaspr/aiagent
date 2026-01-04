import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: Cannot execute because "{file_path}" does not exist or is not a regular file'
        
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, cwd = working_dir_abs, capture_output = True, text = True, timeout = 30.0)

        output = ""
        if not result.returncode == 0:
            output += f'Process exited with code "{result.returncode}"\n'
        
        if not result.stdout and not result.stderr:
            output += 'No output produced'
        elif result.stdout:
            output += "STDOUT:\n" + result.stdout
        elif result.stderr:
            output += "STDERR:\n" + result.stderr
        
        return output

    except Exception as e:
        return f'Error executing file "{file_path}": {e}'


schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Run python file in a specified file path relative to the working directory, with specified arguments",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "File path to run python file, relative to the working directory",
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                description = "Array of arguments to run python file",
                items = types.Schema(
                    type = types.Type.STRING,
                    description = "Argument to run python file",
                ),
            ),
        },
    ),
)