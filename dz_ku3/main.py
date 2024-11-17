from ruamel.yaml import YAML
import sys


def read_and_write_yaml_line_by_line(input_file, output_file):
    yaml = YAML()
    yaml.preserve_quotes = True

    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        comment = 0
        current_tab = 0
        constants = {}
        for i, line in enumerate(lines):
            if line[0] == '#':
                if i + 1 < len(lines):
                    if lines[i + 1][0] == '#':
                        if comment == 0:
                            comment = 1
                            outfile.write('=begin\n')
                            outfile.write(line.replace('#', ''))
                        else:
                            outfile.write(line.replace('#', ''))
                    elif comment == 0:
                        outfile.write(line.replace('#', '!'))
                    else:
                        outfile.write(line.replace('#', ''))
                        outfile.write('=end\n')
                        comment = 0
                else:
                    if comment == 1:
                        outfile.write(line.replace('#', ''))
                        outfile.write('=end\n')
                    else:
                        outfile.write(line.replace('#', '!'))
            elif line[:5] == 'const':
                temp = line.split()
                constants[temp[1]] = int(temp[3])
                outfile.write('(def ' + temp[1] + ' ' + temp[3] + ')\n')
            elif line[0] == '$':
                temp = line.split()
                if temp[0][-1] == '+':
                    outfile.write('@(' + temp[1] + ' ' + temp[2][0] + ' +)\n')
                    outfile.write(str(constants[temp[1]] + int(temp[2][0])) + '\n')
                else:
                    temp[2] = temp[2][:-1]
                    outfile.write('@(' + temp[1] + ' ' + temp[2] + ' min)\n')
                    outfile.write(str(min(constants[temp[1]], constants[temp[2]])) + '\n')
            else:
                if i + 1 < len(lines):
                    if '#' in line:
                        temp = line.split('#')
                        outfile.write(temp[0].replace(':', ' ->') + '!' + temp[1])
                    else:
                        outfile.write(line.replace(':', ' ->'))
                    if lines[i + 1].count('   ') > current_tab:
                        outfile.write(current_tab * '   ' + '{\n')
                        current_tab += 1
                    elif lines[i + 1].count('   ') < current_tab:
                        while current_tab != lines[i + 1].count('   '):
                            current_tab -= 1
                            outfile.write(current_tab * '   ' + '}\n')
                else:
                    if '#' in line:
                        temp = line.split('#')
                        outfile.write(temp[0].replace(':', ' ->') + '!' + temp[1] + '\n')
                    else:
                        outfile.write(line.replace(':', ' ->') + '\n')
                    if current_tab != 0:
                        while current_tab != 0:
                            current_tab -= 1
                            outfile.write(current_tab * '   ' + '}\n')

    print(f"Содержимое YAML файла построчно записано в {output_file}")


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    read_and_write_yaml_line_by_line(input_file, output_file)
