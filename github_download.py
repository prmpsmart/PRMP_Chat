# code to automate the download of github branches
import requests, os


def download_branch(user, repo, branch, dest=""):

    if dest:
        dest = dest + "/"
    filename = f"{dest}{repo}-{branch}.zip"
    if os.path.exists(filename):
        print(f"Already downloaded {filename}")
        return
    url = f"https://codeload.github.com/{user}/{repo}/zip/refs/heads/{branch}"

    print("Download of", filename, "started.")
    response = requests.get(url, allow_redirects=True)

    if b"404" == response.content:
        print(response.content)
    elif response.content:
        file = open(filename, "wb")
        file.write(response.content)
        print("Download of", filename, "finished.", end="\r")


user = "iamshaunjp"
repository = "flutter-beginners-tutorial"
branch = "lesson-%d"

# for num in range(4, 36): download_branch(user, repository, branch%num, dest=r'C:\Users\Administrator\Coding_Projects\Dart\Flutter\flutter_tutorial_for_bginners')


ss = requests.get(
    "https://9jaflaver.com/wp-content/uploads/2021/09/Lil_Smart_Shy_9jaflaver.com_.mp3",
    allow_redirects=True,
)

print(len(ss))
