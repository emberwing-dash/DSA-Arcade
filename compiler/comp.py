import subprocess
import os
import tempfile
import shutil

class Compiler:
    LANG_EXT = {
        "Python": ".py",
        "Java": ".java",
        "C++": ".cpp"
    }

    def __init__(self, language="Python"):
        self.language = language

    def run_code(self, code, user_input=""):
        lang = self.language
        ext = self.LANG_EXT.get(lang)
        if not ext:
            return f"Language {lang} not supported."

        try:
            if lang == "Java":
                # Create a temp directory
                tmpdir = tempfile.mkdtemp()
                file_path = os.path.join(tmpdir, "Main.java")
                with open(file_path, "w") as f:
                    f.write(code)

                # Compile Java
                compile_res = subprocess.run(["javac", file_path], capture_output=True, text=True)
                if compile_res.stderr:
                    return f"Compile Error:\n{compile_res.stderr}"

                # Run Java
                cmd = ["java", "-cp", tmpdir, "Main"]
                result = subprocess.run(cmd, input=user_input, capture_output=True, text=True, timeout=5)

            else:
                # Other languages use tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmpfile:
                    tmpfile.write(code.encode())
                    tmpfile_path = tmpfile.name

                if lang == "Python":
                    cmd = ["python", tmpfile_path]
                elif lang == "C++":
                    exe_file = tmpfile_path + "_exe"
                    compile_res = subprocess.run(["g++", tmpfile_path, "-o", exe_file], capture_output=True, text=True)
                    if compile_res.stderr:
                        return f"Compile Error:\n{compile_res.stderr}"
                    cmd = [exe_file]

                result = subprocess.run(cmd, input=user_input, capture_output=True, text=True, timeout=5)

        except subprocess.TimeoutExpired:
            return "Execution timed out."
        except Exception as e:
            return f"Error: {e}"
        finally:
            # Clean up temp files
            if lang == "Java":
                shutil.rmtree(tmpdir)
            else:
                os.remove(tmpfile_path)
                if lang == "C++" and os.path.exists(exe_file):
                    os.remove(exe_file)

        return f"{result.stdout}{result.stderr}".strip() or "No output."
