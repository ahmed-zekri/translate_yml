import argparse
import subprocess

import yaml


def translate_value(value):
    global counter
    counter += 1
    print(f'translating {counter} of {all_items}')
    value = translator.translate(sub_value, src='thai', dest='fr').text
    print(translator.translate(value,src='fr'))
    return str(value).replace('_char_', '%')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple program to automatically translate symfony yml files')
    from googletrans import Translator

    subprocess.run(['pip', 'install', '--upgrade', 'googletrans'])
    translator = Translator(service_urls=[
        'translate.google.com',
        'translate.google.co.kr',
    ])
    with open(file='messages.th-10-05-2021-2.yml', mode='r', encoding='utf-8') as file:
        content = file.read()
        parsed_yaml_output = dict()
        parsed_yaml = yaml.safe_load(content.replace('%', '_char_'))
        all_items = sum(len(list(item)) for item in list(parsed_yaml.values()))

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
        yaml.dump(parsed_yaml_output, file)
