from pub_collector import users, publications


def main() -> None:
    # Get first Google scholar object for an author
    # e.g., rhDs5gsAAAAJ
    print(users.get_first_author("Paul Ruth")["scholar_id"])

    # Get author by
    # e.g., {'container_type': 'Author', 'filled': ['basics'],
    # 'scholar_id': 'rhDs5gsAAAAJ', 'source': <AuthorSource.AUTHOR_PROFILE_PAGE: 'AUTHOR_PROFILE_PAGE'>,
    # 'name': 'Paul Ruth', 'affiliation': 'RENCI - UNC Chapel Hill', 'interests': [],
    # 'email_domain': '@renci.org', 'citedby': 1834}
    print(users.get_author_by_google_scholar_id("rhDs5gsAAAAJ"))

    print(users.get_author_by_name_email("Paul Ruth", "pruth@renci.org"))

    # Get first author
    author = users.get_first_author("Paul Ruth")
    # Get author details
    author_details = users.get_all_details_for_author(author)
    # List authors publications after 2020
    print(users.get_all_publication_titles(author_details), 2020)

    # Get Publication object by title
    fabric_pub = publications.search_publications(
        "Fabric: A national-scale programmable experimental network infrastructure"
    )
    # Get a list of publications that cited FABRIC paper
    print(publications.get_cited_by(fabric_pub))


if __name__ == "__main__":
    # main()
    main_pub()
