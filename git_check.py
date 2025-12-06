import subprocess
import os

os.chdir(r"c:\Users\dietmar.breihof\OneDrive - Breihof-IT GmbH\Aktien\didis-premium-app")

print("=" * 50)
print("GIT DIAGNOSE")
print("=" * 50)

# Git Status
print("\n--- GIT STATUS ---")
result = subprocess.run(["git", "status"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Git Remote
print("\n--- GIT REMOTE -V ---")
result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Git Log
print("\n--- GIT LOG (letzte 5 Commits) ---")
result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Git Branch
print("\n--- GIT BRANCH ---")
result = subprocess.run(["git", "branch", "-vv"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Fetch und vergleiche mit Remote
print("\n--- GIT FETCH ---")
result = subprocess.run(["git", "fetch", "origin"], capture_output=True, text=True)
print(result.stdout if result.stdout else "Fetch OK")
if result.stderr:
    print("STDERR:", result.stderr)

# Vergleiche local mit remote
print("\n--- VERGLEICH LOCAL vs REMOTE ---")
result = subprocess.run(["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"], capture_output=True, text=True)
print(f"Ahead/Behind: {result.stdout.strip()}")
if result.stderr:
    print("STDERR:", result.stderr)
