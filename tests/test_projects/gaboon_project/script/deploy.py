from src import Counter
import os
import boa

def deploy():
    counter = Counter.deploy()
    print("Starting count: ", counter.number())
    counter.increment()
    print("Ending count: ", counter.number())

def main():
    deploy()