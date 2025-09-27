function Quick-Deploy {
    param([string]$message = "Quick update")
    git add .
    git commit -m $message
    git push origin main
}

# Dann einfach verwenden:
Quick-Deploy "Updated trading pages"