from flask import Flask, request
import wikipedia

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Welcome Hassainar!"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    sum = 0
    query_result = req.get('queryResult')
    if query_result.get('action') == 'wikipedia.search':
        search = str(query_result.get('parameters').get('search'))

        search_result = wikipedia.search(search)
        fulfillmentText = str(search_result)+"\n\nUse 'About + word' to get summary.\nUse 'URL of + word' to get content link.\nUse 'Image of + word' to get images link.\nUse 'Reference link of + word' to get reference from different websites or research, etc."

    elif query_result.get('action') == 'wikipedia.summary':
        summary = str(query_result.get('parameters').get('summary'))

        summary_result = wikipedia.summary(summary)
        fulfillmentText = summary_result+"\n\nUse 'Entire information about + word' to get full page content."

    elif query_result.get('action') == 'wikipedia.content':
        contents = str(query_result.get('parameters').get('content'))

        content_result = wikipedia.page(contents)
        done = content_result.content
        fulfillmentText = done+"\n\nUse 'About + word' to get brief summary."

    elif query_result.get('action') == 'wikipedia.page':
        pages = str(query_result.get('parameters').get('page'))

        page_result = wikipedia.page(pages)
        page_url = page_result.url
        fulfillmentText = page_url

    elif query_result.get('action') == 'wikipedia.image':
        images = str(query_result.get('parameters').get('image'))

        image_result = wikipedia.page(images)
        image_id = image_result.images
        fulfillmentText = str(image_id)

    elif query_result.get('action') == 'wikipedia.link':
        links = str(query_result.get('parameters').get('link'))

        link_result = wikipedia.page(links)
        link_id = link_result.links
        fulfillmentText = str(link_id)

    elif query_result.get('action') == 'wikipedia.language':
        language = str(query_result.get('parameters').get('language'))

        wikipedia.set_lang(language)
        fulfillmentText = "You changed the language."

    return {
        "fulfillmentText": fulfillmentText,
        "displayText": '25',
        "source": "webhookdata"
    }


if __name__ == '__main__':
    app.run(debug=True)
