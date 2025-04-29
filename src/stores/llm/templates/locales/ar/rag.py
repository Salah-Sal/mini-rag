"""Arabic templates for Retrieval-Augmented Generation (RAG) prompts.

This module defines the Arabic language prompt templates used in the RAG pipeline, including:
- System instructions for the LLM
- Format for presenting retrieved document chunks
- Footer with the user's query and instruction to generate an answer

These templates use Python's string.Template for variable substitution.
Variables used:
- $doc_num: Document number for each retrieved chunk
- $chunk_text: The content of a retrieved document chunk
- $query: The user's original question

Usage:
    Typically loaded and processed by the TemplateParser class when Arabic language is selected.
"""

from string import Template

#### RAG PROMPTS ####

#### System ####

system_prompt = Template("\n".join([
    "أنت مساعد لتوليد رد للمستخدم.",
    "ستحصل على مجموعة من المستندات المرتبطة باستفسار المستخدم.",
    "عليك توليد رد بناءً على المستندات المقدمة.",
    "تجاهل المستندات التي لا تتعلق باستفسار المستخدم.",
    "يمكنك الاعتذار للمستخدم إذا لم تتمكن من توليد رد.",
    "عليك توليد الرد بنفس لغة استفسار المستخدم.",
    "كن مؤدباً ومحترماً في التعامل مع المستخدم.",
    "كن دقيقًا ومختصرًا في ردك. تجنب المعلومات غير الضرورية.",
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## المستند رقم: $doc_num",
        "### المحتوى: $chunk_text",
    ])
)

#### Footer ####
footer_prompt = Template("\n".join([
    "بناءً فقط على المستندات المذكورة أعلاه، يرجى توليد إجابة للمستخدم.",
    "## السؤال:",
    "$query",
    "",
    "## الإجابة:",
]))