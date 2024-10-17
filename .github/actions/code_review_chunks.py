import os
import openai
from github import Github
import github
import git
import json
import textwrap
from dotenv import load_dotenv
import shutil
import tiktoken
import re
load_dotenv()

# Load OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')



def count_tokens(text):
    """
    Counts the number of tokens in a given text using OpenAI's tokenizer.

    Args:
        text (str): The input text to count tokens for.

    Returns:
        int: The number of tokens in the text.
    """
    # Use the tokenizer for GPT-3.5 or GPT-4 based models
    tokenizer = tiktoken.get_encoding("cl100k_base")

    # Encode the text and count the number of tokens
    return len(tokenizer.encode(text))


def get_all_files(repo, branch_name):
    """
    This function retrieves all files from the specified branch.

    Args:
        repo (Repo): The Git repository object.
        branch_name (str): The branch name to fetch files from.

    Returns:
        list: A list of file paths in the specified branch.
    """
    return [item.path for item in repo.tree(branch_name).traverse()]

def get_changed_files(pr):
    """
    This function fetches the files that were changed in a pull request,
    returns both the base and PR version of the files, along with the diff.

    Args:
        pr (PullRequest): The pull request object.

    Returns:
        dict: A dictionary containing the file paths as keys and a tuple of (base_content, pr_content, diff) as values.
    """
    # Clone the repository and checkout the PR branch
    repo_path = './repo'
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    repo = git.Repo.clone_from(pr.base.repo.clone_url, to_path=repo_path)

    # Define the branch names
    base_ref = f"origin/{pr.base.ref}"
    head_ref = f"origin/{pr.head.ref}"

    # Get all files from both branches
    base_files = get_all_files(repo, base_ref)
    pr_files = get_all_files(repo, head_ref)

    # Create a set of all unique files from both branches
    all_files = set(base_files).union(set(pr_files))
    all_files = list(all_files)
    all_files.sort()

    all_files = list(all_files)
    all_files.sort()

    # Initialize an empty dictionary to store file contents and diffs
    files = {}
    codebase = {}
    for file_path in all_files:
        try:
            # Get the diff between the base and PR branch for the file
            diff = repo.git.diff(f"{base_ref}:{file_path}", f"{head_ref}:{file_path}")


            # Get the content of the base and PR versions of the file
            base_content = repo.git.show(f"{base_ref}:{file_path}")
            pr_content = repo.git.show(f"{head_ref}:{file_path}")
            codebase[file_path] = base_content

            if diff and "." in file_path:  # Only store files with differences
                files[file_path] = (base_content, pr_content, diff)
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    return files


Token_limit = 4000

def send_to_openai(files):
    reviews = []

    for file_path, (base_content, pr_content, diff) in files.items():
        if count_tokens(base_content) + count_tokens(pr_content) > Token_limit:
            base_chunks = textwrap.wrap(base_content, width=int(Token_limit / 2))
            pr_chunks = textwrap.wrap(pr_content, width=int(Token_limit/ 2))  # Adjust chunk size


            for base_chunk , pr_chunk in zip(base_chunks,pr_chunks):
                content = (
<<<<<<< HEAD
                    f"You are responsible to extract that part of code (user-defined function , variable , class, data structure) from the pr files whose definition is different and changed in pr files with respect to base files"
                    f"Please find all the user-defined functions and variables and classes and any data structures etc that are affected by that part of code.\n"
                    f"please check each and every line of code that is different"
                    f"output must be in this format -> elements' name only"
                    f"Do not provide the code, explanations, or any other details"
                    f"do not consider inbuilt functions"
                    f"Do not write print statements provide the function under which print statement differs"
                    f"do not write added , updated, modified, function, variable ,etc just find the elements' name that are affected or changed"
                    f"File: {file_path}\n"
                    f" base files: {base_chunk}"
                    f"pr files: {pr_chunk}"
                )

=======
            f"You are responsible to extract that part of code (function , variable , class, data structure) from the pr files whose definition is different and changed in pr files with respect to base files"
            f"Please find all the functions and variables and classes and any data structures etc that are affected by that part of code.\n"
            f"please check each and every line of code that is different"
            f"output must be in this format -> elements' name only"
            f"Do not provide the code, explanations, or any other details"
            f"Do not consider print statements provide the function under which print statement differs"
            f"do not write added , updated, modified, function, variable ,etc just find the elements' name that are affected or changed"
            f"File: {file_path}\n"
            f" base files: {base_content}"
            f"pr files: {pr_content}"
        )
>>>>>>> origin/with_chunks


                message = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": content}],
                    temperature = 0.3,
                )
                response_content = message['choices'][0]['message']['content']
                lines = [line.strip() for line in response_content.splitlines() if line.strip()]
                reviews.extend(lines)
        else:
            content = (
<<<<<<< HEAD
                f"You are responsible to extract that part of code (user-defined function , variable , class, data structure) from the pr files whose definition is different and changed in pr files with respect to base files"
                    f"Please find all the user-defined functions and variables and classes and any data structures etc that are affected by that part of code.\n"
                    f"please check each and every line of code that is different"
                    f"output must be in this format -> elements' name only"
                    f"Do not provide the code, explanations, or any other details"
                    f"do not consider inbuilt functions"
                    f"Do not write print statements provide the function under which print statement differs "
                    f"do not write added , updated, modified, function, variable ,etc just find the elements' name that are affected or changed"
                f"File: {file_path}\n"
                f" base files: {base_content}"
                f"pr files: {pr_content}"
            )
