# Auto-Screenshot
A tool for speeding up repetitive screenshots of fixed regions on your screen.

## Usage
### Setting up the project
Clone the repo and `cd` into it.
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements
```

### Running the script
Start the script
```sh
python main.py take-all-screenshots
```
Using the interactive script:
1. Set the button position by pressing "b" to record the position of your cursor.
2. Set the intial screenshot region by pressing "s" twice to record the position of your cursor on opposite corners of the region.
3. To take a screenshot using the same region as previously set, press "c".
4. To set a new region, press "n" and then repeat Step 2.

