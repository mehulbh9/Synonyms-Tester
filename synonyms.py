import math
import collections

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    if len(vec1) > len(vec2):
        focus_d = vec1
        other_d = vec2
    else:
        focus_d = vec2
        other_d = vec1

    focus_items = focus_d.items()
    focus_keys = list(focus_d.keys())
    focus_vals = list(focus_d.values())
    other_keys = list(other_d.keys())
    other_vals = list(other_d.values())

    dot_prod = 0
    mag_u_sq = 0
    mag_v_sq = 0
    counter = 0

    for i in range(len(focus_keys)):
        if focus_keys[i] in other_d.keys():
            dot_prod += focus_vals[i]*other_vals[other_keys.index(focus_keys[i])]
            counter += 1


    if counter == 0: #no common element
        return 0

    res = dot_prod/(norm(vec1)*norm(vec2))
    return res



def build_semantic_descriptors(sentences):
    res_d = {}
    uni_words = []

    for sentence in sentences:
        for word in sentence:
            sub_dict = dict(collections.Counter(list(filter(lambda a: a != word, sentence))))
            if word not in res_d:
                res_d.update({word:sub_dict})
            else:
                for elem in sub_dict:
                    if elem in res_d[word]:
                        res_d[word][elem] += sub_dict[elem]
                    else:
                        res_d[word].update({elem:sub_dict[elem]})

    return res_d


def build_semantic_descriptors_from_files(filenames):
    giant_list = []
    sub_list = []
    text = ""
    for file in filenames:
        text += open(file, "r", encoding="latin1").read().lower()

    text = text.replace("!",".")
    text = text.replace("?",".")
    text = text.replace(","," ")
    text = text.replace("-", " ")
    text = text.replace("--", " ")
    text = text.replace(":", " ")
    text = text.replace("  ", " ")
    text = text.replace(";", " ")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("*", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace("/", " ")
    text = text.replace('"', " ")
    text = text.replace("ã", " ")
    text = text.replace("©", " ")
    text = text.replace("§", " ")
    text = text.replace("'", " ")
    text = text.replace("_", " ")
    text = text.replace("¢", " ")
    text = text.replace("¨", " ")
    text = text.replace("¯", " ")
    text = text.replace("®", " ")
    text = text.replace("´", " ")
    text = text.replace("ª", " ")
    text = text.replace("@", " ")
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    text = text.replace("$", " ")
    text = text.replace("#", " ")
    text = text.replace('\\', " ")
    text = text.replace("â", " ")
    text = text.replace("°", " ")
    text = text.replace('«', " ")
    text = text.replace("«", " ")
    text = text.replace("%", " ")
    text = text.replace("º", " ")
    text = text.replace("³", " ")
    text = text.replace("¶", " ")
    text = text.replace("¡", " ")
    text = text.replace("=", " ")
    text = text.replace("½", " ")
    text = text.replace("¼", " ")
    text = text.replace("¤", " ")
    text = text.replace("å", " ")
    text = text.replace("¦", " ")
    text = text.replace("  ", " ")
    sub_list = text.split(".")
    for i in range(len(sub_list)):
            sub_list[i] = list(filter(lambda a: a != "", sub_list[i].split(" ")))
    giant_list.extend(sub_list)
    return build_semantic_descriptors(giant_list)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    score = []
    for choice in choices:
        if word not in semantic_descriptors or choice not in semantic_descriptors:
            score.append(-1)
        else:
            score.append(similarity_fn(semantic_descriptors[word],semantic_descriptors[choice]))
    return choices[score.index(max(score))] #this would return a word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    words = []
    answers = []
    choices = []
    correct_ans = 0

    f = open(filename, encoding="latin1").readlines()
    for i in range(len(f)):
        f[i] = f[i].replace("\n", "").replace("\t", "").split(" ")
        words.append(f[i][0])
        answers.append(f[i][1])
        choices.append(f[i][2:])

    for index in range(len(words)):
        answer = most_similar_word(words[index], choices[index], semantic_descriptors, similarity_fn)

        if answer == answers[index]:
            correct_ans += 1
    res = correct_ans/len(words)*100

    return res


if __name__ == "__main__":
    #l = []
    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("retest.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")