=======
            f"You are responsible to extract that part of code (function , variable , class, data structure) from the pr files whose definition is different and changed in pr files with respect to base files"
            f"Please find all the functions and variables and classes and any data structures etc that are affected by that part of code.\n"
            f"please check each and every line of code that is different"
            f"output must be in this format -> elements' name only"
            f"Do not provide the code, explanations, or any other details"
            f"Do not consider print statements provide the function under which print statement differs"
            f"do not write added , updated, modified, function, variable ,etc just find the elements' name that are affected or changed"
            f"File: {file_path}\n"
            f" base files: {base_content}"
            f"pr files: {pr_content}"
        )
>>>>>>> origin/with_chunks

            message = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": content}],
                temperature = 0.3,
            )
            response_content = message['choices'][0]['message']['content']
            lines = [line.strip() for line in response_content.splitlines() if line.strip()]
            reviews.extend(lines)



    return reviews

def post_comment(pr, comment):
    """
    This function posts a comment on the pull request with the review.

    Args:
        pr (PullRequest): The pull request object.
        comment (str): The comment to post.
    """
    # Post the OpenAI's response as a comment on the PR


def find_usages_in_codebase(changed_lines, codebase):
    reviews = {}
    TOKEN_LIMIT = 3000  # Define a reasonable token limit

    for file_path, (base_content, pr_content, diff) in codebase.items():
        # Check token count and split content if necessary
        base_token_count = count_tokens(base_content)

        # If the file is too large, split the content into chunks
        if base_token_count > TOKEN_LIMIT:
            chunks = textwrap.wrap(base_content, width=int(TOKEN_LIMIT / 2))  # Adjust chunk size
        else:
            chunks = [base_content]  # If it's within limits, just process as is

        for chunk in chunks:
            content = (
                f"Your task is to find the lines in the file provided to you that are affected by the following functions or elements provided in changed lines."
                f"Return only the line numbers and code where changes are happening in the file content in concised and generalised way.\n"
                f"if you donot find any change or effect or similarity return none"
                f"output format -> line number : only code in respective line"
                f"for example -> Line 1 : def hello()"
                f"do not change the output format"
                f"do not write added , updated, modified,  variable, function, affected etc in the output follow the example provided to you to give answer"

                f"Changed lines:\n{changed_lines}\n\n"
                f"Base file content:\n{chunk}\n\n"
                f"File: {file_path}\n"

            )

            try:
                message = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": content}],
                )
                response_content = message['choices'][0]['message']['content']

                if file_path not in reviews:
                    reviews[file_path] = []  # Initialize if not present
                lines = [line.strip() for line in response_content.splitlines() if line.strip()]
                reviews[file_path].extend(lines)

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    return reviews  # Store under a single key


def find_in_codebase_using_regex(changes, code_base):
    # Create a regex pattern from the list of changes
    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(term.strip()) for term in changes if term.strip()) + r')\b')

    matching_lines = {}

    # Iterate over each file in the code base
    for file_path, (base_content, pr_content, diff) in code_base.items():
        # Only search through Python files with a .py extension


        # Split the base content into lines and search for patterns
        for line_num, line in enumerate(base_content.splitlines(), 1):
            if pattern.search(line):  # Check if the pattern matches any line
                if file_path not in matching_lines:
                    matching_lines[file_path] = []
                matching_lines[file_path].append((line_num, line.strip()))  # Store the matching line with its number

    return matching_lines

def validate_repository_name(repository_name):
    # Ensure the format is 'owner/repo_name'
    parts = repository_name.split('/')
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) == 3:
        return parts[1], parts[2]  # Handle cases like 'owner/project/repo'
    else:
        return None


def main():
    """
    The main function orchestrates the operations of:
    1. Fetching changed files from a PR
    2. Sending those files to OpenAI for review
    3. Posting the review as a comment on the PR
    """
<<<<<<< HEAD
    repository_name = input("Provide a repo name (username/repo_name or username/project/repo): ")

    pull_request_number = int(input("Provide PR req no.: "))

    repo_parts = validate_repository_name(repository_name)
    if not repo_parts:
        print("Invalid repository name format. It should be 'owner/repo_name' or 'owner/project/repo'.")
        return

    owner, repo_name = repo_parts
    full_repo_name = f"{owner}/{repo_name}"
=======
    # If running locally, provide your own repository and PR data
    repository_name = input("Provide a repo name : username/repo_name -> ")  # Replace with your repository, e.g., 'openai/gpt'
    pull_request_number = int(input("Provide pull req no. : "))  # Replace with the pull request number you want to review
>>>>>>> origin/with_chunks

    g = Github(os.getenv('GITHUB_TOKEN'))

    try:
        repo = g.get_repo(full_repo_name)
        pr = repo.get_pull(pull_request_number)
    except github.GithubException as e:
        print(f"Failed to fetch repository or pull request: {e}")
        return

    files = get_changed_files(pr)


    if not files:
        print("No changed files found in the pull request.")
        return

    changed_lines = send_to_openai(files)
    print("Changed lines:\n", changed_lines)
    changed_lines = list(set(changed_lines))

    changes = find_in_codebase_using_regex(changed_lines, files)
    green_color = "\033[92m"
    reset_color = "\033[0m"

    for file in changes:
        print(f"{green_color}***********************{file}**********************{reset_color}")
        for line_num, match in changes[file]:
            print(f"{green_color}Line {line_num}: {match}{reset_color}")


if __name__ == "__main__":
    main()
