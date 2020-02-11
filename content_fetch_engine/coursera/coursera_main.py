from coursera_scrapper import scrapper

def main():
    search_term_list = [
        'artificial intelligence',
        'big data analytics',
        'blockchain',
        'cloud computing',
        'cyber security',
        'data mining',
        'deep learning',
        'face recognition',
        'image processing',
        'IoT',
        'machine learning',
        'network security',
        'neural network',
        'smart grid'
    ]

    for search_term in search_term_list:
        print(search_term)
        scrapper(search_term)

if __name__=="__main__":
    main()