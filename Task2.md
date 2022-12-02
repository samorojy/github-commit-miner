**How would you filter the commits to choose only those which are related to the changes in the DL NN design? There is
no
need to write any code, just describe in text what you would do and why.**

1. Initially I would go through the commits in the kernel files and check them against the diff. For example, like you
   can do in IDEA to distinguish between functional commits and refactoring.
2. Take the code of the file in which the commit is made. Distinguish the importance of the change by the received
   arguments of the function in which the change is made