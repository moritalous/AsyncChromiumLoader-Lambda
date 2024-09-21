import json

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer


def lambda_handler(event, context):

    body = json.loads(event["body"])
    url = body["url"]

    user_agent = "*"
    if "user-agent" in body:
        user_agent = body["user-agent"]

    loader = AsyncChromiumLoader(
        urls=[url],
        user_agent=user_agent,
    )
    documents = loader.load()

    bs_transformer = BeautifulSoupTransformer()
    documents = bs_transformer.transform_documents(
        documents,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "documents": [
                    {"metadata": d.metadata, "page_content": d.page_content}
                    for d in documents
                ],
            }
        ),
    }
