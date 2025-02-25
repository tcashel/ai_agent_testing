# LangChain testing and tutorials

## sql_tutorial.py

- this agent seems to query the API way too much and passes everything to the API making the API fees higher than they should be
  - I think this has to do with the message state, and each call is sending the whole message to the next call instead of just the output of the previous call resultin in increasingly large messages to the openaiapi.
- I used OpenLit to find this out and it was useful
  - observability is importatnt.