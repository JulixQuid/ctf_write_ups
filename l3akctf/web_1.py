import jsbeautifier

# Path to the input JavaScript file
input_file = "/home/julixquid/Downloads/dist/src/static/js/sanitize-html.min.js"

# Path to the output beautified JavaScript file
output_file = "l3akctf/beautified.js"

# Read the input file
with open(input_file, "r") as f:
    ugly_js = f.read()

# Beautify the JavaScript code
beautified_js = jsbeautifier.beautify(ugly_js)

# Write the beautified code to the output file
with open(output_file, "w") as f:
    f.write(beautified_js)

print(f"Beautified JavaScript saved to: {output_file}")