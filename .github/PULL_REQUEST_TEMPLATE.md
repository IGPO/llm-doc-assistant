# 📝 Pull Request Template

## 📌 Summary

<!-- Краткое описание, что делает этот PR -->
[Например: "Adds Docker support with Poetry and production-ready build pipeline."]

---

## 🎯 Motivation and Context

<!-- Зачем нужны эти изменения? Какие проблемы решаются или фичи добавляются? -->
[Например: "Current project lacked a containerized setup. This PR allows consistent environment setup and better deployment strategy."]

---

## 🔧 Implementation Details

- [x] Used Poetry with in-container virtual environment
- [x] Added Dockerfile with multi-stage build
- [x] Updated Makefile for Docker commands
- [x] Created docs/dev_vs_docker.md for documentation

---

## 🧪 How Has This Been Tested?

- [x] `make run` on host
- [x] `make run-docker` in container
- [x] Checked imports and FastAPI routing
- [ ] Manual PDF upload & LLM response checked

---

## 🔍 Checklist

- [ ] I have linked relevant issues (if any)
- [ ] I have added comments/docstrings to the new code
- [ ] I have updated relevant documentation
- [x] My changes generate no new warnings or errors
- [ ] I have tested edge cases and error handling

