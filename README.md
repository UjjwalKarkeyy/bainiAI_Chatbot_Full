<h1>bainiAI — Company-Focused Chatbot (LangChain + RAG + Gemini)</h1>

<p>
bainiAI is a domain-restricted corporate assistant designed to answer only company-related questions based on three internal documents. 
Using LangChain, Retrieval-Augmented Generation (RAG), and Google Gemini, the chatbot provides accurate and controlled responses
strictly grounded in the supplied knowledge base.
</p>

<hr>

<h2>Project Overview</h2>

<p>bainiAI responds using information from the following documents:</p>
<ul>
  <li>Company Overview</li>
  <li>IT Department Policies</li>
  <li>HR Policies</li>
</ul>

<p>
If a user asks something unrelated to the company, bainiAI declines to answer. 
Its behavior is controlled through structured prompt engineering to ensure alignment and consistency.
</p>

<hr>

<h2>Core Features</h2>

<ul>
  <li>Document-based answers using a RAG pipeline</li>
  <li>LangChain for retrieval, embeddings, and orchestration</li>
  <li>Gemini LLM for refined, instruction-following responses</li>
  <li>Prompt engineering to enforce behavior boundaries</li>
  <li>Strict domain-restricted answering</li>
  <li>Professional and consistent communication style</li>
</ul>

<hr>

<h2>How It Works</h2>

<h3>1. Document Processing</h3>
<ul>
  <li>Documents are split into chunks</li>
  <li>Text chunks are embedded</li>
  <li>Embeddings stored in a vector database (Chroma)</li>
</ul>

<h3>2. Retrieval</h3>
<ul>
  <li>User query is converted into vector form</li>
  <li>Closest document chunks are retrieved using similarity search</li>
</ul>

<h3>3. Reasoning</h3>
<ul>
  <li>Gemini receives the retrieved context</li>
  <li>Custom prompts guide it to stay within the company's domain</li>
  <li>Final answer is generated strictly from provided documents</li>
</ul>

<h3>4. Guardrails</h3>
<ul>
  <li>If no relevant information exists, the chatbot declines</li>
  <li>Non-company questions are rejected</li>
  <li>Prompts enforce tone, accuracy, and boundaries</li>
</ul>

<hr>

<h2>Architecture Overview</h2>

<pre>
User Query
   ↓
Retriever (LangChain)
   ↓
Vector DB (Chroma)
   ↓
Relevant Document Chunks
   ↓
Gemini LLM (with strict prompts)
   ↓
Company-Specific Answer
</pre>

<hr>

<h2>Purpose</h2>

<p>
The main goal of bainiAI is to simulate how real enterprises use LLMs internally:
systems that answer reliably from verified company material rather than producing generic or speculative information.
</p>

<hr>

<h2>Example Queries</h2>

<p>Valid queries include:</p>
<ul>
  <li>“What is our leave policy?”</li>
  <li>“Explain the IT onboarding process.”</li>
  <li>“Summarize the company's mission and values.”</li>
</ul>

<p>bainiAI will decline questions such as:</p>
<ul>
  <li>“Who is the president of the United States?”</li>
  <li>“Tell me a joke.”</li>
  <li>“How do I solve this math problem?”</li>
</ul>

<hr>

<h2>Technologies Used</h2>

<ul>
  <li>LangChain</li>
  <li>Retrieval-Augmented Generation (RAG)</li>
  <li>Google Gemini</li>
  <li>Chroma Vector Database</li>
  <li>Custom prompt engineering</li>
</ul>

<hr>

<h2>Future Enhancements</h2>

<ul>
  <li>Add more internal documents</li>
  <li>Introduce conversational forms (e.g., appointment booking)</li>
  <li>Integrate tool-based agents</li>
  <li>Deploy using FastAPI and Docker</li>
  <li>Create a full UI interface</li>
  <li>Add authentication and role-based responses</li>
</ul>

<hr>

<h2>License</h2>

<p>
This project is for educational and demonstration purposes.
</p>
