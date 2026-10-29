$ git switch -c add-charts          # create and move to a new branch
# ...edit, add, commit as usual...
$ git switch main
$ git merge add-charts              # bring the work into main
$ git branch -d add-charts          # delete the finished branch
