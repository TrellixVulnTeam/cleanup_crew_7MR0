from pydaisi import Daisi


if __name__ == '__main__':
    daisi = Daisi("Rocket League Replay Analyzer", base_url='https://dev3.daisi.io')
    with open('d65f4255-1ec1-4ed4-95c3-359e7084127d.replay', 'rb') as in_file:
        result = daisi.process_replay_raw(file_path=in_file.read())
        print(type(result.value()))