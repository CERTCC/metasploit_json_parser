# Metasploit Database Parser

The open-source metasploit framework
https://github.com/rapid7/metasploit-framework
contains a JSON database listing each module within
the tool along with a list of references to source URLs, 
vulnerability IDs, etc.

The code in this repository performs the following tasks:
1. Clones or pulls the latest metasploit code from github
2. Parses the JSON database
3. Extracts the relevant data from the JSON database
4. Emits two CSV files:
    * A complete list of every file with every reference
    * A list of only CVE references and accompanying files
    
## Usage

Clone this repository.

```bash
git clone <clone_url_for_this_repo>
```

Use of a virtual environment such as anaconda is highly 
recommended to avoid polluting your native python installation
with possibly incompatible packages.

This script was written using python 3.9.
It should probably work for any version 3 python interpreter, although I make no guarantees of that.

```bash
conda create --name myenv python=3.9
conda activate myenv
pip install -r requirements.txt
```

Edit the `config.yaml` as needed.

Run `main.py`

```python
python main.py
```

Skim the output, or have a look at the resulting CSV files
(in `./DATA` by default).

