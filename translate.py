import argparse
import subprocess


def translate_value(value):
    global counter
    counter += 1
    print(f'translating {counter} of {all_items}')
    value = translator.translate(value, lang_tgt='fr')
    value = str(value).replace('_char_', '%') if type(value) is str else value[0]
    print(value)
    return value


def count_yml(parsed_yaml):
    sum = 0
    for index, item in parsed_yaml.items():
        for _, sub_item in item.items():
            if type(sub_item) is str:
                sum += 1
            if type(sub_item) is dict:
                sum += len(sub_item)
    return sum


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple program to automatically translate symfony yml files')
    print(f'Installing/upgrading dependencies')
    subprocess.run(['pip', 'install', '--upgrade', 'google_trans_new'], capture_output=True)
    subprocess.run(['pip', 'install', '--upgrade', 'PyYaml'], capture_output=True)
    from google_trans_new import google_translator
    import yaml

    translator = google_translator()

    with open(file='messages.th-10-05-2021-2.yml', mode='r', encoding='utf-8') as file:
        content = file.read()
        parsed_yaml_output = dict()
        parsed_yaml = yaml.safe_load(content.replace('%', '_char_'))

        all_items = count_yml(parsed_yaml)

        counter = 0
        for key, value in parsed_yaml.items():

            for sub_key, sub_value in value.items():

                if type(value[sub_key]) is not dict:
                    value[sub_key] = translate_value(value[sub_key])

                else:
                    for sub_sub_key, sub_sub_value in value[sub_key].items():
                        value[sub_key][sub_sub_key] = translate_value(value[sub_key][sub_sub_key])

            parsed_yaml_output[key] = value
    with open(file='translated.yml', mode='w') as file:
        yaml.safe_dump(parsed_yaml_output, file, encoding='utf-8')
