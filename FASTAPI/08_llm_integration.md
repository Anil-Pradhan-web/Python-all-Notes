# 📘 Chapter 8: LLM Integration 🔥

> FastAPI + AI = Modern Backend. OpenAI, Groq, Gemini, LangChain, Streaming — sab seekho.

---

## 8.1 🤖 Calling LLM APIs — Direct

### OpenAI

```bash
pip install openai
```

```python
# app/services/llm.py

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content
```

```python
# app/routers/ai.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import chat_with_openai

router = APIRouter(prefix="/ai", tags=["AI"])

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"

class ChatResponse(BaseModel):
    response: str
    model: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = chat_with_openai(request.prompt, request.model)
    return ChatResponse(response=result, model=request.model)
```

### Groq (Ultra Fast)

```bash
pip install groq
```

```python
from groq import Groq
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_with_groq(prompt: str, model: str = "llama-3.1-70b-versatile") -> str:
    response = groq_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content
```

### Google Gemini

```bash
pip install google-genai
```

```python
from google import genai
import os

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def chat_with_gemini(prompt: str, model: str = "gemini-2.0-flash") -> str:
    response = gemini_client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text
```

### Multi-Provider LLM Service

```python
# app/services/llm_service.py

class LLMService:
    """Ek unified interface — koi bhi provider use karo"""

    def __init__(self):
        self.providers = {
            "openai": self._call_openai,
            "groq": self._call_groq,
            "gemini": self._call_gemini,
        }

    async def chat(self, prompt: str, provider: str = "openai", model: str = None) -> str:
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        return await self.providers[provider](prompt, model)

    async def _call_openai(self, prompt: str, model: str = None):
        model = model or "gpt-4o-mini"
        # ... OpenAI call
        return chat_with_openai(prompt, model)

    async def _call_groq(self, prompt: str, model: str = None):
        model = model or "llama-3.1-70b-versatile"
        return chat_with_groq(prompt, model)

    async def _call_gemini(self, prompt: str, model: str = None):
        model = model or "gemini-2.0-flash"
        return chat_with_gemini(prompt, model)

# Dependency
def get_llm_service():
    return LLMService()
```

---

## 8.2 🌊 Streaming Responses

LLM responses progressive dikhana — like ChatGPT.

### OpenAI Streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_openai(prompt: str):
    """Generator function — chunks yield karta hai"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True  # ← Yeh key hai!
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

@app.post("/ai/stream")
def stream_chat(prompt: str):
    return StreamingResponse(
        stream_openai(prompt),
        media_type="text/event-stream"
    )
```

### Server-Sent Events (SSE) — Better Streaming

```bash
pip install sse-starlette
```

```python
from sse_starlette.sse import EventSourceResponse
import json

async def event_generator(prompt: str):
    """SSE format mein events bhejo"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield {
                "event": "message",
                "data": json.dumps({"content": content})
            }

    # Stream complete signal
    yield {
        "event": "done",
        "data": json.dumps({"status": "complete"})
    }

@app.post("/ai/sse")
async def sse_chat(prompt: str):
    return EventSourceResponse(event_generator(prompt))
```

**Frontend (JavaScript):**
```javascript
const eventSource = new EventSource('/ai/sse?prompt=Hello');
eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    document.getElementById('output').textContent += data.content;
};
eventSource.addEventListener('done', () => {
    eventSource.close();
});
```

---

## 8.3 🦜 LangChain Integration

```bash
pip install langchain langchain-openai langchain-community
```

### Basic Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Chain banao
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {topic} teacher. Explain in Hinglish."),
    ("user", "{question}")
])

chain = prompt | llm | StrOutputParser()

# FastAPI endpoint
@app.post("/ai/explain")
async def explain(topic: str, question: str):
    result = await chain.ainvoke({"topic": topic, "question": question})
    return {"explanation": result}
```

### LangChain with Streaming

```python
from fastapi.responses import StreamingResponse

async def langchain_stream(topic: str, question: str):
    async for chunk in chain.astream({"topic": topic, "question": question}):
        yield chunk

@app.post("/ai/explain-stream")
async def explain_stream(topic: str, question: str):
    return StreamingResponse(
        langchain_stream(topic, question),
        media_type="text/event-stream"
    )
```

