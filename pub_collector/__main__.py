from pub_collector import users, publications
import json


def main() -> None:
    if False:
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

    # Example input
    input_data = [
        {
            "uid": "dfafeb1c-1902-4726-a032-f91483f99b09",
            "google_scholar_id": "KiMZogkAAAAJ",
        },
        {
            "uid": "bebbc63c-3d6b-4b08-b364-4f952d89337a",
            "google_scholar_id": "aZgSEiAAAAAJ",
        },
    ]

    result = {}
    for item in input_data:
        # Get author by Google Scholar ID
        # author = users.get_author_by_google_scholar_id(item["google_scholar_id"])
        # if not author:
        #     print(
        #         f"Author not found for Google Scholar ID: {item['google_scholar_id']}"
        #     )
        #     continue

        # author_details = users.get_all_details_for_author(author)
        # if not author_details:
        #     print(f"Could not retrieve details for author: {author}")
        #     continue
        # Get all publications for the author
        # publications = users.quick_list_author_publications(author_details, since_year=2020)
        publications = publications.quick_list_author_publications(
            item["google_scholar_id"], since_year=2020
        )
        if not publications:
            print(f"No publications found for Google scholar ID: {item["google_scholar_id"]}")
            continue

        print(publications)

        result[item["uid"]] = {
            "google_scholar_id": item["google_scholar_id"],
            "publications": publications,
        }

        # Output the result
        print(json.dumps(result, indent=4))

        # Optionally save to file
        with open("scholar_publications.json", "w") as f:
            json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()
