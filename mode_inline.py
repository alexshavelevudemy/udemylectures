from telebot import TeleBot, types
import json

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")

METHODS = []
METHODS_URLS = {}

"""
First i crate resources folder with methods json file.
API methods are keys and URLs are values.

Then in main file we crate load methods function.
It stores method names to list and method name as key and link as value to dict.
I call it before start polling

Next we have only one inline handler.
We check query len and if less that 3 chars simply skip it. 
That we get one by one method names from list. Ans if our query is part of name - store method name to results list

Ok, now we have results list with methods match our query.
Next we iterate by them. We create input text message content with method name and doc link we extract from dict by method name
Then we create Inline query result article with unique id, method name , message content.
And append this article to query results list.
and When we parse all results it's time to call answer inline query 
"""



def load_methods():
    with open('resources/methods.json') as file:
        data = json.loads(file.read())

        for k, v in data.items():
            METHODS.append(k)
            METHODS_URLS[k] = v


@bot.inline_handler(func=lambda query: True)
def inline(query):

    if len(query.query) < 3:
        return

    results = []
    for method_name in METHODS:
        if query.query in method_name:
            results.append(method_name)

    query_results = []
    for result_id, method_name in enumerate(results):

        input_message_content = types.InputTextMessageContent(message_text='[doc]({}) for {}'.format(
            METHODS_URLS[method_name], method_name
        ), parse_mode='markdown', disable_web_page_preview=True)

        result = types.InlineQueryResultArticle(id=str(result_id),
                                                title=method_name,
                                                description='add description',
                                                input_message_content=input_message_content
                                                )

        query_results.append(result)

    bot.answer_inline_query(inline_query_id=query.id,
                            results=query_results,
                            cache_time=1)


load_methods()
bot.polling()
