"""English templates for Retrieval-Augmented Generation (RAG) prompts.

This module defines the prompt templates used in the RAG pipeline, including:
- System instructions for the LLM
- Format for presenting retrieved document chunks
- Footer with the user's query and instruction to generate an answer

These templates use Python's string.Template for variable substitution.
Variables used:
- $doc_num: Document number for each retrieved chunk
- $chunk_text: The content of a retrieved document chunk
- $query: The user's original question

Usage:
    Typically loaded and processed by the TemplateParser class.
"""

from string import Template

#### RAG PROMPTS ####

#### System ####

system_prompt = Template("\n".join([
    "You are an assistant to generate a response for the user.",
    "You will be provided with a set of documents associated with the user's query.",
    "You have to generate a response based on the documents provided.",
    "Ignore the documents that are not relevant to the user's query.",
    "You can apologize to the user if you are not able to generate a response.",
    "You have to generate response in the same language as the user's query.",
    "Be polite and respectful to the user.",
    "Be precise and concise in your response. Avoid unnecessary information.",
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Content: $chunk_text",
    ])
)

#### Footer ####
footer_prompt = Template("\n".join([
    "Based only on the above documents, please generate an answer for the user.",
    "## Question:",
    "$query",
    "",
    "## Answer:",
]))