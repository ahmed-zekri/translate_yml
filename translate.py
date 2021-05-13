import argparse
import datetime
import subprocess
import concurrent.futures
import sys
import time


def translate_value(value, sub_key, key, sub_sub_key=None):
    global counter
    global parsed_yaml
    counter += 1
    print(f'translating {counter} of {all_items}')
    try:
        value = translator.translate(value, lang_tgt=args.lang)
    except Exception as e:
        print(e)

    value = str(value).replace('_char_', '%') if type(value) is str else value[0]
    print(value)
    if sub_sub_key is None:
        parsed_yaml[key][sub_key] = value
    else:
        parsed_yaml[key][sub_key][sub_sub_key] = value


def count_yml(parsed_yaml):
    sum = 0
    for index, item in parsed_yaml.items():
        for _, sub_item in item.items():
            if type(sub_item) is str:
                sum += 1
            if type(sub_item) is dict:
                sum += len(sub_item)
    return sum


def print_progress():
    dots = 0
    while not dependencies_installed:
        if dots == 0:
            printed_dots = ''
        elif dots == 1:
            printed_dots = '.'
        elif dots == 2:
            printed_dots = '..'
        else:
            printed_dots = '...'
        print(f'\rinstalling/upgrading dependencies, this can take minutes on the first run{printed_dots}', end='')
        dots += 1
        if dots == 4:
            dots = 0
        time.sleep(0.5)


def translation_process(parsed_yaml, executor=None):
    for key, value in parsed_yaml.items():

        for sub_key, sub_value in value.items():

            if type(value[sub_key]) is not dict:
                if executor is not None:
                    executor.submit(translate_value, value[sub_key], sub_key, key)
                else:
                    translate_value(value[sub_key], sub_key, key)


            else:
                for sub_sub_key, sub_sub_value in value[sub_key].items():
                    if executor is not None:
                        executor.submit(translate_value, value[sub_key], sub_key, key, sub_sub_key=sub_sub_key)
                    else:
                        translate_value(value[sub_key], sub_key, key, sub_sub_key=sub_sub_key)


if __name__ == '__main__':
    date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    output_file_name = f'translated_{date}.yml'
    parser = argparse.ArgumentParser(description='A command line program to translate yaml files')
    parser.add_argument('-l', '--lang', type=str, default='en',
                        help='The language in which the yaml file will be translated, the values must be equals to country codes for example:'
                             'en for english, fr for french and so on ... ', )
    parser.add_argument('-f', '--file', required=True,
                        help='Add the path of the file to be translated (name of the file if it\'s at the same path)')
    parser.add_argument('-st', '--single-threading', default=False, action='store_true',
                        help='translate all values in the main thread instead of splitting the translation process across different threads, this will drastically slow down the translation but it\'s safer to use to avoid google blocking requests from the scripts')
    parser.add_argument('-o', '--output',
                        help='Specify the file name of the translated output file')
    args = parser.parse_args()
    single_threaded = args.single_threading
    if args.output is not None:
        extension = str().join(
            args.output[index] if index > len(args.output) - 6 else '' for index in
            range(len(args.output)))
        print(extension)

        if extension != '.yaml':
            args.output += '.yaml'

        output_file_name = args.output
    with concurrent.futures.ThreadPoolExecutor() as executor:
        dependencies_installed = False
        executor.submit(print_progress)
        subprocess.run(['pip', 'install', '--upgrade', 'google_trans_new'], capture_output=True)
        subprocess.run(['pip', 'install', '--upgrade', 'PyYaml'], capture_output=True)
        dependencies_installed = True
    from google_trans_new import google_translator
    import yaml

    translator = google_translator()

    with open(file=args.file, mode='r', encoding='utf-8') as file:
        content = file.read()

        parsed_yaml = yaml.safe_load(content.replace('%', '_char_'))

        all_items = count_yml(parsed_yaml)

        counter = 0
        if not single_threaded:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                translation_process(parsed_yaml, executor=executor)
        else:
            translation_process(parsed_yaml)

    with open(file=output_file_name, mode='w', encoding='utf-8') as file:
        file.write(yaml.dump(parsed_yaml, allow_unicode=True))
