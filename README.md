# gpt-rag-scraping
Project to gather information from websites, providing support for the ingestion process of Microsoft's GPT-RAG architectural solution. [GPT-RAG](https://github.com/Azure/GPT-RAG/tree/main)

Simple Flask-developed API designed to support the scraping process. Used in conjunction with a Power Automate flow. (Coming soon)

The structure is straightforward:
- app.py: File responsible for launching the API and publishing the endpoints.
- requirements.txt: File describing the necessary libraries and dependencies.
- services/ExtractLinks: Contains the logic to retrieve all links present on the site to be scraped. These are used to match with the original host and perform recursive scraping, with a tree structure (from root to nodes).
- services/GetHTMLContent: Contains the logic to retrieve all content containing textual information, eliminating HTML content.

**Recommendations**
It is recommended to implement as functions.

**Planned improvements**
Support for sites with highly dynamic content (or JS), allowing the ignoring of iframes or pop-up content that could block access to the site's information.
