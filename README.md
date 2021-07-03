# Udemy project for learning blockchain

**Activate the virtual environment**

```
python -m venv blockchain-env
source ./blockchain-env/bin/activate
```

**Install all packages**

```
pip install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment.

```
python -m pytest backend/tests/
```

**Run the application and API**

Make sure to activate the virtual environment.

```
python -m backend.app
or
python -m backend.app
```

**Run a peer instance**

Make sure to activate the virtual environment.

```
export PEER=True && python -m backend.app
```
