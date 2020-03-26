I followed these steps to verify install and test:
1. Make a fresh install of 18.04 on a separate computer
2. Ran these commands

```
sudo apt update
```
```
sudo apt upgrade
```
```
sudo apt install python3
```
```
sudo apt install python3-venv
```
```
git clone https://github.com/sean-maclane/cpsc-449-group-c-project-1.git
```
```
cd cpsc-449-group-c-project-1
```
```
python3 -m venv venv
```
```
. venv/bin/activate
```
```
pip install -e .
```
```
pip install '.[test]'
```
```
pytest --tb=line
```