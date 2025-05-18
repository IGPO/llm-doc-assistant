.PHONY: help install run build run-docker stop rebuild

PYTHON ?= python
POETRY ?= poetry

# 🎯 Show help
help:  ## Show this help.
	@echo "📘 LLM Document Assistant — Makefile commands"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
        | awk 'BEGIN {FS = ":.*?## "}; {printf "🌟 \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# 🔧 Install dependencies using Poetry
install:  ## Install dependencies via Poetry
	$(POETRY) install

# 🚀 Run FastAPI locally
run:  ## Run FastAPI with Uvicorn
	$(POETRY) run uvicorn llm_doc_assistant.main:app --reload

# 🐳 Build Docker image
build:  ## Build Docker image
	docker build -t llm-doc-assistant-image .

# 🏃 Run Docker container
run-docker:  ## Run Docker container
	docker run -it --rm -p 8000:8000 \
	--name llm-doc-assistant-container \
	llm-doc-assistant-image
	#uvicorn llm_doc_assistant.main:app --host 0.0.0.0 --port 8000

# 🛑 Stop Docker container
stop:
	@echo "Stopping and removing container (if exists)..."
	@docker stop llm-doc-assistant-container 2>/dev/null || echo "Already stopped"
	@docker rm llm-doc-assistant-container 2>/dev/null || echo "Already removed"

# 🔁 Rebuild Docker image (with cleanup)
rebuild: stop build  ## Rebuild Docker image
	@echo "♻️  Rebuild complete"
