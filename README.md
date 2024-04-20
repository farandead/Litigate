<p align="center">
  <img src="https://github.com/farandead/Litigate/blob/main/Docs/Images_report/Artboard_1-removebg-preview.png" width="400">
</p>

# Litigate

## Introduction
Litigate leverages state-of-the-art large language models such as GPT-3.5, GPT-3.5 Turbo, GPT-4.0, and LLaMA 2 to provide expert legal advice on household and tenant law. This tool answers questions, offers advice, and references relevant case laws to help users navigate legal complexities effectively.

## Features
- Comprehensive answers and advice on household and tenant law.
- Integration with multiple advanced AI models for a broad perspective.
- Case law references to support legal advice.

## Getting Started

### Prerequisites
Before setting up Litigate, ensure you have:
- An OpenAI API key.
- Python 3.11 or newer installed.
- Conda as your environment manager.

### Installation

1. **Clone the Repository**
   Clone Litigate to your local machine using the following command:
   ```bash
   git clone https://github.com/farandead/Litigate.git
   cd Litigate
1. **Clone the Repository**
   Clone Litigate to your local machine using the following command:
   ```bash
   git clone https://github.com/farandead/Litigate.git
   cd Litigate
3. **Install Dependencies**
   Install the required Python packages with:
   ```bash
   pip install -r requirements.txt

## Configure Api Keys and Models
1. **GPT Models Configuration**
   Set your OpenAI API key in 'app/nlp/nlp_engine.py':
   ```bash
   import os
   os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
2. **LLaMA 2 Configuration**
   Download the LLaMA model from the provided link 'https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q4_0.bin' or if your working with a different model then change the name of the model in nlp_engine.py    
   accordingly and place it in the same directory as nlp_engine.py. Replace the existing Q/A chain setup:
   ```bash
   llm=CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':4096,
                          'temperature':0.8,
                          'context_length' : 2048})
   qa_chain = make_chain(llm,retriver,chain_type_kwargs)

## Set Up the Vector Database

To set up the vector database necessary for the project, follow these steps:

1. **Navigate to the Vector Database Setup Directory**
   Change to the directory where the setup script is located:
   ```bash
   cd app/nlp
   ```

2. **Run the Setup Script**
   Execute the setup script to configure the vector database:
   ```bash
   python setup_vector_database.py
   ```

## Adding Extra Context for the Model

- If you need to add extra context or additional data files for the model to use, place them in the `data` folder located within the `app/nlp` directory.

## Usage

To use Litigate, run the following command in your project directory:
```bash
flask run
```

## Contributing

We encourage community contributions. Please read our contributing guidelines for more information on how to contribute.

## License

Litigate is available under the MIT License. See the LICENSE file for more details.

## Contact

Faran Zafar - faranzafarcs@gmail.com

## Acknowledgements

- OpenAI for the AI models.
- Contributors who have helped to improve this tool.




