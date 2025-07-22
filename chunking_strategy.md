# Custom Chunking Strategy for Tables and Cross-References

## Overview
Banking documents often contain complex tables and cross-references (e.g., "See Table 3.2"). Standard text splitting can break these relationships, leading to context loss and inconsistent answers. This project uses a hybrid chunking approach to preserve table integrity and cross-reference context.

## Approach
- **UnstructuredElementNodeParser** (from LlamaIndex) is used to parse documents into structured nodes, preserving tables and hierarchical relationships.
- Each node (table, section, etc.) is extracted as a coherent chunk, maintaining header-data relationships.
- **RecursiveCharacterTextSplitter** is then applied to further split large nodes into manageable, model-friendly chunks (≤512 tokens, ~2000 characters), ensuring no chunk exceeds the embedding model's input limit.
- Metadata is preserved and sanitized for each chunk, allowing for accurate retrieval and traceability.

## Cross-Reference Handling
- Chunks containing references (e.g., "See Table 3.2") retain enough surrounding context to make the reference meaningful.
- Table headers and footnotes are kept with their data rows whenever possible.
- During retrieval, semantically similar or referenced chunks are likely to be retrieved together, improving answer consistency.

## Benefits
- **Table context is preserved**: Answers about table data remain accurate.
- **Cross-references are meaningful**: Users can ask about referenced tables or sections and get coherent answers.
- **Regulatory and compliance information is less likely to be fragmented.**

## Example
> "What is the maximum LTV for retail centers?"
- The system retrieves the chunk containing Table 3.1 and its explanatory text, ensuring the answer includes both the value and its context. 