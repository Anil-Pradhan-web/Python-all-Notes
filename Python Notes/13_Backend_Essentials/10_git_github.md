# Git & GitHub Basics

### Simple Explanation (Hinglish)
**Git** ek version control system hai jo track karta hai ki code mein kya changes hue hain. **GitHub** ek online platform hai jahan hum apna Git code store aur share karte hain. Team mein kaam karne ke liye yeh essential hai!

### Theory (Clear + Structured)
- **Repository (Repo)**: Project folder jahan Git tracking hoti hai.
- **Commit**: Ek snapshot of changes at a point in time.
- **Branch**: Parallel version of code for developing features.
- **Merge**: Combining changes from different branches.
- **Pull Request (PR)**: Request to merge changes into main branch.

### Essential Git Commands

```bash
# Initial Setup (pehli baar)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Repository initialize karna
git init
# # Current folder ko Git repo bana do

# Changes stage karna
git add .
# # Saare changes stage kar do

git add filename.py
# # Sirf ek file stage karo

# Commit karna (save karna)
git commit -m "Added login functionality"
# # Message ke saath commit karo

# Remote repository connect karna
git remote add origin https://github.com/username/repo.git
git push -u origin main
# # Code GitHub pe push karo

# Branch banana aur switch karna
git branch feature-login
# # Nayi branch banao
git checkout feature-login
# # Us branch pe switch karo
git checkout -b feature-payment
# # Branch banao aur switch karo (shortcut)

# Changes merge karna
git checkout main
git merge feature-login
# # feature-login ko main mein merge karo

# Latest changes pull karna
git pull origin main
# # GitHub se latest code lao

# Status dekhna
git status
# # Kaunsi files modified hain

git log
# # Saare commits dekho

git diff
# # Changes dekho before staging
```

### Common `.gitignore` Entries
```bash
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/
.env
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

### Common Mistakes
1. **Sensitive data commit karna**: `.env`, passwords, API keys kabhi commit mat karna!
2. **Chhote commits**: Har chhote change pe commit karo descriptive message ke saath.
3. **Main branch pe direct push**: Hamesha branch banao, PR bhejo, review lo, fir merge karo.

### Interview Notes
1. **Git Flow**: Popular branching strategy with main, develop, feature, release, and hotfix branches.
2. **Resolve Merge Conflicts**: Jab do log same file edit karte hain, conflicts resolve karna seekho.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Initialize a Git repo, make a commit, and push to GitHub (or write down the commands).
2. **(Basic)** Explain the difference between `git add` and `git commit`.
3. **(Medium)** Create a feature branch, make changes, and write instructions to merge it into the main branch.
4. **(Medium)** Explain how `.gitignore` works and create a standard `.gitignore` for a Python backend project.
5. **(Hard)** Explain or write down a step-by-step guide to resolve a merge conflict between two branches.
