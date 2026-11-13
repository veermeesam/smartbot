from datetime import datetime
import ast
import operator
import random


# Safe arithmetic: eval() ke bajay sirf allowed math operations chalte hain
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def safe_calculate(expression):
    """Evaluate a basic arithmetic expression safely."""
    try:
        tree = ast.parse(expression, mode="eval")
        return _evaluate_node(tree.body)
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None


def _evaluate_node(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)

        # Keep exponentiation within reasonable bounds
        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large")

        return OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_evaluate_node(node.operand))

    raise ValueError("Unsupported expression")


def get_response(message):
    text = message.lower().strip()

    if any(word in text for word in ("hello", "hi", "hey", "salam", "assalamualaikum")):
        return "Wa alaikum assalam! Welcome. How can I help you?"

    if "how are you" in text:
        return "I'm doing great, thank you! What would you like to know?"

    if "who are you" in text or "your name" in text:
        return "I'm SmartBot, a Python chatbot built with rule-based responses."

    if "motivate me" in text or "motivation" in text:
        return random.choice([
            "Keep going. Every bug you solve makes you a better developer!",
            "Small progress every day adds up to big results.",
            "You don't have to be perfect—just keep learning and building."
        ])

    if "happy" in text:
        return "That's great to hear! Keep that positive energy going."

    if "sad" in text or "upset" in text:
        return "I'm sorry you're feeling that way. Take one small step at a time."

    if "time" in text:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."

    if "date" in text or "today" in text:
        return f"Today's date is {datetime.now().strftime('%d %B %Y')}."

    if text.startswith("calculate "):
        expression = text.removeprefix("calculate ").strip()
        result = safe_calculate(expression)
        if result is not None:
            return f"The answer is {result}."
        return "I couldn't calculate that. Try something like: calculate 12 * (4 + 2)"

    return "I don't know that yet. Try /help to see what I can do."


def main():
    print("=" * 52)
    print("ASSALAMUALAIKUM! WELCOME TO SMARTBOT")
    print("Type /help for commands or 'bye' to exit.")
    print("=" * 52)

    chat_history = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        if not user_input:
            print("Bot: Please type a message.")
            continue

        command = user_input.lower()

        if command in ("bye", "exit", "quit"):
            print("Bot: Goodbye! Keep learning and building.")
            break

        if command == "/help":
            print(
                "Bot: You can ask about greetings, my name, how I am, "
                "motivation, time, date, or use 'calculate 5 * (2 + 3)'.\n"
                "     Commands: /help, /history, bye"
            )
            continue

        if command == "/history":
            if not chat_history:
                print("Bot: No conversation history yet.")
            else:
                print("\n--- Conversation History ---")
                for question, answer in chat_history:
                    print(f"You: {question}\nBot: {answer}")
            continue

        reply = get_response(user_input)
        chat_history.append((user_input, reply))
        print(f"Bot: {reply}")


if __name__ == "__main__":
    main()