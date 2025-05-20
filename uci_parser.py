import re

def parse_file(content: str, config_name: str = None):
    lines = content.strip().splitlines()

    config_specified=True

    section_name = ""
    section_index = 0

    output_lines = [""]

    if config_name is None:
        config_specified = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if not config_specified:
            match = re.match(r'^CONFIGNAME:\S+$', line)
            if match:
                print("MATCH: " + line)
                config_name = line.split(":")[1].strip()
                output_lines.append("")

        if line.startswith("config"):
            parts = line.split()
            section_type = parts[1].strip("'\"")
            if len(parts) > 2:
                section_name = parts[2].strip("'\"")
            else:
                section_name = f"cfg{section_index:04d}"
                section_index += 1

            output_lines.append(f"set {config_name}.{section_name}={section_type}")

        elif line.startswith("option") or line.startswith("list"):
            parts = re.split(r'\s+', line, maxsplit=2)
            if len(parts) < 3:
                continue  # skip malformed lines
            key_type, key, value = parts
            key = key.strip("'\"")
            value = value.strip("'\"")
            if key_type == "option":
                output_lines.append(f"set {config_name}.{section_name}.{key}='{value}'")
            elif key_type == "list":
                output_lines.append(f"add_list {config_name}.{section_name}.{key}='{value}'")

    return "\n".join(output_lines)
