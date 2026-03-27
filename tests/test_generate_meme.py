import subprocess
import sys

def test_generate_meme_help():
    try:
        result = subprocess.run(
            [sys.executable, "generate_meme.py", "--help"],
            capture_output=True,
            text=True,
            check=False # Run even if return code is not 0 initially
        )
        # A help command should ideally exit with 0, but we'll be lenient
        # and primarily check that it didn't crash.
        # Depending on how generate_meme.py is structured,
        # it might print help to stdout or stderr, and exit code might vary.
        # For now, let's just ensure it runs.
        # A more robust check would be to assert result.returncode == 0
        print("stdout:", result.stdout, flush=True)
        print("stderr:", result.stderr, flush=True)
        assert result.returncode == 0, f"Script exited with {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"
    except FileNotFoundError:
        print("Error: generate_meme.py not found or python executable is not correct.", flush=True)
        assert False, "generate_meme.py not found or python executable is not correct."
    except Exception as e:
        print(f"An unexpected error occurred: {e}", flush=True)
        assert False, f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    test_generate_meme_help()
    print("Test script finished.", flush=True)
