
# code to automate the download of github branches
import requests

def download_branch(user, repo, branch, dest=''):

    if dest: dest = dest+'/'
    filename = f'{dest}{repo}-{branch}.zip'
    url = f'https://codeload.github.com/{user}/{repo}/zip/refs/heads/{branch}'

    print('Download of', filename, 'started.')
    response = requests.get(url, allow_redirects=True)

    if b'404' == response.content: print(response.content)
    elif response.content:
        file = open(filename, 'wb')
        file.write(response.content)
        print('Download of', filename, 'finished.')





user = 'iamshaunjp'
repository = 'flutter-beginners-tutorial'
branch = 'lesson-%d'

for num in range(10, 36): download_branch(user, repository, branch%num, dest=r'C:\Users\Administrator\Coding_Projects\Dart\Flutter Tutorial for Beginners\codes')