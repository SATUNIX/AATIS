# AATIS
Experimental AATIS system. Agentic Accelerator for Testing Information Systems. 


AATIS is a fully-local, modular, dynamic assistant built on AutoGen 0.6 + Ollama (LLMs), equipped with a multi-layer memory stack (STM / MTM / LTM + FAISS), Constitution-guided governance, and self-improvement loops. Capable of self inference of long term goals for improving or modifying capability.
It can plan, research, write reports, answer questions from its own knowledge base, and even develop new tools, teams, or agents when it detects capability gaps.

## Under Development 

## Dev Note:

May take a few months since open source is not my full time. I wouldnt class this anywhere near sub-AGI even though some attributes and capabilities of self learning, self improvement, long term planning and state management described above are characteristics of a sub-AGI. With current models which can be ran efficient locally at the time of writing mid 2025, I dont see its self improvement capabilities being particularly ground breaking. but would help slightly, possibly, if it doesnt break itself which is more likely than not.

Current models which run under the hood just arent quite there yet but this system is designed to enable that forward view, provide a jumping off point for the next curious mind who finds this repo. So feel free to fork it if new tech comes out with proper memory management, better models and agent governance. Just make sure the system sticks to a proper constitution / spec.

---

graph TD

%% Core Input Interface
UI[TUI / External Module Input] --> Manager[Management Agent]
Manager -->|Digest Task| Router[SmartSelector / Router]

%% Team Selection
Router --> MethodologyTeam[Team: Methodology Builder]
Router --> QATeam[Team: Q&A / Memory Search]
Router --> DevTeam[Team: Technical Self-Improvement]
Router --> ResearchTeam[Team: Theory Expansion]
Router --> MemoryTeam[Team: Memory Management]
Router --> AuditTeam[Team: Constitution & Ethics Oversight]

%% Methodology Team Flow
MethodologyTeam --> ResearcherAgent
ResearcherAgent --> WebSearchTool
MethodologyTeam --> SummariserAgent
SummariserAgent --> SummariseTool
MethodologyTeam --> ReportWriterAgent
ReportWriterAgent --> ReportWriterTool
ReportWriterAgent -->|Output| MemoryWriter

%% QA Team Flow
QATeam --> QAAgent
QAAgent --> MemoryReaderTool

%% Dev Team Flow
DevTeam --> DevAgent
DevAgent --> ToolGeneratorTool
DevAgent --> FileWriterTool

%% Theory Team Flow
ResearchTeam --> TheoryAgent
TheoryAgent --> WebSearchTool
TheoryAgent --> SummaryAndInsightsTool

%% Memory Team Flow
MemoryTeam --> MemoryAgent
MemoryAgent --> FaissStore[FAISS Vector Store]
MemoryAgent --> MemoryIndexerTool
MemoryAgent --> MemoryReaderTool
MemoryAgent --> MemoryUpdaterTool

%% Manager Task Loop
Manager -->|Update Task State| TaskStateEngine
Manager -->|Track Progress| TaskMemoryEngine

%% Constitution
Manager -->|Compliance Check| ConstitutionRuleset
AuditTeam -->|Monitors| ConstitutionRuleset

%% Shared Memory Bus
FaissStore <--> MemoryReaderTool
FaissStore <--> MemoryWriter
FaissStore <--> MemoryUpdaterTool
FaissStore <--> TaskMemoryEngine

%% Output
ReportWriterAgent --> MarkdownOutput[(Markdown Report)]
QAAgent --> QAResponse[(Answered Questions)]
DevAgent --> NewTools[(Improved Tools)]

style ConstitutionRuleset fill=#fdd,stroke=#900,stroke-width=2px
style Manager fill=#bbf,stroke=#00f,stroke-width=2px
style FaissStore fill=#dfd,stroke=#0a0,stroke-width=2px
style TaskMemoryEngine fill=#ffd,stroke=#aa0,stroke-width=2px
style TaskStateEngine fill=#ffd,stroke=#aa0,stroke-width=2px
