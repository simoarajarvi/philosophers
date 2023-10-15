# Expertise Locator Framework - "Philosophers" PoC App


## RAG - based locator
The RAG based locator applies two distinct NLP techniques for pinpointing domain-specific expertise, typically within expansive knowledge organizations. The system is structured loosely around the [Retrieval-Augmented Generation (RAG)](https://arxiv.org/pdf/2005.11401.pdf) pattern and is executed in two distinct phases:

1. The initial phase employs cached document embeddings to represent the expertise of individual participants. These embeddings are derived from an array of data sources, such as publications, project narratives, résumés and other pertinent artifacts. Upon receiving a query, the system performs a retrieval action against these embeddings, generating a preliminary list of top-n candidates. This retrieval mechanism ensures the selection of experts whose expertise semantically aligns with the input query. The first phase retrieval does not generate textual metadata about the retrieval results.  

2. The secondary phase brings in a Large Language Model (LLM) for an in-depth evaluation of the initially identified candidates. The LLM generative model appraises the initial embeddings and offers a more refined ranking of experts. Moreover, it furnishes plain text explanations, detailing the rationale behind each expert's placement, thus enhancing the users' and contextual understanding of the results.

One of the primary advantages of this dual-phase approach is its scalability. By concentrating the resource-intensive LLM evaluations to a narrowed set of candidates, the system can handle vast repositories of expert documents more efficiently. This method is more scalable and also less complex compared to a fine-tuning strategy. 

### Example implementation 

In the "Philosophers" toy example, the procedure starts with the preprocessing of documents detailing the knowledge and background of experts, in this case 25 classic philosophers. During this phase, each document is transformed using an embedding model (OpenAI text-embedding-ada-002) to produce vector representations. (These embeddings serve as a distilled version of the philosophers' expertise, enabling efficient comparison and retrieval based on semantic similarity.)

The experts selected as the top-N candidates by a vector distance metric (e.g. cosine) are then introduced to a Large Language Model (LLM) API, such as OpenAI gpt-4. At this juncture, various parameters like tone, temperature, and prompt are configured according to user-defined settings. This step facilitates a more granular evaluation of the candidate documents by the LLM, factoring in the user preferenes and requirements of specific use cases. 

Concluding the procedure, the third phase focuses on result presentation. The LLM outputs the most relevant experts based on the evaluation, supplemented with brief explanations that decode the rationale behind each score. To add a layer of interpretability, the system dispenses metrics related to retrieval confidence. This metric offers a quantitative measure of the confidence level associated with each recommendation. 


### Screen captures
The PoC is hosted as a web app, only a developmen server implementation - **Not to be used in production** - is provided in this repo. At server startup, a directory with expertise documents is scanned and compared against cached embeddings. If updates are found, the embedding model is called to process the updated documents and cache them. At the landing page, the user will enter a question (or a describe the topic(s) where help is needed). In the toy-example, a user is looking for a classic philosopher to help with 6th grade math:

![Screenshot of home page](./img/question.png)

Whe the user submits a question, the question text is first processed the embedding model and then compared against the cached document embeddings representing the available experts. In the toy-example, each philosopher was given a 4 paragraph summary of their achievements and areas of exploration. After the top-N experts are processed by the second phase LLM model, the sorted results are sent to the browser asynchronously and the results page is updated with the best experts, and explanations for the selections. 

![Screenshot of home page](./img/results.png)

With the current version, the expertise documents are not highlighted for areas that support a candate's selection. Since the results are produced at a semantic level, this is not a trivial task, but it would be very helpful feature for an end user and implementation is under research.   

![Screenshot of home page](./img/expertise_basis.png)

