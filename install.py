import os

os.system("python setup.py bdist_wheel")
bullish_install = os.listdir("dist")[0]
os.system("echo y | pip uninstall bullish && pip install " + os.path.join("dist", bullish_install))