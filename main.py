import pandas as pd
import yaml
import os
import logging
import sys

from mtsp_parser import mtsp_json
from mtsp_parser.repo_manager import RepoManager

logger = logging.getLogger()
# we now set this in main
# logger.setLevel(logging.DEBUG)
hdlr = logging.StreamHandler(sys.stderr)
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
    DEBUG = cfg['DEBUG']
    VERBOSE = cfg['VERBOSE']

    if DEBUG:
        logger.setLevel(logging.DEBUG)
    elif VERBOSE:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)

    logger.debug("Config values:")
    for k,v in cfg.items():
        logger.debug(f"\t{k}: {v}")



    local_data_ = cfg['LOCAL_DATA']
    clone_to_ = cfg['CLONE_TARGET']
    clone_from_ = cfg['GIT_REPO']
    git_branch_ = cfg['GIT_BRANCH']
    jsonfile_ = cfg['JSONFILE']
    outfile_cve = cfg['MTSP_OUTFILE_CVE']
    outfile_all = cfg['MTSP_OUTFILE_ALL']
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

    df = mtsp_json.clean_df(df)

    cve_df = mtsp_json.only_cves(df)
    logger.info(f"Filtered to {len(cve_df)} CVE-related records from {jsonfile_}")

    # output csv
    logger.info(f"Writing all records to {outfile_all}")
    df.to_csv(outfile_all, index=True)

    logger.info(f"Writing CVE-related records to {outfile_cve}")
    cve_df.to_csv(outfile_cve, index=True)


    # print stuff
    # df = df.reset_index()
    cve_df = cve_df.reset_index()

    # print()
    # print()
    # print(f"=== {nrecs_} most recent records (all references) ===")
    # for record in df.tail(nrecs_).to_dict(orient="records"):
    #     print()
    #     print("-"*20)
    #     for k,v in record.items():
    #         print(f"{k}: {v}")


    print()
    print()
    print(f"=== {nrecs_} most recent CVE-related records ===")
    for record in cve_df.tail(nrecs_).to_dict(orient="records"):
        print()
        print("-"*20)
        for k,v in record.items():
            print(f"{k}: {v}")
