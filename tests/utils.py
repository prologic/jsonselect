from json import load, loads


MARKER_MAP = {
    "{": "}",
    "[": "]"
}


def get_tests(test_path):
    inputs = {}
    for selector_path in test_path.visit("*.selector"):
        input_path = selector_path.new(
            purebasename=selector_path.purebasename.split("_")[0],
            ext="json"
        )

        output_path = selector_path.new(ext="output")

        if input_path not in inputs:
            with input_path.open("r") as f:
                inputs[input_path] = load(f)

        with selector_path.open("r") as selector_f:
            with output_path.open("r") as output_f:
                yield (
                    selector_f.read().strip(),
                    inputs[input_path],
                    read_output(output_f),
                    selector_path.purebasename,
                )


def parse_output(output):
    marker = None
    collected = []
    collecting = ""

    for line in output.split("\n"):
        if not line:
            continue

        # int value?
        try:
            collected.append(int(line))
            continue
        except ValueError:
            pass

        # string
        if line[0] == "\"":
            collected.append(loads(line))
            continue

        # closing object or array
        if line[0] == marker:
            collecting += line
            collected.append(loads(collecting))
            collecting = ""
            marker = None
            continue

        # opening object or array
        if line[0] in "[{":
            marker = MARKER_MAP[line[0]]
            collecting += line
            continue

        # object or array body
        if marker:
            collecting += line
            continue

        # anything else
        collected.append(line)

    return collected


def items_equal(l1, l2):
    """assert that two lists and their items are equal

    Taken from: http://stackoverflow.com/questions/12813633
    """

    return len(l1) == len(l2) and sorted(l1) == sorted(l2)


def read_output(output_f):
    output = output_f.read().strip()

    try:
        output = loads(output)
        return output
    except ValueError:
        return parse_output(output)
