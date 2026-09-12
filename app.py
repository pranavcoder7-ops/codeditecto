from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# -----------------------------
# LANGUAGE DETECTION
# -----------------------------
def detect_language(code):

    # C++
    if (
        "#include <iostream>" in code
        or "using namespace std" in code
        or "cout <<" in code
        or "cin >>" in code
        or "std::" in code
    ):
        return "C++"

    # C
    if (
        "#include <stdio.h>" in code
        or "printf(" in code
        or "scanf(" in code
    ):
        return "C"

    # Python
    if (
        "def " in code
        or "import " in code
        or "print(" in code
        or "elif " in code
        or "range(" in code
    ):
        return "Python"

    return "Unknown"


# -----------------------------
# CONCEPT DETECTION
# -----------------------------
def detect_concepts(code, language):

    concepts = []

    if "for" in code:
        concepts.append("For Loop")

    if "while" in code:
        concepts.append("While Loop")

    if "if" in code:
        concepts.append("Conditional Statement")

    if language == "Python" and "def " in code:
        concepts.append("Function")

    if language in ["C", "C++"] and "(" in code:
        concepts.append("Function")

    if "class " in code:
        concepts.append("Class")

    if "=" in code:
        concepts.append("Variables")

    if language in ["C", "C++"] and "#include" in code:
        concepts.append("Header File")

    if "[]" in code or "[" in code:
        concepts.append("Array / List")

    if "return" in code:
        concepts.append("Return Statement")

    if not concepts:
        concepts.append("Basic Programming")

    return list(dict.fromkeys(concepts))


# -----------------------------
# SMART EXPLANATION
# -----------------------------
def generate_explanation(code, language, concepts):

    explanation = []

    if language == "Python":

        explanation.append(
            "This is a Python program. Python is a high-level "
            "programming language known for simple and readable syntax."
        )

    elif language == "C":

        explanation.append(
            "This is a C program. C is a procedural programming "
            "language commonly used for system and application programming."
        )

    elif language == "C++":

        explanation.append(
            "This is a C++ program. C++ supports procedural, "
            "object-oriented and generic programming."
        )

    else:

        explanation.append(
            "The programming language could not be detected. "
            "Please enter C, C++ or Python code."
        )
        return explanation

    # Loop
    if "For Loop" in concepts:

        explanation.append(
            "A for loop is used to repeat a block of code "
            "multiple times or process items from a sequence."
        )

    # While
    if "While Loop" in concepts:

        explanation.append(
            "A while loop repeatedly executes code while "
            "a specified condition remains true."
        )

    # Condition
    if "Conditional Statement" in concepts:

        explanation.append(
            "The program uses a condition to make a decision. "
            "Different code can execute depending on whether "
            "the condition is true or false."
        )

    # Function
    if "Function" in concepts:

        explanation.append(
            "The program contains a function. Functions help "
            "organize code into reusable blocks."
        )

    # Variables
    if "Variables" in concepts:

        explanation.append(
            "Variables are used to store and work with data "
            "during program execution."
        )

    # Array/List
    if "Array / List" in concepts:

        explanation.append(
            "The program appears to use a collection such as "
            "an array or list to store multiple values."
        )

    # Class
    if "Class" in concepts:

        explanation.append(
            "A class is used to create objects and organize "
            "data and behaviour using object-oriented programming."
        )

    return explanation


# -----------------------------
# OUTPUT ESTIMATION
# -----------------------------
def estimate_output(code, language):

    if "print(" in code:
        return "The program contains a print statement. Its output depends on the values used."

    if "printf(" in code:
        return "The program contains printf(), which displays formatted output."

    if "cout <<" in code:
        return "The program contains cout, which displays output on the console."

    return "Output depends on the input and execution of the program."


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# ANALYZE API
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    code = data.get("code", "")

    if not code.strip():

        return jsonify({
            "error": "Please enter some code first."
        }), 400

    language = detect_language(code)

    concepts = detect_concepts(code, language)

    explanation = generate_explanation(
        code,
        language,
        concepts
    )

    output = estimate_output(
        code,
        language
    )

    return jsonify({

        "language": language,

        "lines": len(code.splitlines()),

        "characters": len(code),

        "concepts": concepts,

        "explanation": explanation,

        "output": output

    })


# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )