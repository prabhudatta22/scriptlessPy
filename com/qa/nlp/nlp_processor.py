import os
import subprocess

class NLPProcessor:

    def run_python(self):
        print("Test Case Mapping started")
        path = os.path.join(os.getcwd(), "src", "main", "java", "com", "tadigital", "qa", "nlp")

        process = subprocess.Popen(
            ["python", "-m", "predict"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # ensures output is string, not bytes
        )

        stdout, stderr = process.communicate()

        if stdout:
            print(stdout)
        if stderr:
            print(stderr)

        print("Test Case Mapping completed successfully")

    def train_model(self):
        print("Model Training started")
        path = os.path.join(os.getcwd(), "src", "main", "java", "com", "tadigital", "qa", "nlp")

        process = subprocess.Popen(
            ["python", "-m", "train"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        if stdout:
            print(stdout)
        if stderr:
            print(stderr)

        print("Model Training completed successfully")


if __name__ == "__main__":
    processor = NLPProcessor()
    processor.train_model()
    processor.run_python()
