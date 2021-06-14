#!/usr/bin/env python
'''
file: repo_manager
author: adh
created_at: 6/14/21 12:20 PM
'''
import git.exc
from git import Repo
import os
import logging

logger = logging.getLogger(__name__)

class RepoManager(object):
    def __init__(self,working_dir,clone_url,branch="master"):
        self.workdir = working_dir
        self.url = clone_url
        self.branch = branch

        self.repo = Repo()

    def pull_or_clone(self):
        # does the path exist?

        if os.path.exists(self.workdir):
            logger.debug(f"Found possible clone at {self.workdir}")
            # is it a repo?
            r = Repo(self.workdir)
            assert not r.bare, "Cannot use a bare repository"

            logger.info(f"Using repo at {self.workdir}")
            self.repo = r
            self.pull()
        else:
            self.clone()

    def clone(self):
        logger.info(f"Cloning {self.url} to {self.workdir} (might take a while)")
        self.repo.clone_from(url=self.url,to_path=self.workdir,branch=self.branch)
        logger.debug(f"Cloning complete.")
        logger.debug(f"Branch is {self.branch}")

    def pull(self):
        o = self.repo.remotes.origin
        logger.info(f"Pulling from {o.refs.master.name}")
        o.pull()
        logger.debug(f"Pull complete")

def main():
    pass


if __name__ == '__main__':
    main()
