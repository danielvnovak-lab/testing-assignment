
# Getting started

# Install git on your machine.
  - Linux: https://git-scm.com/install/linux
  - Mac: https://git-scm.com/install/mac
  - Windows: https://git-scm.com/downloads/win

Open VSCode and open the terminal. 

> git clone 'https://project.url'

project.url = Project URL you want to clone.

You now have a local copy of the project.

## Setting up

### Set your email & name for local commits
> git config --global user.email "your.email@student.edu.au"

> git config --global user.name "Your Name"

### Set your account for github commits
> gh auth login

Instructions on how to install 'gh' can be found below.
https://docs.github.com/en/github-cli/github-cli/quickstart

## Updating your local copy 

To update the local copy with the latest changes from the remote copy.
> git pull


## Saving your changes

To save your changes made to the local copy.
1. Add all the changes you made to the local copy.
> git add --all .

2. Commit the changes.
> git commit 

3. Push the changes to the remote copy.
> git push

Now the remote copy of the project is updated with your changes.

## Working with branches

Changes should be made on a branch instead of committing straight to `main`. A branch is a separate line of work you can experiment on safely.

1. Create a branch and switch to it. Give it a short, descriptive name.
> git checkout -B "new-branch-name"

For example:
> git checkout -B testing/blah-blah

(`-B` creates the branch, or resets it if it already exists.)

2. Make your changes, then add and commit them (see [Saving your changes](#saving-your-changes)).

3. Push your branch to the remote copy. The `-u` flag links your local branch to a new branch on the remote.
> git push -u origin "new-branch-name"

## Opening a pull request

A pull request (PR) asks your teammates to review the changes on your branch before they are merged into `main`.

1. Next time you visit your branch on the GitHub website, you will see the option to open a pull request.

2. Give the PR a clear title and a short description of what changed and why.

3. Teammates review the PR and leave comments. To address feedback, push more commits to the same branch and the PR updates automatically.

4. Once approved, merge the PR with the green 'Merge pull request' button, or from the terminal.
> gh pr merge

5. Clean up and get the merged changes onto your local `main`.
> git switch main
> git pull
> git branch -d "new-branch-name"

### Bonus - Updating commit message editor

The below command sets Git to use VSCode for writing your commit messages.
> git config --global core.editor "code --wait" 