### RAG (Retrieval Augmented Generation)

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Document load & split karo
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Vector store banao
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_texts(texts, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# RAG chain
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """Answer based on the following context only:
    Context: {context}
    If you don't know, say 'I don't know'."""),
    ("user", "{question}")
])

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

@app.post("/ai/rag")
async def rag_query(question: str):
    result = await rag_chain.ainvoke(question)
    return {"answer": result}
```

---

## 8.4 🕸️ LangGraph Agent as API

```bash
pip install langgraph
```

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI

# State define karo
class AgentState(TypedDict):
    messages: list
    current_step: str

# Tools define karo
def search_tool(query: str) -> str:
    return f"Search results for: {query}"

def calculator_tool(expression: str) -> str:
    return str(eval(expression))

# Agent graph banao
llm = ChatOpenAI(model="gpt-4o-mini")

def agent_node(state: AgentState):
    """Agent decide karta hai next step"""
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def tool_node(state: AgentState):
    """Tools execute karo"""
    # Tool execution logic
    return state

# Graph build karo
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", "tools")
workflow.add_edge("tools", END)

agent_app = workflow.compile()

# FastAPI endpoint
@app.post("/ai/agent")
async def run_agent(query: str):
    result = await agent_app.ainvoke({
        "messages": [{"role": "user", "content": query}],
        "current_step": "start"
    })
    return {"result": result["messages"][-1]}
```

---

## 8.5 📝 Prompt Templating via Request Params

```python
from pydantic import BaseModel

class PromptRequest(BaseModel):
    template: str = "Explain {topic} in simple terms for a {audience}"
    variables: dict = {"topic": "FastAPI", "audience": "beginner"}
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 500

@app.post("/ai/template")
async def template_chat(request: PromptRequest):
    # Template fill karo
    prompt = request.template.format(**request.variables)

    response = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

    return {
        "prompt_used": prompt,
        "response": response.choices[0].message.content
    }
```

---

## 8.6 🪝 Webhooks for LLM Callbacks

```python
import httpx
from fastapi import BackgroundTasks

class WebhookRequest(BaseModel):
    prompt: str
    callback_url: str  # Results yahan bhejo

async def process_and_callback(prompt: str, callback_url: str):
    """Background mein LLM call karo, result webhook pe bhejo"""
    try:
        result = chat_with_openai(prompt)

        async with httpx.AsyncClient() as client:
            await client.post(callback_url, json={
                "status": "completed",
                "prompt": prompt,
                "response": result
            })
    except Exception as e:
        async with httpx.AsyncClient() as client:
            await client.post(callback_url, json={
                "status": "failed",
                "error": str(e)
            })

@app.post("/ai/async-chat")
async def async_chat(request: WebhookRequest, background_tasks: BackgroundTasks):
    """
    LLM call background mein karo — result webhook pe aayega.
    Long-running LLM tasks ke liye perfect.
    """
    background_tasks.add_task(
        process_and_callback,
        request.prompt,
        request.callback_url
    )
    return {"status": "processing", "message": "Result will be sent to callback URL"}

# Webhook receiver (for testing)
@app.post("/webhook/receive")
async def receive_webhook(data: dict):
    print(f"Webhook received: {data}")
    return {"received": True}
```

---

## ⚠️ Common Mistakes

| # | Mistake | Solution |
|---|---------|----------|
| 1 | API key code mein hardcode karna | `.env` file + `os.getenv()` use karo |
| 2 | Streaming response mein error handling nahi | try/except generator mein lagao |
| 3 | LLM response pe blindly trust karna | Output validate karo — Pydantic models use karo |
| 4 | Rate limits ignore karna (OpenAI) | Retry logic + exponential backoff lagao |
| 5 | Sync LLM calls async endpoint mein | `await` wali async methods use karo ya `def` use karo |

---

## 💡 Pro Tips

1. **Multi-provider support** rakho — agar ek provider down ho toh fallback
2. **Streaming** always offer karo — UX bahut better hota hai
3. **Token counting** karo — cost control ke liye (`tiktoken` library)
4. **Caching** lagao repeated prompts pe — Redis use karo
5. **Structured output** ke liye Pydantic + `instructor` library use karo

---

> **Next Chapter:** [09 — Security](./09_security.md) →
