import sass
import os

def compile_scss(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.scss'):
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_dir, file.replace('.scss', '.css'))
                with open(input_file, 'r') as f:
                    compiled_css = sass.compile(string=f.read(), indented=False)
                    with open(output_file, 'w') as out_f:
                        out_f.write(compiled_css)
                print(f"Compiled {input_file} to {output_file}")

if __name__ == "__main__":
    input_dir = 'app/static/scss'
    output_dir = 'app/static/css'
    compile_scss(input_dir, output_dir)
