def is_spam_words(text, spam_words, space_around=False):
    text_lower = text.lower()

    for spam_word in spam_words:
        spam_words_lower = spam_word.lower()
        value = text_lower.find(spam_words_lower)

        if value != -1:
            if space_around == False:
                return True
            elif space_around == True \
                    and text_lower[value - 1] == " " or value == 0 \
                    and text_lower[value + len(spam_words_lower)] in (".", " "):
                return True
            else:
                return False