c = get_config()

# Export all the notebooks in the current directory to the sphinx_howto format.
c.NbConvertApp.notebooks = ["notebook1.ipynb"]
c.NbConvertApp.export_format = "python"
