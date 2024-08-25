import os
from dotenv import load_dotenv

def test_environment_variables():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Lista de variáveis de ambiente que você deseja testar
    env_vars = [
        'IAM_ROLE_ARN',
        'LAYER_ARN',
        'SQS_QUEUE_ARN'
    ]

    for var in env_vars:
        value = os.getenv(var, 'Not Set')
        print(f'{var}: {value}')

if __name__ == "__main__":
    test_environment_variables()
