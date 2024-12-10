import re
import math
import sys
import yaml


# Функция для вычисления выражений в префиксной форме
def evaluate_expression(expr, constants):
    if isinstance(expr, list):
        op = expr[0]
        if op == "+":
            return sum(evaluate_expression(e, constants) for e in expr[1:])
        elif op == "-":
            return evaluate_expression(expr[1], constants) - sum(evaluate_expression(e, constants) for e in expr[2:])
        elif op == "*":
            result = 1
            for e in expr[1:]:
                result *= evaluate_expression(e, constants)
            return result
        elif op == "/":
            result = evaluate_expression(expr[1], constants)
            for e in expr[2:]:
                divisor = evaluate_expression(e, constants)
                if divisor == 0:
                    raise ValueError("Division by zero")
                result /= divisor
            return result
        elif op == "len":
            return len(evaluate_expression(expr[1], constants))
        elif op == "sqrt":
            return math.sqrt(evaluate_expression(expr[1], constants))
        else:
            raise ValueError(f"Unknown operator: {op}")
    else:
        if expr.isdigit():
            return int(expr)
        elif expr in constants:
            return constants[expr]
        else:
            raise ValueError(f"Unknown value: {expr}")


# Функция для парсинга и обработки входного текста
def parse_input(input_text):
    # Убираем многострочные комментарии
    input_text = re.sub(r'{{!.*?}}', '', input_text, flags=re.DOTALL)

    # Словарь для хранения констант
    constants = {}

    # Обработка let-конструкций
    let_pattern = r'let (\w+) = (.*?);'
    let_matches = re.findall(let_pattern, input_text)
    for name, value in let_matches:
        value = value.strip()
        if value.startswith('#('):  # Если это массив
            value = value[2:-1].split(", ")
            constants[name] = value
        elif value.isdigit():  # Если это число
            constants[name] = int(value)
        elif value.startswith("^["):  # Если это выражение
            value = value[2:-1].split()
            constants[name] = evaluate_expression(value, constants)
        else:
            raise ValueError(f"Invalid value for constant: {value}")

    # Словарь для хранения итоговых данных
    result = {}

    # Заменяем let в тексте на значения из constants
    for name, value in constants.items():
        result[name] = value

    # Преобразуем все выражения ^[...] в их вычисленные значения
    expr_pattern = r'\^\[(.*?)\]'
    expr_matches = re.findall(expr_pattern, input_text)
    for match in expr_matches:
        expression_value = evaluate_expression(match.split(), constants)
        result[match] = expression_value

    return result


# Функция для обработки входных данных и преобразования их в YAML
def main():
    input_text = sys.stdin.read()

    try:
        parsed_data = parse_input(input_text)
        yaml_output = yaml.dump(parsed_data, sort_keys=False)
        print(yaml_output)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
