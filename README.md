# Door movement prediction

The original datasets used for the project can be downloaded [here](https://gitlab.pld.ttu.ee/IAS0360/IAS0360_project_door).

## UI interface

The UI interface is developed with the library `streamlit`.
In order to run the program it has to be installed:

```
>$ pip3 install streamlit
```

And to run the interface, after uncompressing `labeled_door1.csv.zip`:
```
>$ streamlit run UI_params.py
```
A browser should open inmediately with the interface, and in case it doesn't, it can be accessed at `http://localhost:8501/`.

## Python implementation
The script `implementation.py` is the whole implementation of the workflow in one script. It can be executed on terminal with:
```
$> python3 implementation.py

optional arguments:
  -h, --help            show this help message and exit
  -df [DF], --df [DF]   Dataframe used, by default data/data_door1.txt
  -range [DFRANGE], --dfRange [DFRANGE]
                        Number of rows used (by default maximum)
  -v [VERB], --verb [VERB]
                        Verbosity of terminal input, 1 for information on each
                        iteration
```

## C implementation
(TODO)

## Notebooks
In the notebooks folders can be found all the jupyter notebooks used for exploration and designing of the algorithms
