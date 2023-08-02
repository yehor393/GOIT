articles_dict = [
    {
        "title": "Endless ocean waters.",
        "author": "Jhon Stark",
        "year": 2019,
    },
    {
        "title": "Oceans of other planets are full of silver",
        "author": "Artur Clark",
        "year": 2020,
    },
    {
        "title": "An ocean That cannot be crossed.",
        "author": "Silver Name",
        "year": 2021,
    },
    {
        "title": "The ocean that you love.",
        "author": "Golden Gun",
        "year": 2021,
    },
]


def find_articles(key, letter_case=False):
    result = list()
    if letter_case:
        for i in range(len(articles_dict)):
            if articles_dict[i]["title"].find(key) != -1 or articles_dict[i]["author"].find(key) != -1:
                result.append(articles_dict[i])
    else:
        for i in range(len(articles_dict)):
            if (articles_dict[i]["title"].lower()).find(key) != -1 or (articles_dict[i]["author"].lower()).find(key) != -1:
                result.append(articles_dict[i])
    return result
print(find_articles("tha"))