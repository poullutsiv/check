import os
import jinja2
from flask import Flask, render_template, request
from checker import flake8_checker, mypy_checker, pydocstyle_checker, coverage_checker


def create_app() -> Flask:
    app = Flask(__name__, static_url_path='/static')

    project_path = os.path.dirname(app.root_path)
    templates_path = os.path.join(project_path, 'templates')
    my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['/templates', project_path, templates_path]),
    ])
    app.jinja_loader = my_loader

    app.static_folder = os.path.join(project_path, 'static')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload_file')
    def upload():
        return render_template('upload_file.html')

    @app.route('/checked_code', methods=['POST'])
    def update():
        if request.method == "POST":
            results = {}
            code = ''
            if str(request.referrer).replace(request.host_url, '') == 'upload_file':
                code_file = request.files['code_file']
                code = code_file.read()
                code = code.decode("utf-8")

            else:
                code = request.form['code']
                config_flake = {}
                flake8_checkbox = request.form.get('Flake8')
                mypy_checkbox = request.form.get('MyPy')
                pydocstyle_checkbox = request.form.get('PyDocStyle')
                coverage_checkbox = request.form.get('Coverage')
                mypy1 = request.form.get('MyPy1')
                mypy2 = request.form.get('MyPy2')
                mypy3 = request.form.get('MyPy3')
                mypy4 = request.form.get('MyPy4')
                mypy5 = request.form.get('MyPy5')
                mypy6 = request.form.get('MyPy6')

                with open('code.txt', 'w') as f:
                    f.write(code)

                if flake8_checkbox == 'on':
                    config_flake['line_length'] = request.form['flake-config']
                    config_flake['ignore_errors'] = request.form['flake-ignore']
                    results['Flake8'] = flake8_checker(config_flake)

                if mypy_checkbox == 'on':
                    args = []
                    if mypy1 == 'on':
                        args.append("--disallow-any-unimported")
                    if mypy1 == 'on':
                        args.append("--disallow-untyped-calls")
                    if mypy1 == 'on':
                        args.append("--no-warn-no-return")
                    if mypy1 == 'on':
                        args.append("--no-implicit-optional")
                    if mypy1 == 'on':
                        args.append("--warn-unused-ignores")
                    if mypy1 == 'on':
                        args.append("--warn-redundant-casts")
                    results['MyPy'] = mypy_checker(args)


                if pydocstyle_checkbox == 'on':
                    config_pydocstyle = request.form['pydocstyle-ignore']
                    results['PyDocStyle'] = pydocstyle_checker(config_pydocstyle)

                if coverage_checkbox == 'on':
                    results['Coverage'] = coverage_checker()

            return render_template('checked-code.html', code_text=code, res=results)

    return app
