from scholarly import scholarly

author_id = 'VynxFpEAAAAJ'
yr = '2023'

def scrape_publications(author_id: str, yr: str):
    author = scholarly.search_author_id(author_id)

    list = scholarly.fill(author, sections=['publications'],sortby='year', publication_limit=100)
    pubs = list['publications']
    pubs_year = [pub for pub in pubs if (pub['bib']['pub_year'] == yr)]

    return pubs_year

def make_citations(pubs: dict):
    '''
    :param pubs:
    :return:
    '''

    citations = []
    dud = []

    for pub in pubs:
        cite = True
        num_exists = True
        vol_exists = True
        pages_exist = True

        citation = ''

        pub = scholarly.fill(pub)
        bib = pub['bib']

        authors = bib['author']
        authors_list = split_authors(authors)
        APA_authors = apa_authors(authors_list)
        APA_authors_string = stringify_apa_authors(APA_authors)

        title = bib['title']
        year = str(bib['pub_year'])
        journal = bib['journal']

        if 'volume' in bib:
            volume = bib['volume']
        else:
            volume = ''
            dud.append(bib)
            cite = False
            vol_exists = False

        if 'number' in bib:
            number = bib['number']
        else:
            number = ''
            dud.append(bib)
            cite = False
            num_exists = False

        if 'pages' in bib:
            pages = bib['pages']
        else:
            pages = ''
            dud.append(bib)
            cite = False
            pages_exist = False

        if cite == True:
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '; '
            citation += number + '('
            citation += volume + '): '
            citation += pages + '.'
        elif num_exists and pages_exist and not vol_exists:
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '; '
            citation += number + ': '
            # citation += volume + '): '
            citation += pages + '.'
        elif vol_exists and pages_exist and not num_exists:
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '; '
            citation += '('
            citation += volume + '): '
            citation += pages + '.'
        elif vol_exists and num_exists and not pages_exist:
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '; '
            citation += number + '('
            citation += volume + ').'
        elif num_exists and not (pages_exist or vol_exists):
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '; '
            citation += number + '.'
            # citation += volume + '): '
            # citation += pages + '.'
        elif vol_exists and not (pages_exist or num_exists):
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '; '
            citation += '('
            citation += volume + ').'
            # citation += pages + '.'
        elif pages_exist and not (num_exists or vol_exists):
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '; '
            citation += pages + '.'
        else:
            citation += APA_authors_string + '. '
            citation += title + '. '
            citation += journal + '. '
            citation += year + '.'


        citations.append(citation)

    return citations, dud


def split_authors(string:str):
    '''
    Takes authors in string, seperated by "and" and outputs list of authors without "and"
    :param list:
    :return:
    '''

    authors = string.split(' and ')

    return authors


def apa_authors(authors:list):
    '''
    Takes list of full author names and turns into LastName Initial
    E.g., Fidel Vila-Rodriguez = Vila-Rodriguez F
    :param list:
    :return:
    '''

    ab_authors = []

    for author in authors:
        names = author.split(' ')
        last_name = names[-1]
        abbreviation = last_name + ' '

        for i in range(len(names)-1):
            name = names[i]
            ab = name[0]
            abbreviation += ab

        ab_authors.append(abbreviation)


    return ab_authors


def stringify_apa_authors(authors: list):
    '''
    Takes list of authors, outputs a single string with commas between each.
    :param authors:
    :return:
    '''

    string = ''

    for i in range(len(authors)-1):
        string += authors[i] + ', '

    string += authors[-1]

    return string


def make_wall_of_citations(citations: list):
    '''
    takes list of strings, outputs single string with each element separated by 2 line breaks
    :param citations:
    :return:
    '''

    string = ''

    for citation in citations:
        string += citation + '\n'

    return string


pubs = scrape_publications(author_id, yr)
cites, dud = make_citations(pubs)

citations_text = make_wall_of_citations(cites)

# print(cites)
print(citations_text)

# print(dud)

# print(stringify_apa_authors(apa_authors(['Fidel Vila-Rodriguez', 'William John Sun', 'W. John'])))

# print(split_authors('Fidel Vila-Rodriguez and William John Sun and W. John'))