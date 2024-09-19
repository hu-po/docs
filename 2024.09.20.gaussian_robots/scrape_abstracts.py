# pip install arxiv
import arxiv

# List of arXiv paper IDs
paper_ids = [
    "2409.08353",
    "2409.10161",
    "2409.08669",
    "2409.07759",
    "2409.08189",
    "2409.07456",
    "2409.07441",
    "2409.04751",
    "2406.18717",
    "2409.10216"
]

# Output file
output_file = "abstracts.txt"

# Open the output file in write mode
with open(output_file, "w") as f:
    # Iterate over each paper ID
    for paper_id in paper_ids:
        # Search for the paper on arXiv
        search = arxiv.Search(id_list=[paper_id])

        # Fetch the result (this will only be one result for each paper_id)
        result = next(search.results())

        # Write the paper details to the file
        f.write(f"Title: {result.title}\n")
        f.write(f"Authors: {', '.join([author.name for author in result.authors])}\n")
        f.write(f"Published Date: {result.published}\n")
        f.write(f"Last Updated: {result.updated}\n")
        f.write(f"DOI: {result.doi if result.doi else 'N/A'}\n")
        f.write(f"Primary Category: {result.primary_category}\n")
        f.write(f"arXiv URL: {result.entry_id}\n")
        f.write(f"PDF URL: {result.pdf_url}\n")
        f.write(f"Abstract: {result.summary}\n")
        f.write("\n" + "-"*80 + "\n\n")

print(f"Abstracts and additional information have been written to {output_file}")
