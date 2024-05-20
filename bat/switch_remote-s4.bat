git config --unset-all remote.origin.fetch
git remote set-branches --add origin art/main-s4
git fetch --all
git reset --hard 
git switch art/main-s4
git reset --hard origin art/main-s4

git lfs prune origin 