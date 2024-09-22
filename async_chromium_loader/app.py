import json

from playwright.sync_api import sync_playwright


def get_page(url: str, user_agent: str = None, extract_main: bool = False) -> dict:
    print("start get_html")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            args=[
                "--single-process",
                "--no-zygote",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--headless=new",
            ]
        )

        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        response = page.goto(url=url)

        content = page.content()
        title = page.title()

        browser.close()

        return {
            "status": response.status,
            "content": transform_content(content) if extract_main else content,
            "title": title,
        }


def transform_content(html: str) -> str:
    from langchain_community.document_transformers import BeautifulSoupTransformer
    from langchain_core.documents import Document

    bs_transformer = BeautifulSoupTransformer()

    doc = Document(page_content=html)

    docs_transformed = bs_transformer.transform_documents(
        [doc], tags_to_extract=["main"]
    )

    print(len(docs_transformed))

    return docs_transformed[0].page_content


def strtobool(val) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value {!r}".format(val))


def lambda_handler(event, context):

    body = json.loads(event["body"])
    url = body["url"]
    user_agent = body["user-agent"] if "user-agent" in body else None
    extract_main = strtobool(body["extract-main"]) if "extract-main" in body else False

    response = get_page(url=url, user_agent=user_agent, extract_main=extract_main)

    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
