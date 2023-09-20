# Introduction 
The objective of this hackathon idea is to create an API that facilitates the creation and search of a knowledge base (KB) using ChatGPT as the interpreter. The primary focus of this hackathon is to build a comprehensive and useful knowledge base by leveraging ChatGPT's language understanding capabilities.

There are three applications:
- KB_Microservice.py - This is the API and does most of the work.
- test_kb_services.py - This is small app to execute and test the API endpoints.
- ChatBot - .NET Console App that is the chat bot app. It calls the API search endpoint.

# Getting Started
Make sure to add the appropriate config settings to user secrets. RMC on project -> Manage User Secrets.

```
{
  "endpoint": "https://azureopenai_name.openai.azure.com/",
  "openaikey": "key goes here",
  "deployment": "deployment_model_name"
}
```

You'll also need to create two files in the KB_Microservice folder (for the python scripts):
- endpoint_openai_azure.txt
- key_openai_azure.txt

Run the python script in two different command prompts via:
- `python kb_microservice.py`
- `python test_kb_services.py`

Run ChatBot from visual studios


## Acknowledgments

This project has benefited from a number of other open-source projects and resources:

- [KB_microservice](https://github.com/daveshap/KB_microservice) for the KB approach.
- [ChromaDB_Chatbot_Public](https://github.com/daveshap/ChromaDB_Chatbot_Public) for providing a solid foundation using ChromaDB.
- David Shapiro's [Private ChatGPT instance with ChromaDB backend, builds personal KB articles, updates User Profile!](https://youtu.be/n8X2h8Mg3WE) for ChromaDB, chatbot and ChatGPT.
- David Shapiro's [ChatGPT as an Interpreter: Introducing the KB Microservice for autonomous AI entities](https://www.example.com) for guiding the create and search of KB articles.
- [David Shapiro](https://github.com/daveshap) GitHub Profile

We're grateful for the contributions of these projects and the people behind them.
