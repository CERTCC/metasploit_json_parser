import pandas as pd
import yaml
import os
import logging
import sys

from mtsp_parser import mtsp_json
from mtsp_parser.repo_manager import RepoManager

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
hdlr = logging.StreamHandler(sys.stdout)
logger.addHandler(hdlr)

CONFIGFILE = "./config.yaml"

def read_config(cfgfile):
    with open(cfgfile,'r') as fp:
        cfg = yaml.safe_load(fp)
    return cfg

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # load config
    cfg = read_config(CONFIGFILE)
    logger.debug("Config values:")
    for k,v in cfg.items():
        logger.debug(f"\t{k}: {v}")

    local_data_ = cfg['LOCAL_DATA']
    clone_to_ = cfg['CLONE_TARGET']
    clone_from_ = cfg['GIT_REPO']
    git_branch_ = cfg['GIT_BRANCH']
    jsonfile_ = cfg['JSONFILE']
    outfile_ = cfg['MTSP_OUTFILE']
    nrecs_ = cfg['N_RECS']


    # make dirs
    os.makedirs(local_data_, exist_ok=True)

    # clone or refresh metasploit
    r = RepoManager(
            working_dir=clone_to_,
            clone_url=clone_from_,
            branch=git_branch_,
    )
    r.pull_or_clone()

    # parse json
    logger.debug(f"Checking for json file at {jsonfile_}")
    assert(os.path.exists(jsonfile_))
    logger.debug(f"json file exists at {jsonfile_}")

    df = mtsp_json.json_to_df(jsonfile_)
    logger.info(f"Read {len(df)} records from {jsonfile_}")

    logger.debug(f"Cleaning data")
    df = mtsp_json.clean_df(df)

    df = mtsp_json.only_cves(df)
    logger.info(f"Filtered to {len(df)} CVE-related records from {jsonfile_}")

    # output csv
    logger.info(f"Writing CVE-related records to {outfile_}")
    df.to_csv(outfile_, index=True)

    # print stuff
    df = df.reset_index()

    logger.info(f"Here are the {nrecs_} most recent records")
    for record in df.tail(nrecs_).to_dict(orient="records"):
        logger.info("-"*20)
        for k,v in record.items():
            logger.info(f"{k}: {v}")
