from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.response_selection import get_random_response


chatbot = ChatBot(
    'Broski',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.85,
            'response_selection_method': get_random_response
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
            'response_selection_method': get_random_response,
            'threshold': 0.65,
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation',
            'response_selection_method': 'chatterbot.response_selection.get_random_response'
        },
        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter',
            'response_selection_method': 'chatterbot.response_selection.get_random_response'
        },
    ],
    database_uri='sqlite:///database.sqlite3'
)

training_data = [
    "Hi there!",
    "Hello!",
    "How are you?",
    "I'm doing well, thank you.",
    "What's your name?",
    "My name is Broski.",
    "Tell me a joke.",
    "Why couldn't the bicycle stand up by itself? Because it was two-tired!",
    "What's the weather like today?",
    "It's currently sunny with a high of 75°F.",
    "What time is it?",
    "It's currently 3:00 PM.",
    "Do you like pizza?",
    "Yes, I love pizza!",
    "Can you help me with something?",
    "Of course! What do you need help with?",
    "Goodbye",
    "Goodbye! Have a great day!"
]


def train_bot():
    trainer = ListTrainer(chatbot)
    trainer.train(training_data)

    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    corpus_trainer.train('chatterbot.corpus.english')


def run_chatbot():
    print("Welcome to Broski ChatBot. Type 'exit' to end the conversation.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Broski: Goodbye!")
                break
            else:
                bot_response = chatbot.get_response(user_input)
                print("Broski:", bot_response)
        except (KeyboardInterrupt, EOFError):
            print("\nBroski: Goodbye!")
            break
        except Exception as e:
            print("Broski: An error occurred:", str(e))


if __name__ == "__main__":
    train_bot()
    run_chatbot()
