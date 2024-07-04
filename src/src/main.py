import sys
from xml.dom import minidom
from game import Game
from maze import Maze
from state import State


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("INPUT LENGTH ERROR! Use:\n\tpython src/main.py \"xml string\"\n"
                         "\tpython src/main.py <xml_file>")

    mazeXml = sys.argv[1]
    if "<Maze>" not in mazeXml:
        with open(mazeXml, "r") as file:
            mazeXml = file.read()

    visualize = False

    compiler = Maze(mazeXml)
    state = State(compiler.maze, compiler.level, compiler.start, compiler.escape, compiler.traps)
    g = Game(compiler, 128)
    result = compiler.outputXML(g.ai_play(visualize=visualize))

    dom = minidom.parseString(result)
    xml_str = dom.toprettyxml(indent="  ")
    print(xml_str)
