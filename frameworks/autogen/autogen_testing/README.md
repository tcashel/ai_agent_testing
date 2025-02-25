# Autogen and Autogen Studio testing

## Get started

```bash
poetry install
```

## Autogen

## Autogen Studio

to run UI you need to be in the autogenstudio_ui directory
it uses a separate python environment, so you need to install dependencies there

### Autogen Studio notes

- its cool, but not all autogen code can be translated into the json format to load into the UI making it hard to actually use.

```bash
cd autogenstudio_ui
poetry install
```

then run the UI

```bash
poetry run autogenstudio ui --port 8081 --appdir /Users/tcashel/repositories/ai_agent_testing/autogen_testing/autogenstudio_ui
```

## To run the examples

from the root directory run

```bash
poetry install
```

then run the examples

```bash
python my_examples/OpenAIAssistantAPI.py
```
