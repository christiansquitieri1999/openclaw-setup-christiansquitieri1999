# LLM Prompt Injection Attack Notes

*Saved 2026-08-01*

---

## 1. Astra Security — "Prompt Injection Attacks in LLMs: Complete Guide for 2026"

**Source:** https://www.getastra.com/blog/ai-security/prompt-injection-attacks/

This comprehensive guide frames prompt injection as the leading security risk in LLM applications, rooted in the fundamental architectural limitation that models cannot distinguish between trusted system instructions and untrusted user input. It breaks down direct injection (where attackers craft their own inputs to jailbreak guardrails) from the more dangerous indirect injection (where malicious payloads hide in documents, emails, websites, or images that the model processes on behalf of a user). The article highlights the landmark 2023 Bing Chat "Sydney" leak as proof of how simple prompts can expose internal system logic, and discusses how obfuscation techniques like encoding, multilingual injection, and hidden content let attackers bypass content filters. Mitigation focuses on layered controls — input sanitization, output validation, and adversarial testing — rather than any single fix.

---

## 2. Kunal Ganglani — "Prompt Injection in 2026: Still OWASP's Number One LLM Vulnerability"

**Source:** https://www.kunalganglani.com/blog/prompt-injection-2026-owasp-llm-vulnerability

This FAQ-style guide explains why prompt injection remains at the top of OWASP's LLM Top 10 even years after it was first documented. The author distinguishes prompt injection (any manipulation of an LLM through crafted inputs) from jailbreaking (a subset that aims to bypass safety training entirely). A key insight is that neither RAG nor fine-tuning can prevent injection attacks — they improve output quality but don't solve the core problem of undifferentiated token streams. The article emphasizes that as LLMs gain tool access (sending emails, querying databases, making API calls), indirect injection becomes exponentially more dangerous because a single compromised agent can cascade failures across multi-agent systems. The recommended defense-in-depth strategy includes input sanitization, least-privilege tool scoping, strict schema validation on outputs, human-in-the-loop for high-stakes actions, and assuming the model will be compromised.

---

## 3. Iterathon — "LLM Prompt Injection Attacks & Defense 2026: Production Security Guide"

**Source:** https://iterathon.tech/blog/llm-prompt-injection-attacks-defense-2026-production-security-guide

This production-oriented technical guide covers the most recent attack vectors including Model Context Protocol (MCP) sampling vulnerabilities (CVE-2025-54135 and CVE-2025-54136), which demonstrated how manipulating MCP configurations in tools like Cursor IDE could let attackers override system instructions by injecting malicious context before validation. It also details the Microsoft 365 Copilot "EchoLeak" vulnerability, where hidden HTML instructions or white-on-white text in emails could trigger data exfiltration when users asked Copilot to summarize their inbox. Multimodal injection is covered extensively — attackers can embed invisible text in images using steganography or low-contrast overlays, use ultrasonic frequencies for audio injection, and combine cross-modal payloads. The guide provides production code examples for multi-layer defenses: input validation pipelines, architectural security patterns like privilege separation, and output schema enforcement against strict types.