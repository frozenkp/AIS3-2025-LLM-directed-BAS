from mcp.server.fastmcp import FastMCP
import subprocess
import os

mcp = FastMCP('mcp_tools')

@mcp.tool()
def execute_nircmd(args_string: str, nircmd_path: str = ".\\NirCmd.exe") -> str:
    """
    Executes nircmd.exe with a given string of arguments.

    Args:
        args_string: A string containing the arguments to pass to nircmd.exe,
                     separated by spaces.
        nircmd_path: The full path to nircmd.exe. Defaults to "nircmd.exe",
                     assuming it's in the system's PATH.

    Returns:
        A string containing the standard output and standard error from the
        command execution.
    """
    # The command needs to be a list of strings.
    command = ['powershell.exe', '-Command', f'{nircmd_path} {args_string}']
    print(f"Executing command: {' '.join(command)}")

    try:
        # Execute the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,  # Capture output as a string
            check=False, # Do not raise an exception for non-zero exit codes
            encoding='utf-8' # Specify encoding
        )

        # Combine stdout and stderr for a complete output log
        output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return output

    except FileNotFoundError:
        return (f"Error: '{nircmd_path}' not found. "
                "Please ensure nircmd.exe is in your system's PATH "
                "or provide the full path to the executable.")
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@mcp.tool()
def create_startup_shortcut(program_path: str, shortcut_name: str = "MyProgram", nircmd_path: str = ".\\NirCmd.exe") -> str:
    """
    Uses nircmd to create a shortcut in the current user's Startup folder.

    Args:
        program_path: The full path to the program for the shortcut.
        shortcut_name: The name for the shortcut file.
        nircmd_path: The full path to nircmd.exe. Defaults to "nircmd.exe".

    Returns:
        A string containing the standard output and standard error from the
        command execution.
    """
    # Get the user's startup folder path in a reliable way
    # APPDATA is the correct environment variable for the Roaming folder
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Ensure the program path and startup folder are quoted to handle spaces
    # The final argument (shortcut name) does not need quotes according to nircmd syntax
    args = f'shortcut "{program_path}" "{startup_folder}" "{shortcut_name}"'

    # Call the generic execution function
    return execute_nircmd(args, nircmd_path)

if __name__ == '__main__':
    mcp.run(transport='sse')
